import subprocess
import tempfile
import unittest
from pathlib import Path

import gpui_registry as registry


class RegistryProjectionTests(unittest.TestCase):
    def test_registry_override_validates_inherited_identity_and_keeps_features(self):
        workspace = {
            "dependencies": {
                "executor": {
                    "package": "smol",
                    "version": "2.0",
                    "features": ["upstream"],
                    "default-features": False,
                }
            }
        }
        packages = {
            "smol": {
                "package": "gpui-alloy-smol",
                "directory": "external/smol",
                "source": {"git": "https://example.test/smol", "rev": "a" * 40},
            }
        }
        overrides = {
            "executor": {"source": {"package": "smol", "version": "2.0"}, "internal": "smol"}
        }
        value, internal = registry.dependency(
            "executor",
            {
                "workspace": True,
                "features": ["local"],
                "optional": True,
            },
            workspace,
            "crates/util",
            packages,
            "0.1.0",
            {},
            overrides,
        )
        self.assertEqual(internal, "smol")
        self.assertEqual(
            value,
            {
                "package": "gpui-alloy-smol",
                "version": "=0.1.0",
                "path": "../../external/smol",
                "features": ["upstream", "local"],
                "default-features": False,
                "optional": True,
            },
        )
        for changes in ({"version": "2.1"}, {"package": "another-smol"}, {"registry": "private"}):
            with (
                self.subTest(changes=changes),
                self.assertRaisesRegex(ValueError, "audited package/version"),
            ):
                registry.dependency(
                    "executor",
                    {"package": "smol", "version": "2.0", **changes},
                    {},
                    "crates/util",
                    packages,
                    "0.1.0",
                    {},
                    overrides,
                )

    def test_provenance_is_packaged_with_include_or_exclude_filters(self):
        for field, patterns in (
            ("include", ["src/**", f"!/{registry.PACKAGE_RECORD}"]),
            ("exclude", ["*.json"]),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                original = {
                    "package": {
                        "name": "fixture",
                        "version": "0.1.0",
                        "edition": "2024",
                        field: patterns,
                    }
                }
                manifest, _ = registry.project_manifest(
                    original,
                    {},
                    ".",
                    {"fixture": {"package": "gpui-alloy-fixture", "directory": "."}},
                    "0.1.0",
                    {},
                )
                (root / "Cargo.toml").write_text(registry.render_manifest(manifest))
                (root / "src").mkdir()
                (root / "src/lib.rs").write_text("pub fn fixture() {}\n")
                (root / registry.PACKAGE_RECORD).write_text("{}\n")
                (root / "excluded.json").write_text("{}\n")
                listed = subprocess.check_output(
                    ["cargo", "package", "--list", "--offline", "--allow-dirty"],
                    cwd=root,
                    stderr=subprocess.PIPE,
                    text=True,
                ).splitlines()
                self.assertIn(registry.PACKAGE_RECORD, listed)
                self.assertNotIn("excluded.json", listed)

    def test_manifest_preserves_aliases_features_and_library_identity(self):
        workspace = {
            "package": {"edition": "2024", "publish": False},
            "dependencies": {
                "core": {"package": "gpui", "path": "crates/gpui", "features": ["one"]},
                "download": {"version": "=1.2.3", "default-features": False},
            },
            "lints": {"rust": {"unsafe_code": "warn"}},
        }
        original = {
            "package": {"name": "gpui_apple", "version": "0.1.0", "edition": {"workspace": True}},
            "lib": {"path": "src/platform.rs"},
            "features": {"github-download": ["dep:download"]},
            "lints": {"workspace": True},
            "dependencies": {
                "core": {"workspace": True, "features": ["two", "one"]},
                "download": {"workspace": True, "optional": True},
            },
            "dev-dependencies": {"cyclic": {"path": "../cyclic"}},
            "example": [{"name": "demo"}],
            "target": {"cfg(unix)": {"dev-dependencies": {"test-helper": "1"}}},
        }
        packages = {
            "gpui": {"package": "gpui-alloy", "directory": "crates/gpui"},
            "gpui_apple": {"package": "gpui-alloy-apple", "directory": "crates/gpui_apple"},
        }
        result, reached = registry.project_manifest(
            original, workspace, "crates/gpui_apple", packages, "0.1.0", {}
        )
        self.assertEqual(result["lib"]["name"], "gpui_apple")
        self.assertEqual(result["package"]["edition"], "2024")
        self.assertEqual(
            result["dependencies"]["core"],
            {
                "package": "gpui-alloy",
                "path": "../gpui",
                "version": "=0.1.0",
                "features": ["one", "two"],
            },
        )
        self.assertEqual(result["dependencies"]["download"]["version"], "=1.2.3")
        self.assertFalse(result["dependencies"]["download"]["default-features"])
        self.assertEqual(result["features"], original["features"])
        self.assertEqual(reached, {"gpui"})
        self.assertNotIn("dev-dependencies", result)
        self.assertNotIn("dev-dependencies", result["target"]["cfg(unix)"])
        self.assertNotIn("example", result)
        self.assertIn("cyclic", original["dev-dependencies"])
        registry.render_manifest(result)

    def test_git_mapping_requires_audited_identity_and_preserves_features(self):
        source = {"git": "https://example.test/tar", "rev": "a" * 40}
        value = {**source, "optional": True, "features": ["download"]}
        with self.assertRaisesRegex(ValueError, "Audit a registry replacement"):
            registry.dependency("tar", value, {}, "crates/client", {}, "0.1.0", {})
        with self.assertRaisesRegex(ValueError, "Audit a registry replacement"):
            registry.dependency(
                "tar",
                value,
                {},
                "crates/client",
                {},
                "0.1.0",
                {"tar": {"source": {**source, "rev": "b" * 40}, "registry": {"version": "1"}}},
            )
        resolved, _ = registry.dependency(
            "tar",
            value,
            {},
            "crates/client",
            {},
            "0.1.0",
            {"tar": {"source": source, "registry": {"version": "=1.2.3", "package": "tar-fork"}}},
        )
        self.assertEqual(
            resolved,
            {
                "version": "=1.2.3",
                "package": "tar-fork",
                "optional": True,
                "features": ["download"],
            },
        )
        with self.assertRaisesRegex(ValueError, "preserve exact version pin"):
            registry.dependency(
                "tar",
                {**value, "version": "=1.2.3"},
                {},
                "x",
                {},
                "0.1.0",
                {"tar": {"source": source, "registry": {"version": "1.2.3"}}},
            )

    def test_git_member_uses_fixed_source_and_suite_version(self):
        source = {"git": "https://example.test/client", "rev": "a" * 40}
        packages = {
            "zed-client": {
                "package": "gpui-alloy-client",
                "directory": "external/gpui-alloy-client",
                "source": source,
            }
        }
        resolved, internal = registry.dependency(
            "client",
            {**source, "version": "0.12", "features": ["tls"]},
            {},
            "crates/http",
            packages,
            "0.1.0",
            {"client": {"source": source, "internal": "zed-client"}},
        )
        self.assertEqual(internal, "zed-client")
        self.assertEqual(
            resolved,
            {
                "version": "=0.1.0",
                "features": ["tls"],
                "package": "gpui-alloy-client",
                "path": "../../external/gpui-alloy-client",
            },
        )

    def test_build_adapter_and_external_license_are_self_contained(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            apple = root / "crates/gpui_apple"
            apple.mkdir(parents=True)
            original = b'fn location() { value.join("../gpui"); }\n'
            (apple / "build.rs").write_bytes(original)
            (root / "LICENSE").write_text("license text")
            (apple / "LICENSE").symlink_to("../../LICENSE")
            for name in registry.SHADER_INPUTS:
                path = root / "crates/gpui/src" / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"source bytes\n" + name.encode())
            links = registry.materialize_links(root, ["crates/gpui_apple"])
            adapter = registry.adapt_apple_build(root)
            self.assertFalse((apple / "LICENSE").is_symlink())
            self.assertEqual((apple / "LICENSE").read_text(), "license text")
            self.assertEqual(links["crates/gpui_apple/LICENSE"]["target"], "../../LICENSE")
            self.assertEqual(
                (apple / "build.rs").read_bytes(), original.replace(b"../gpui", b"vendor/gpui")
            )
            for name in registry.SHADER_INPUTS:
                self.assertEqual(
                    (apple / "vendor/gpui/src" / name).read_bytes(),
                    (root / "crates/gpui/src" / name).read_bytes(),
                )
            self.assertEqual(adapter["before_sha256"], registry.digest(original))


if __name__ == "__main__":
    unittest.main()
