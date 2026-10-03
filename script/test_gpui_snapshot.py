import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

from gpui_snapshot import export_snapshot, inventory, verify_resolution, verify_snapshot


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "--quiet")
        self.write(
            "Cargo.toml",
            """[workspace]
resolver = "2"
members = ["crates/*"]
[workspace.package]
edition = "2024"
publish = false
[workspace.dependencies]
gpui = { path = "crates/gpui" }
dev_helper = { path = "crates/dev_helper" }
build_helper = { path = "crates/build_helper" }
target_helper = { path = "crates/target_helper" }
unused = { path = "crates/unused" }
[workspace.lints.rust]
unsafe_code = "deny"
[patch.crates-io]
external = { git = "https://example.invalid/external", rev = "1111111111111111111111111111111111111111" }
[profile.dev]
opt-level = 1
""",
        )
        for name in (
            "gpui",
            "gpui_platform",
            "dev_helper",
            "build_helper",
            "target_helper",
            "unused",
        ):
            self.write(
                f"crates/{name}/Cargo.toml",
                f'''[package]
name = "{name}"
version = "0.1.0"
edition.workspace = true
publish.workspace = true
[lints]
workspace = true
''',
            )
            self.write(f"crates/{name}/src/lib.rs", "pub fn fixture() {}\n")
        with (self.repo / "crates/gpui/Cargo.toml").open("a") as handle:
            handle.write("""[dev-dependencies]
dev_helper.workspace = true
[build-dependencies]
build_helper.workspace = true
[target.'cfg(windows)'.dependencies]
target_helper.workspace = true
""")
        with (self.repo / "crates/gpui_platform/Cargo.toml").open("a") as handle:
            handle.write("[dependencies]\ngpui.workspace = true\n")
        for path, content in {
            "LICENSE-APACHE": "Apache fixture\n",
            "LICENSE-GPL": "GPL fixture\n",
            "assets/fonts/fixture.ttf": "font fixture\n",
            "Cargo.lock": "version = 4\n",
            ".cargo/config.toml": '[env]\nFIXTURE = "yes"\n',
            "rust-toolchain.toml": '[toolchain]\nchannel = "stable"\n',
        }.items():
            self.write(path, content)
        self.write("crates/gpui/fixture.sh", "#!/bin/sh\nexit 0\n")
        (self.repo / "crates/gpui/fixture.sh").chmod(0o755)
        (self.repo / "crates/gpui/src/alias.rs").symlink_to("lib.rs")
        for path in ("Cargo.toml", "Cargo.lock", ".cargo/config.toml", "rust-toolchain.toml"):
            self.write(f"alloy-source/{path}", (self.repo / path).read_text())
        self.packages = {
            name: f"crates/{name}/Cargo.toml"
            for name in ("gpui", "gpui_platform", "dev_helper", "build_helper", "target_helper")
        }
        original_tree = self.root / "original"
        for path in (
            *(str(Path(path).parent) for path in self.packages.values()),
            "assets/fonts",
            "alloy-source",
        ):
            shutil.copytree(self.repo / path, original_tree / path, symlinks=True)
        for path in ("Cargo.toml", "LICENSE-APACHE", "LICENSE-GPL"):
            shutil.copy2(self.repo / path, original_tree / path)
        (original_tree / "README.md").write_text("Original generated README\n")
        original = {
            "format": 1,
            "upstream": "1" * 40,
            "revision": "2" * 40,
            "roots": ["crates/gpui", "crates/gpui_platform"],
            "packages": self.packages,
            "files": inventory(original_tree),
        }
        original_bytes = json.dumps(original, sort_keys=True) + "\n"
        self.write("alloy-source/ALLOY-SNAPSHOT.json", original_bytes)
        self.source = {
            "format": 1,
            "kind": "standalone-source",
            "repository": "https://github.com/example/source",
            "upstream": original["upstream"],
            "revision": original["revision"],
            "snapshot_sha256": hashlib.sha256(original_bytes.encode()).hexdigest(),
        }
        self.write("ALLOY-SOURCE.json", json.dumps(self.source))
        self.write(".cargo/config.toml", '[env]\nSTANDALONE = "yes"\n')
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "fixture")
        self.revision = self.git("rev-parse", "HEAD").strip()
        self.snapshot = self.root / "snapshot"
        self.record = export_snapshot(self.repo, self.revision, self.snapshot)

    def git(self, *args):
        return subprocess.check_output(
            [
                "git",
                "-C",
                str(self.repo),
                "-c",
                "commit.gpgsign=false",
                "-c",
                "user.name=Snapshot Test",
                "-c",
                "user.email=test@example.invalid",
                *args,
            ],
            text=True,
        )

    def write(self, path, content):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def test_export_is_fixed_complete_and_reproducible(self):
        self.write("crates/gpui/src/lib.rs", "dirty checkout must not be exported\n")
        (self.repo / ".git/info/attributes").write_text("crates/gpui/src/lib.rs export-ignore\n")
        second = self.root / "second"
        repeated = export_snapshot(self.repo, self.revision, second)
        self.assertEqual(self.record, repeated)
        self.assertEqual(repeated["format"], 2)
        self.assertEqual(repeated["revision"], self.revision)
        self.assertEqual(repeated["source"], self.source)
        for path in self.record["files"]:
            self.assertEqual((self.snapshot / path).read_bytes(), (second / path).read_bytes())
        self.assertNotIn("ALLOY-SNAPSHOT.json", self.record["files"])
        self.assertIn("crates/gpui/src/lib.rs", repeated["files"])
        self.assertTrue(repeated["files"]["crates/gpui/fixture.sh"]["executable"])
        self.assertTrue((second / "crates/gpui/fixture.sh").stat().st_mode & 0o111)
        self.assertEqual(repeated["files"]["crates/gpui/src/alias.rs"]["type"], "symlink")
        self.assertEqual((second / "crates/gpui/src/alias.rs").readlink(), Path("lib.rs"))
        self.assertEqual(self.record["packages"], self.packages)
        manifest = tomllib.loads((self.snapshot / "Cargo.toml").read_text())
        self.assertNotIn("unused", manifest["workspace"]["dependencies"])
        self.assertNotIn("patch", manifest)
        self.assertNotIn("profile", manifest)
        self.assertFalse((self.snapshot / ".cargo/config.toml").exists())
        self.assertEqual(
            (self.snapshot / "alloy-source/.cargo/config.toml").read_text(),
            '[env]\nFIXTURE = "yes"\n',
        )
        self.assertEqual(verify_snapshot(self.repo, self.revision, self.snapshot), self.record)

    def test_verification_rejects_changed_extra_files_and_revision(self):
        source = self.snapshot / "crates/gpui/src/lib.rs"
        original = source.read_bytes()
        source.write_text("changed\n")
        with self.assertRaises(ValueError):
            verify_snapshot(self.repo, self.revision, self.snapshot)
        source.write_bytes(original)
        extra = self.snapshot / "unexpected.txt"
        extra.write_text("extra\n")
        with self.assertRaises(ValueError):
            verify_snapshot(self.repo, self.revision, self.snapshot)
        extra.unlink()
        record_path = self.snapshot / "ALLOY-SNAPSHOT.json"
        record_bytes = record_path.read_bytes()
        record_path.write_text(json.dumps(dict(self.record, revision="3" * 40)))
        with self.assertRaises(ValueError):
            verify_snapshot(self.repo, self.revision, self.snapshot)
        record_path.write_bytes(record_bytes)
        self.write("README.md", "second revision, same GPUI sources\n")
        self.git("add", "README.md")
        self.git("commit", "--quiet", "-m", "second revision")
        with self.assertRaises(ValueError):
            verify_snapshot(self.repo, self.git("rev-parse", "HEAD").strip(), self.snapshot)

    def test_export_rejects_changed_provenance_sources_and_package_closure(self):
        changes = {
            "record_digest": ("alloy-source/ALLOY-SNAPSHOT.json", "{}\n"),
            "record_origin": (
                "ALLOY-SOURCE.json",
                json.dumps(dict(self.source, revision="3" * 40)),
            ),
            "source": ("crates/gpui/src/lib.rs", "pub fn changed() {}\n"),
            "extra_source": ("crates/gpui/src/extra.rs", "pub fn extra() {}\n"),
            "package_closure": (
                "Cargo.toml",
                (self.repo / "Cargo.toml")
                .read_text()
                .replace('path = "crates/dev_helper"', 'path = "crates/unused"'),
            ),
        }
        for name, (path, content) in changes.items():
            with self.subTest(name=name):
                target = self.repo / path
                previous = target.read_bytes() if target.exists() else None
                self.write(path, content)
                self.git("add", ".")
                self.git("commit", "--quiet", "-m", name)
                with self.assertRaises(ValueError):
                    export_snapshot(
                        self.repo, self.git("rev-parse", "HEAD").strip(), self.root / name
                    )
                if previous is None:
                    target.unlink()
                else:
                    target.write_bytes(previous)
                self.git("add", ".")
                self.git("commit", "--quiet", "-m", "restore fixture")

    def test_resolution_checks_reachable_package_identity_and_path(self):
        consumer = self.root / "consumer"
        consumer.mkdir()
        (consumer / "Cargo.toml").write_text('[package]\nname="consumer"\nversion="0.1.0"\n')
        packages = [
            {
                "id": "opaque consumer",
                "name": "consumer",
                "source": None,
                "manifest_path": str(consumer / "Cargo.toml"),
            }
        ]
        packages += [
            {
                "id": f"opaque {index}",
                "name": name,
                "source": None,
                "manifest_path": str(self.snapshot / path),
            }
            for index, (name, path) in enumerate(self.record["packages"].items())
        ]
        metadata = {
            "packages": packages,
            "workspace_root": str(consumer),
            "workspace_members": [packages[0]["id"]],
            "resolve": {
                "root": packages[0]["id"],
                "nodes": [
                    {
                        "id": package["id"],
                        "deps": [
                            {"name": child["name"], "pkg": child["id"], "dep_kinds": []}
                            for child in packages[index + 1 : index + 2]
                        ],
                    }
                    for index, package in enumerate(packages)
                ],
            },
        }
        self.assertEqual(
            verify_resolution(metadata, consumer, self.snapshot, self.record), len(packages) - 1
        )
        for changed in ("wrong_path", "registry", "duplicate"):
            with self.subTest(changed=changed):
                invalid = copy.deepcopy(metadata)
                if changed == "wrong_path":
                    invalid["packages"][1]["manifest_path"] = str(consumer / "wrong/Cargo.toml")
                elif changed == "registry":
                    invalid["packages"][1]["source"] = (
                        "registry+https://github.com/rust-lang/crates.io-index"
                    )
                else:
                    duplicate = dict(invalid["packages"][1], id="duplicate candidate")
                    invalid["packages"].append(duplicate)
                    invalid["resolve"]["nodes"][0]["deps"].append(
                        {"name": duplicate["name"], "pkg": duplicate["id"], "dep_kinds": []}
                    )
                    invalid["resolve"]["nodes"].append({"id": duplicate["id"], "deps": []})
                with self.assertRaises(ValueError):
                    verify_resolution(invalid, consumer, self.snapshot, self.record)


if __name__ == "__main__":
    unittest.main()
