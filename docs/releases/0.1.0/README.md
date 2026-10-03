# GPUI Alloy 0.1.0

**Release status: partially published (22/31 packages).** Crates.io has accepted the frozen packages listed in the publication record. The new-crate rate limit controls the remaining uploads. Registry consumer acceptance and the release tag remain pending. See the [publication record](publication.json) and [continuation instructions](RESUME.md).

| Identity | Fixed commit |
| --- | --- |
| Upstream Zed baseline U | `4c841aaf1c4fa613e89a5d77096523d0ff593b56` |
| Patched source integration D | `d21987f81a013ec67945892506bcc6aae8a2db0f` |
| Standalone source S | `9d59ea617d75d02e4645eefd22844235431138c8` |
| Packaging commit | `de934a6a08b82e6c85a86dd8f156d82742c583ce` |

The [maintenance ledger](../../../ALLOY.md) records the eleven source patches and the U → D → S relationship. This release starts Alloy's independent `0.1.*` compatibility series. The packaging projection preserves the runtime implementation from S; it changes package identities and dependency metadata, materializes package-external license links, and adapts the Apple build script to read five copied GPUI shader inputs inside its own archive. Original library names and public features remain available. Consumers must resolve the Alloy family together; registry and vendored GPUI types have distinct package identities.

The [projection](projection.json) defines all 31 package names, manifests, source hashes, transformations, and dependency order. The family consists of 26 standalone crates and five external source packages, all at `0.1.0`. Dependencies between family packages use `=0.1.0`. Package manifests omit development dependencies and test, example, and benchmark targets. Source tests remain in the source repository.

| Preserved external package | Reason |
| --- | --- |
| `gpui-alloy-async-tar` | Retain the fixed fork's length-based PAX parsing and `http_client/github-download`. |
| `gpui-alloy-reqwest` | Retain `system-configuration 0.8.0` and failed proxy-store initialization handling. |
| `gpui-alloy-font-kit` | Retain the fixed manifest's `dirs 6.0` dependency. |
| `gpui-alloy-smol` → `gpui-alloy-async-process` | Retain the macOS `adopt_raw_pid` API used by `util` through `smol::process`. |

Exact external Git commits and registry comparisons are recorded in the [dependency audit](dependency-audit.json) and [process dependency audit](process-dependency-audit.json). The latter verifies the Smol registry archive against its published Git commit. Registry substitutions retain `proptest 1.10.0` with `attr-macro`, `zed-scap 0.0.8-zed`, `zed-xim 0.4.0-zed`, and `wasm_thread 0.3.3`.

No root `[patch.crates-io]` table is propagated. The required `async-process` implementation is included through the namespaced Smol dependency. Root Git patches for `async-task`, `calloop`, and `windows-capture` are omitted. Registry consumers use normal registry resolution for those dependencies. This release does not claim an identical external dependency graph to the standalone workspace.

| Validation or publication step | Status |
| --- | --- |
| Exact S source validation | Previously passed: 517 tests and two native harnesses; see the [source validation record](../../validation/20261003-standalone/). |
| Packaging and consumer-verifier Python tests | Passed: 15 tests; see [the log](python-check.log). |
| Independent archive inspection | Passed for all 31 candidate archives: package identities, exact family dependencies, provenance, licenses, runtime file completeness, and source bytes. See the [locked archive audit](archive-audit.json) and [file digests](archive-files.json). |
| Full Cargo workspace publish dry-run | Passed for all 31 packages; see [the dry-run log](preflight-2.log). The [first candidate](preflight-1.log) exposed the required `adopt_raw_pid` API; the current candidate preserves the two-package process chain. |
| Clean consumer against the generated package set | Passed: 119 tests, formatting, Clippy, and 19 reachable Alloy identities; see the [result](generated-consumer.json) and [log](generated-consumer.log). |
| Locked package verification and frozen archives | Passed for all 31 packages; see [the final package log](preflight-3.log), [archive checksums](archives.json), and [release lockfile](registry.Cargo.lock). |
| Crates.io uploads and checksum verification | Published packages are independently checksum-verified; see [publication.json](publication.json). All 31 publication archives reproduced the frozen hashes before the first upload; see the [pre-upload check](pre-upload-check.json). |
| Clean Cupertino consumer resolving only crates.io Alloy packages | Pending. |
| Consumer integration commit | Pending. |
| Signed `v0.1.0` tag, signature verification, and remote object IDs | Pending. |

Validation scope is macOS on `aarch64-apple-darwin`. This record does not establish Linux, Windows, FreeBSD, or Web compilation or runtime support. Historical vendor consumer checks do not establish registry consumer acceptance.

The package checks report upstream `cocoa` deprecation warnings in `gpui-alloy-apple` and `gpui-alloy-macos` and a future-incompatibility warning for `block 0.1.6`. These warnings remain recorded limitations. The candidate does not claim warning-free builds or compatibility with a future compiler that rejects the warned code. No warning suppression or runtime rewrite is part of this packaging projection.

The [release lockfile](registry.Cargo.lock) has SHA-256 `d8cd328129b2fb34e3fe8da3fcdf033869c3df5401680be4dafdde934e34b6a4`. Cargo 1.98.1 generated the lockfile before the final `cargo package --workspace --locked --registry crates-io` validation. The [resolution comparison](lock-comparison.json) records the change from the earlier unlocked package checks: the workspace selects `unicode-properties 0.1.3`, with no additional external package identity or checksum change among common dependencies.
