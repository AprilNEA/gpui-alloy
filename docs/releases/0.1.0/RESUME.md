# Resume GPUI Alloy 0.1.0

All 31 release packages are published. Registry consumer acceptance and the release tag remain pending. The confirmed package list and current count are stored in [publication.json](publication.json). Their downloaded archives and registry index checksums match [archives.json](archives.json). The remaining package set is the complete projection minus those confirmed packages.

Crates.io permits an initial burst of five new crates and then restores one new-crate allowance every ten minutes. Follow the retry time in each server response. See the [official rate-limit documentation source](https://github.com/rust-lang/crates.io/blob/main/svelte/src/routes/docs/rate-limits/+page.svelte).

The user approved automatic continuation. The active chat schedule `gpui-alloy-cupertino` runs every ten minutes and publishes at most one new crate per run. After all 31 packages are verified in crates.io, the schedule completes Cupertino registry acceptance and stops. Keep the computer on and the Codex desktop app running for the local schedule.

## Fixed local inputs

| Input | Path |
| --- | --- |
| Alloy repository | `/Users/Xuan/Developer/AprilNEA/gpui-alloy` |
| Candidate workspace | `/private/tmp/alloy-registry-packager/staging-process-31` |
| Frozen archives and lockfile | `/private/tmp/gpui-alloy-0.1.0-frozen` |
| Cargo target directory | `/private/tmp/gpui-alloy-registry-target` |
| Full-family registry probe | `/private/tmp/alloy-complete-family-probe-0.1.0` |
| Cupertino integration worktree | `/Users/Xuan/.codex/worktrees/gpui-alloy-registry/gpui-cupertino` |
| Cupertino integration branch | `codex/gpui-alloy-registry` |
| Existing Cargo environment | `devenv shell` from `/Users/Xuan/Developer/AprilNEA/gpui-cupertino` |

The packaging commit is `de934a6a08b82e6c85a86dd8f156d82742c583ce`. The frozen archive record commit is `1b00d42433dda5ca6a540a6a6cc6aecb668a5b5d`. The source revision, projection, external source revisions, workspace lockfile, and hashes are stored in this release directory. Temporary directories must remain available until publication finishes. If a directory is missing, reconstruct the fixed candidate from the recorded inputs and require identical archive hashes before continuing.

## Continue publication

1. Verify each confirmed package against its frozen checksum. Use official Cargo registry queries and downloads. Stop if a registry checksum differs.
2. Select the first unpublished package in `projection.json`'s `publish_order`. Confirm that each Alloy dependency is already published.
3. Wait until the server permits another publish. Publish at most one new package per ten-minute scheduled run.
4. Run `cargo package --manifest-path CANDIDATE/Cargo.toml --package NAME --locked --registry crates-io`. Use the recorded Cargo 1.98.1 environment and target directory.
5. Compare the generated archive with `archives.json`. Stop if the archive differs. Keep the frozen artifacts unchanged.
6. Run `cargo publish --manifest-path CANDIDATE/Cargo.toml --package NAME --locked --registry crates-io`. Keep Cargo's package verification enabled.
7. Query the published version with `cargo info NAME@0.1.0 --registry crates-io`. Compare the downloaded archive and registry index checksum with the frozen checksum.
8. Update `publication.json` and save the command log. After a timeout, confirm registry state before another upload attempt.

The initial workspace publish uploaded five packages and then received HTTP 429. The separate `gpui-alloy-macros` upload succeeded after the stated retry time. The first error's remaining-package note omits the failed package; derive the remaining set from the release manifest instead.

## Complete acceptance

1. After all 31 packages are published, run the full-family probe with `devenv shell -- sh /private/tmp/alloy-complete-family-probe-0.1.0/verify.sh`. Preserve the 31-package registry identity and checksum report.
2. Use Cargo to replace Cupertino's temporary path dependencies with exact registry aliases for `gpui-alloy`, `gpui-alloy-apple`, and `gpui-alloy-platform`. Preserve the normal and development `gpui` aliases, `test-support`, and `font-kit` features.
3. Run `script/gpui_registry_consumer.py` against the Cupertino worktree, the projection, and the frozen archive record.
4. Run Cupertino's formatter, full Clippy check, and full test suite against the registry graph. The generated-package preflight passed 119 tests; those results do not replace registry acceptance.
5. Update the pending consumer documents. Create signed commits and verify signatures with the existing 1Password SSH key. Recheck the original Cupertino branch before integrating the completed worktree changes. Preserve unrelated user work.
6. Record registry acceptance and create the signed immutable `v0.1.0` tag. Keep existing snapshot tags unchanged. Leave Git pushing to the user under the current user instructions.

The 1Password SSH signing agent recovered after the user unlocked 1Password. The pending wgpu publication record and blocker evidence were committed as `8969b0064c9945252eb2eab74b6ba783e3d02ae4`. The signature was verified against the configured public key. See `record_commit` in [publication.json](publication.json) for the verification log and preserved failure history. The release contains 31 verified packages. The fixed release inputs were subsequently recovered and verified as recorded below.

Previous signature verification used the configured public key in a temporary `allowed_signers` file. No global trust configuration or new key is required.

## Recovered local release inputs

At the 2026-10-04 09:42 UTC check, the candidate workspace, frozen archive directory, Cargo target directory, and full-family registry probe were absent. An escalated filesystem check confirmed the missing directories. The Cupertino integration worktree still exists. No package was published during this check. See `local_inputs` in [publication.json](publication.json) for the path observations and evidence log.

The user authorized reconstruction. The fixed Smol Git commit, candidate, all 31 frozen archives, release lockfile, and full-family probe are restored. Every archive SHA-256 matches the original record. The projection and workspace lockfile hashes are identical. Cargo 1.98.1 verified the five rebuilt packages with verification enabled; 26 archives were recovered from matching Cargo cache copies. See the [recovery report](recovery-20261004/recovery.json) and [package verification log](recovery-20261004/package-five.log). Both the local input blocker and the signature blocker are resolved.

A persistent backup is stored at `/Users/Xuan/.local/share/gpui-alloy/releases/0.1.0`. The backup contains `frozen/`, `candidate.tar.gz`, and `probe/`. See the [backup record](recovery-20261004/backup.json). If temporary inputs disappear again, restore from this backup and require the original archive, projection, and lockfile hashes before publishing. Preserve published versions and tags.

## Current Cupertino integration hold

Current Cupertino includes GPUI-012 from standalone source `1a77576c8ef715f2ceaece8af18017cb360434c9`. GPUI-012 adds macOS native accessibility focus forwarding. The frozen 0.1.0 source `9d59ea617d75d02e4645eefd22844235431138c8` does not include this fix. Switching the current consumer to 0.1.0 would regress native focus behavior. The GPUI-012 native harness is outside the ordinary workspace tests. The earlier 119-test preflight cannot establish compatibility with GPUI-012.

Complete the immutable 0.1.0 publication and isolated registry acceptance. Preserve the current Cupertino vendor, its later commits, and all uncommitted user changes. Do not integrate the older registry candidate into the current consumer. Validate a later release containing GPUI-012 before the current consumer switches to registry dependencies. Record the final integration separately. See `consumer_integration` in [publication.json](publication.json).
