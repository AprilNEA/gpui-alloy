import copy
import unittest
from pathlib import Path

import gpui_registry_consumer as verifier


class RegistryConsumerTests(unittest.TestCase):
    def setUp(self):
        self.consumer = Path("/consumer")
        self.projection = {
            "format": 1,
            "kind": "registry-projection",
            "version": "0.1.0",
            "packages": {
                "gpui": {"package": "gpui-alloy"},
                "gpui_macros": {"package": "gpui-alloy-macros"},
            },
        }
        self.archives = {
            "packages": [
                {"name": "gpui-alloy", "version": "0.1.0", "sha256": "a" * 64},
                {"name": "gpui-alloy-macros", "version": "0.1.0", "sha256": "b" * 64},
            ]
        }
        self.lock = {
            "package": [
                {
                    "name": entry["name"],
                    "version": entry["version"],
                    "checksum": entry["sha256"],
                    "source": verifier.CRATES_IO,
                }
                for entry in self.archives["packages"]
            ]
        }
        self.metadata = {
            "workspace_root": str(self.consumer),
            "workspace_members": ["app"],
            "packages": [
                {"id": "app", "name": "app", "version": "0.1.0", "source": None},
                {
                    "id": "alloy",
                    "name": "gpui-alloy",
                    "version": "0.1.0",
                    "source": verifier.CRATES_IO,
                },
                {
                    "id": "macros",
                    "name": "gpui-alloy-macros",
                    "version": "0.1.0",
                    "source": verifier.CRATES_IO,
                },
            ],
            "resolve": {
                "nodes": [
                    {"id": "app", "deps": [{"pkg": "alloy"}]},
                    {"id": "alloy", "deps": [{"pkg": "macros"}]},
                    {"id": "macros", "deps": []},
                ]
            },
        }

    def verify(self):
        return verifier.verify_resolution(
            self.metadata, self.lock, self.projection, self.archives, self.consumer
        )

    def test_only_reachable_packages_are_checked(self):
        self.metadata["packages"].append(
            {"id": "unused", "name": "gpui", "version": "0.2.2", "source": None}
        )
        self.metadata["resolve"]["nodes"].append({"id": "unused", "deps": []})
        checked = self.verify()
        self.assertEqual([entry["name"] for entry in checked], ["gpui-alloy", "gpui-alloy-macros"])
        self.assertEqual(checked[0]["checksum"], "a" * 64)

    def test_wrong_source_version_or_checksum_fails(self):
        original = copy.deepcopy(self.metadata)
        for field, value, message in (
            ("source", None, "outside crates.io"),
            ("source", "git+https://example.test/alloy", "outside crates.io"),
            ("version", "0.1.1", "expected 0.1.0"),
        ):
            with self.subTest(field=field, value=value):
                self.metadata = copy.deepcopy(original)
                self.metadata["packages"][1][field] = value
                with self.assertRaisesRegex(ValueError, message):
                    self.verify()
        self.metadata = original
        self.lock["package"][0]["checksum"] = "c" * 64
        with self.assertRaisesRegex(ValueError, "checksum differs"):
            self.verify()

    def test_duplicate_family_identities_fail(self):
        self.metadata["packages"].append(
            {
                "id": "duplicate",
                "name": "gpui-alloy",
                "version": "0.1.1",
                "source": verifier.CRATES_IO,
            }
        )
        self.metadata["resolve"]["nodes"].append({"id": "duplicate", "deps": []})
        self.metadata["resolve"]["nodes"][0]["deps"].append({"pkg": "duplicate"})
        with self.assertRaisesRegex(ValueError, "multiple package identities"):
            self.verify()

    def test_original_family_copy_and_missing_core_fail(self):
        self.metadata["packages"][2]["name"] = "gpui_macros"
        with self.assertRaisesRegex(ValueError, "original GPUI family package"):
            self.verify()
        self.metadata["resolve"]["nodes"][0]["deps"] = []
        with self.assertRaisesRegex(ValueError, "does not resolve gpui-alloy"):
            self.verify()

    def test_incomplete_or_duplicate_archive_manifest_fails(self):
        removed = self.archives["packages"].pop()
        with self.assertRaisesRegex(ValueError, "every release package"):
            self.verify()
        self.archives["packages"].append(removed)
        self.archives["packages"].append(removed)
        with self.assertRaisesRegex(ValueError, "repeats package"):
            self.verify()


if __name__ == "__main__":
    unittest.main()
