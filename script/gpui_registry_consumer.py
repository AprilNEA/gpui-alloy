#!/usr/bin/env python3
"""Verify a consumer resolves the frozen Alloy release from crates.io."""

import argparse
import hashlib
import json
import re
import subprocess
import tomllib
from pathlib import Path

CRATES_IO = "registry+https://github.com/rust-lang/crates.io-index"


def verify_resolution(metadata, lock, projection, archives, consumer):
    if projection["format"] != 1 or projection["kind"] != "registry-projection":
        raise ValueError("Expected an Alloy registry projection record.")
    if Path(metadata["workspace_root"]).resolve() != consumer.resolve():
        raise ValueError("Cargo metadata describes a different consumer workspace.")
    if metadata["resolve"] is None:
        raise ValueError("Cargo metadata must include the dependency graph.")
    version = projection["version"]
    names = {entry["package"] for entry in projection["packages"].values()}
    expected = {}
    for archive in archives["packages"]:
        name = archive["name"]
        if name in expected:
            raise ValueError(f"Archive manifest repeats package {name}.")
        if archive["version"] != version or not re.fullmatch(r"[0-9a-f]{64}", archive["sha256"]):
            raise ValueError(f"Archive manifest has an invalid version or checksum for {name}.")
        expected[name] = archive["sha256"]
    if expected.keys() != names:
        raise ValueError(
            "Archive manifest must contain every release package and no other packages."
        )
    packages = {package["id"]: package for package in metadata["packages"]}
    nodes = {node["id"]: node for node in metadata["resolve"]["nodes"]}
    pending = list(metadata["workspace_members"])
    reached = set()
    family = {}
    while pending:
        package_id = pending.pop()
        if package_id in reached:
            continue
        reached.add(package_id)
        pending.extend(dependency["pkg"] for dependency in nodes[package_id]["deps"])
        package = packages[package_id]
        name = package["name"]
        if name in projection["packages"]:
            raise ValueError(f"Consumer still resolves an original GPUI family package: {name}.")
        if name not in names:
            if name == "gpui-alloy" or name.startswith("gpui-alloy-"):
                raise ValueError(
                    f"Consumer resolves an Alloy package outside this release: {name}."
                )
            continue
        if name in family:
            raise ValueError(f"Consumer resolves multiple package identities for {name}.")
        family[name] = package
    if "gpui-alloy" not in family:
        raise ValueError("Consumer does not resolve gpui-alloy.")
    checked = []
    for name, package in sorted(family.items()):
        if package["version"] != version:
            raise ValueError(f"Consumer resolves {name} {package['version']}; expected {version}.")
        if package["source"] != CRATES_IO:
            raise ValueError(f"Consumer resolves {name} outside crates.io: {package['source']}.")
        matches = [
            entry
            for entry in lock["package"]
            if (entry["name"], entry["version"], entry.get("source")) == (name, version, CRATES_IO)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Cargo.lock must contain one crates.io identity for {name} {version}."
            )
        if matches[0].get("checksum") != expected[name]:
            raise ValueError(f"Cargo.lock checksum differs from the frozen archive for {name}.")
        checked.append(
            {"name": name, "version": version, "source": CRATES_IO, "checksum": expected[name]}
        )
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer", required=True, type=Path)
    parser.add_argument("--projection", required=True, type=Path)
    parser.add_argument("--archives", required=True, type=Path)
    parser.add_argument("--target", default="aarch64-apple-darwin")
    args = parser.parse_args()
    consumer = args.consumer.resolve()
    projection_bytes = args.projection.read_bytes()
    archive_bytes = args.archives.read_bytes()
    lock_bytes = (consumer / "Cargo.lock").read_bytes()
    command = [
        "cargo",
        "metadata",
        "--format-version",
        "1",
        "--locked",
        "--all-features",
        "--filter-platform",
        args.target,
    ]
    metadata_bytes = subprocess.check_output(command, cwd=consumer)
    if (consumer / "Cargo.lock").read_bytes() != lock_bytes:
        raise ValueError("Cargo.lock changed while the consumer dependency graph was inspected.")
    projection = json.loads(projection_bytes)
    checked = verify_resolution(
        json.loads(metadata_bytes),
        tomllib.loads(lock_bytes.decode()),
        projection,
        json.loads(archive_bytes),
        consumer,
    )
    report = {
        "format": 1,
        "kind": "registry-consumer-verification",
        "consumer": str(consumer),
        "release_version": projection["version"],
        "source_revision": projection["revision"],
        "target": args.target,
        "command": command,
        "projection_sha256": hashlib.sha256(projection_bytes).hexdigest(),
        "archive_manifest_sha256": hashlib.sha256(archive_bytes).hexdigest(),
        "cargo_lock_sha256": hashlib.sha256(lock_bytes).hexdigest(),
        "cargo_metadata_sha256": hashlib.sha256(metadata_bytes).hexdigest(),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checked_packages": checked,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
