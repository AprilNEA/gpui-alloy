# GPUI Alloy maintenance

Use the validated snapshot [gpui-alloy/20261003.2](https://github.com/AprilNEA/gpui-alloy/tree/gpui-alloy/20261003.2), which identifies S `9d59ea617d75d02e4645eefd22844235431138c8`. Pin that full commit SHA in dependencies and exports. The `main` branch also carries later documentation commits and acceptance records.

## Repository roles

| Repository | Responsibility |
| --- | --- |
| [zed-industries/zed](https://github.com/zed-industries/zed) | Upstream GPUI development and PR review. |
| [AprilNEA/zed](https://github.com/AprilNEA/zed) | Full source history, independent patch branches, and the `downstream/gpui` integration branch. |
| [AprilNEA/gpui-alloy](https://github.com/AprilNEA/gpui-alloy) | Standalone GPUI workspace, exports, current maintenance policy, and acceptance records on `main`. |
| [AprilNEA/gpui-alloy-archive](https://github.com/AprilNEA/gpui-alloy-archive) | The earlier full-history Alloy repository, original refs, signed tags, and validation evidence. |

The standalone repository has an independent Git history. Do not copy the full source Git database, old refs, or old tags into this repository. Do not make an upstream or source integration commit a parent of a standalone commit.

The archive entry point is [main at `3ec8404e11262fb038e15b583724e2a35809dfae`](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/ALLOY.md). Preserve that archive commit and every archived object. Keep current maintenance records here instead of adding new archive commits.

Old commit and tag references must use the archive URL. In particular, use `https://github.com/AprilNEA/gpui-alloy-archive.git` for an old Git dependency pinned to D. Reusing the old repository name prevents reliance on rename redirects. Existing local vendor files remain valid until the consumer imports another snapshot.

The source notices that link to this document remain valid. Keep those notices unchanged when moving the source between repositories.

## Source contract: U → D → S → V

| Symbol | Meaning | Current value |
| --- | --- | --- |
| U | Fixed upstream baseline in the full source repository. | `4c841aaf1c4fa613e89a5d77096523d0ff593b56` |
| D | Full source integration commit containing the downstream patches. | `d21987f81a013ec67945892506bcc6aae8a2db0f` |
| S | Independently versioned standalone commit projected from D. | `9d59ea617d75d02e4645eefd22844235431138c8` |
| V | Consumer commit that imports an export of S. | `3208e4fb8e751b6619e5b25997893618011b2809` |

U must be an ancestor of D in `AprilNEA/zed`. D → S is a source projection, not a Git ancestry relationship. S → V is a fixed Git tree export followed by a consumer import.

[ALLOY-SOURCE.json](ALLOY-SOURCE.json) identifies the source repository, U, D, and the original export record digest. The preserved [source export record](alloy-source/ALLOY-SNAPSHOT.json) has format 1 and SHA-256 `88a1781f7241d1f6a5f0f178a63230e0730085fce93c0f1049b66445a076615a`.

Preserve these six provenance files in S and in every consumer export:

- `ALLOY-SOURCE.json`
- `alloy-source/ALLOY-SNAPSHOT.json`
- `alloy-source/Cargo.toml`
- `alloy-source/Cargo.lock`
- `alloy-source/.cargo/config.toml`
- `alloy-source/rust-toolchain.toml`

The four source control files and the original export record retain their original bytes. They describe D. The active standalone root configuration describes S.

An independent comparison against the actual fixed D must establish the D → S source relationship. A consistent JSON record alone does not prove that relationship. Record the path set, content, file modes, symlink targets, and permitted root configuration changes.

GPUI production files must match the recorded D projection. If a production file needs a change, make the change in a source topic branch first. Integrate a new D before importing the change into S. Do not maintain another implementation directly in the standalone repository or consumer vendor directory.

S cannot contain its own commit SHA. V cannot contain its own commit SHA. Record exact S, exact V, validation logs, and publication results in a later documentation commit. The snapshot tag must continue to identify the tested S, even when `main` advances to that documentation commit.

## Branch, record, and signing policy

Each potential upstream PR must have one independent topic branch in `AprilNEA/zed`. Each branch must address one problem. Keep Alloy tools, root maintenance documents, and unrelated patches out of upstream topic branches.

Use a stable `GPUI-NNN` identifier for each patch. Record the topic head, original source, base, dependencies, integrated commit, PR, checks, and retirement condition. Preserve the identifier across rebases. If a topic splits into independent problems, assign new identifiers and record the relationship.

Use `GPUI-Patch: GPUI-NNN` trailers for new downstream topic commits. GPUI-005 has a historical `Patch-ID` trailer; preserve that history. Upstream submission messages may follow the upstream convention without internal trailers.

A dependent topic may use another topic as its base. Record that dependency explicitly. Do not assume upstream maintainers accept stacked PRs. Rebase or separate the submission after checking the current upstream requirements.

Keep `local/*` branches for local-only changes or adaptations of existing PRs. A local adaptation does not update the original PR branch. Preserve the original PR branch until a deliberate PR update is ready.

Sign new authored commits and annotated snapshot or archive tags. Preserve upstream commits, authorship, existing commit objects, and existing tag objects. Do not re-sign imported history. Before rewriting a working topic branch, preserve its old head with an archive reference and record the mapping.

Published snapshot tags are immutable. Never move a published tag to another commit or replace its tag object. If a correction is required, create a new snapshot number. The one-time signing conversion before the first remote publication does not authorize later history rewrites.

Create a release tag only after both validation layers pass: the exact GPUI revision and the consumer using its exact export. Verify the commit and tag signatures before publication. Confirm the remote object IDs after publication.

Keep licenses and attribution. Every modified Apache-2.0 file must carry a prominent modification notice. A repository-level notice alone is insufficient. Add new notices in the downstream integration when needed; keep existing notices through export.

## Current patch ledger

AprilNEA maintains all eleven patches. D contains all eleven topics. The following signed source branches are published in `AprilNEA/zed`. The final acceptance record links the remote verification evidence.

Unless a dependency is listed, each topic is based on U. GPUI-005 does not depend on GPUI-003. GPUI-010 contains the native popup adaptation and a later hidden-popup lifecycle fix.

| Patch | Source branch | Signed topic head | Dependency |
| --- | --- | --- | --- |
| GPUI-001 | `fix/gpui-cancel-pending-activation` | `9710df14519e1fedee1bdd8d16d57e712bcfb23c` | None. |
| GPUI-002 | `fix/gpui-interceptor-propagation` | `98c107d7bcc00df80a64ca68385aaf332943a99a` | None. |
| GPUI-003 | `test/gpui-accessibility-window` | `0f31f3c56aa6cad679d2de3c36ec838d09610ea9` | None. |
| GPUI-004 | `fix/gpui-spring-clock` | `a1ab296fcd88f01900cc616d2b934564c95bf8c3` | None. |
| GPUI-005 | `feat/gpui-inert` | `d09c26a6bf798eccc23e277450e1e8614f088a50` | None. |
| GPUI-006 | `feat/gpui-autoscroll-on-focus` | `445e4f9af7b6da4b3dcd52db4e0374a7a8a9942d` | GPUI-005. |
| GPUI-007 | `feat/gpui-ordered-backdrop` | `1f55d0eaf4b55a88316ee1b4fb30bdb9a564e5d0` | None. |
| GPUI-008 | `feat/gpui-continuous-quad` | `91f103447160b013c67e74f60204f1dadd039b74` | GPUI-007. |
| GPUI-009 | `local/gpui-inactive-clear` | `271ec2547b5f81740cd1f1855ec647e50b98a852` | GPUI-008, including GPUI-007. |
| GPUI-010 | `local/gpui-010-native-popup` | `459b3648bf99f6cc5cd149a6d3e695bb476f3fec` | None. |
| GPUI-011 | `local/gpui-011-popup-decorations` | `02c9bcf88b50768302b3ba95ca1cc8f52d345576` | None. |

The full source integration branch is `downstream/gpui` at D. The [archived signing map](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/alloy-validation/20261003/signing-map.json) maps original topic commits and integration commits to their signed objects.

| Patch | Behavior | Upstream route | Regression source |
| --- | --- | --- | --- |
| GPUI-001 | Cancel pending keyboard and pointer activation when click handlers disappear. | One fix PR; not submitted. | [div tests](crates/gpui/src/elements/div.rs). |
| GPUI-002 | Honor interceptor propagation before raw capture and bubble handlers. | One fix PR; not submitted. | [key dispatch tests](crates/gpui/src/key_dispatch.rs). |
| GPUI-003 | Expose test-window accessibility actions and activation. | One test-support PR; not submitted. | [test window](crates/gpui/src/platform/test/window.rs). |
| GPUI-004 | Use the scheduler clock for Spring animation. | One fix PR; not submitted. | [animation tests](crates/gpui/src/elements/animation.rs). |
| GPUI-005 | Preserve painting while excluding an inert subtree from input, focus, platform text input, and accessibility. | Discuss the API before a PR. | [inert tests](crates/gpui/src/elements/inert.rs), [input tests](crates/gpui/src/input.rs). |
| GPUI-006 | Reveal focused descendants with scoped, nested scroll offsets. | Discuss the API and GPUI-005 dependency before a PR. | [focus scrolling tests](crates/gpui/src/elements/div/scroll_focus_tests.rs). |
| GPUI-007 | Preserve backdrop ordering and render backdrop effects in Metal. | Discuss the platform contract and cost before a PR. | [scene tests](crates/gpui/tests/ordered_backdrop.rs), [backdrop](crates/gpui_apple/tests/backdrop.rs), [numeric](crates/gpui_apple/tests/numeric_reference.rs), [optical](crates/gpui_apple/tests/optical_reference.rs). |
| GPUI-008 | Render continuous rounded quads. | Discuss the drawing API and GPUI-007 dependency before a PR. | [continuous corners](crates/gpui_apple/tests/continuous_corners.rs). |
| GPUI-009 | Render inactive Clear with public ColorSync conversion. | Local-only. | [Clear](crates/gpui_apple/tests/clear.rs), [color management](crates/gpui_apple/tests/color_management.rs). |
| GPUI-010 | Add native anchored popups and correct hidden-popup lifecycle handling. | Existing [PR #64353](https://github.com/zed-industries/zed/pull/64353); the local lifecycle fix has not updated that PR. | [native popup](crates/gpui_macos/tests/native_popup.rs), [popup example](crates/gpui/examples/popup.rs). |
| GPUI-011 | Remove native decoration from untitled popup windows. | Existing [PR #64430](https://github.com/zed-industries/zed/pull/64430). | [popup decorations](crates/gpui_macos/tests/popup_decorations.rs). |

Both existing PRs were open at the 2026-10-03 source audit. Recheck their current base, review, and CI status before an update. The migration must preserve these original PR refs:

| Patch | Original branch in `AprilNEA/zed` | Original PR head |
| --- | --- | --- |
| GPUI-010 | `feat/macos-anchored-popup` | `619d4b2b3da3040e61c027a394aa5417123e92d0` |
| GPUI-011 | `fix/macos-popup-decorations` | `22df6ff9402b46943d5948e767b4c7ad493d69c3` |

The original creation base for both PRs is `70a74b8725fa39a4aa81eab4479f9055aa0d7078`. The GPUI-010 migration used the later PR base `6872711ff860c18e3d44a0171105273b6717ee15` to calculate its adaptation. Do not substitute that later base for the creation base.

The [fixed archive ledger](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/ALLOY.md) retains original Cupertino source commits, integration mappings, and migration decisions. The [topic check record](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/alloy-validation/20261003/topic-checks.md) retains the original commands. Those checks describe source topics, not the new standalone S.

## Standalone workspace projection

S contains 26 complete crate directories, `assets/fonts`, and the root licenses. The source audit compared 430 production, resource, and license entries against D. All bytes and Git modes matched, including 27 symlinks. No selected file was missing or extra.

The original export inventory contains 436 entries. That inventory also includes the generated root manifest and README, plus four preserved source controls. Keep the original inventory intact. Record standalone root changes separately.

The standalone workspace preserves the source resolver, workspace package values, workspace lints, and 147 inherited dependency definitions. The root configuration has these deliberate changes:

- Limit workspace members to the 26 required crates. Keep `tooling/perf` because `util_macros` requires that crate.
- Keep only the four reachable crates.io patches listed below. Fix `calloop` to the commit already selected by the original lockfile.
- Keep the base development profile, its build override, and the base release profile. Omit Zed package overrides and the custom `dbg` and `release-fast` profiles.
- Keep Rust `1.98.1`, the minimal toolchain profile, rustfmt, and Clippy. Omit editor components and additional compilation targets.
- Keep shared Rust flags, `tokio_unstable`, Windows `windows_slim_errors`, and `MACOSX_DEPLOYMENT_TARGET = 10.15.7`.
- Omit Zed command aliases, LiveKit static CRT flags, and the Linux libwebrtc linker setting.
- Keep [rustfmt.toml](rustfmt.toml), [clippy.toml](clippy.toml), [ruff.toml](ruff.toml), and the existing check scripts. The Clippy script has no shear, typo, or protobuf checks.

| Root patch | Resolved version | Fixed Git commit |
| --- | --- | --- |
| `async-process` | `2.5.0` | `0b6d6713570af61806e1e5cb40e0f757cb93fd9d` |
| `async-task` | `4.7.1` | `b4486cd71e4e94fbda54ce6302444de14f4d190e` |
| `calloop` | `0.14.3` | `eb6b4fd17b9af5ecc226546bdd04185391b3e265` |
| `windows-capture` | `1.4.3` | `f0d6c1b6691db75461b732f6d5ff56eed002eeb9` |

The standalone lockfile retains 874 of the original 1,824 packages. No retained version, registry checksum, or Git commit changed. The only source-string change makes the existing `calloop` revision explicit. The smaller workspace removes 65 dependency edges from 40 retained packages and adds no edges. This is dependency pruning, not an identical full dependency graph.

The audited root `Cargo.lock` has SHA-256 `f1b9fa1c2dd5ceabd9d3ff9a3e2b7aa8357d9b8ea25de9dd92126452af8b5547`. The preserved source lockfile has SHA-256 `9ff58114305da0bf66438fe64c571a64bfd65c05422960a20d4f2b1f20ff0e20`.

The evidence directory is [docs/validation/20261003-standalone](docs/validation/20261003-standalone/). The [projection report](docs/validation/20261003-standalone/source-projection-review.md) and [structured comparison](docs/validation/20261003-standalone/source-projection-review.json) bind the source comparison to exact S. The `fixed_git_verification` record reads committed tree and blob objects. The record confirms that S has no parents, that the selected source matches D, and that the audited root configuration matches S.

## Export a fixed standalone commit

Use Python 3.12 or later and Git. Use the exporter version stored in the selected S. Pass a full 40-character commit SHA to `--revision`; do not pass a moving branch or tag name.

```sh
python3 script/gpui_snapshot.py export \
  --repo /path/to/gpui-alloy \
  --revision FULL_S_SHA \
  --snapshot /new/vendor
```

The destination must not exist. Review the generated snapshot before replacing a consumer vendor directory. Keep build output outside the snapshot.

The standalone CLI accepts `--revision` without `--upstream`. The exporter reads committed Git tree and blob objects. Dirty worktree files, Git replacements, and local archive attributes do not change the export.

The exporter includes all required path dependencies, including optional, build, development, and target dependencies. The package-path mapping must match the preserved source export. Complete crate directories, fonts, licenses, and provenance files retain their Git modes and safe relative symlinks.

The generated consumer workspace keeps the resolver, workspace package values, used inherited dependencies, and lints. The standalone root patches, profiles, lockfile, Cargo configuration, and toolchain are not automatically applied to the consumer. The consumer root and lockfile control external dependency resolution. Matching source files do not imply identical builds.

The generated format 2 `ALLOY-SNAPSHOT.json` identifies S, its source record, the exporter digest, package paths, and file inventory. The inventory excludes the outer record itself.

## Verify the consumer

```sh
python3 script/gpui_snapshot.py verify-consumer \
  --repo /path/to/gpui-alloy \
  --revision FULL_S_SHA \
  --snapshot /path/to/consumer/vendor \
  --consumer /path/to/consumer \
  --target aarch64-apple-darwin
```

First, the checker reconstructs the expected export from S. The checker compares every file, mode, symlink target, and export record. Missing, extra, or modified files fail verification.

Next, the checker runs fresh `cargo metadata --format-version 1 --locked --all-features` in the consumer. `--target` selects Cargo's `--filter-platform`; omit the option to inspect all target dependencies. Saved metadata is not accepted as current evidence.

GPUI must be reachable from the consumer workspace. Every reachable exported package name must resolve to one package identity, with no registry or Git source, at its exact canonical vendor manifest path. This strict collision policy also applies to shared names such as `util`, `path`, and `collections`. A target-filtered graph need not reach every exported crate.

The source check detects stale vendor files, mixed GPUI copies, changed files, and wrong dependency paths. The source check does not replace compilation or behavior tests. Run the consumer's formatter, linter, and relevant tests after the source check.

Old format 1 snapshots require the archived exporter and a full source checkout containing U and D. Do not point an old source check at the new standalone Git repository. The old snapshot `gpui-alloy/20261003.1` remains in the archive with tag object `87e974154254c5e92ef3e37a0612ea9e3db0f34f`, which resolves to D.

## Synchronization and release procedure

1. Select a full upstream commit U in the source repository. Record upstream changes that affect retained patches.
2. Compare each patch with U. If U provides the required behavior, stop applying the duplicate patch and run its regression checks. Do not revert equivalent upstream behavior merely because a PR merged.
3. Preserve old topic heads before a rewrite. Update each affected topic on its independent branch, with explicit bases and dependencies.
4. Run relevant topic checks. Record failures and platform limits without weakening assertions.
5. Integrate the selected topics into a new D on `downstream/gpui`. Preserve authorship, patch mappings, licenses, and required per-file modification notices.
6. Run the source integration checks. Preserve a reproducible source export from fixed U and D using the source exporter recorded with that integration.
7. Import the selected crate and resource projection into the standalone repository. Update `ALLOY-SOURCE.json` and the original source export record together.
8. Compare the imported payload directly with D. Record permitted root configuration changes and dependency identities separately.
9. Run the standalone checks below. Create signed S with the reviewed source, configuration, tools, and documents.
10. Export exact S into a new directory. Verify the consumer source paths and run the consumer checks against that export.
11. Commit only the intended consumer import as signed V. Record U, D, S, export digests, commands, and results in the import documentation.
12. After both validation layers pass, create a signed annotated snapshot tag that identifies S. Use a new `gpui-alloy/YYYYMMDD.N` name.
13. Publish only the intended source refs, standalone refs, tag, and consumer ref. Verify remote object IDs, signatures, and repository visibility.
14. Add exact S, V, tag object, logs, and publication results in a later documentation commit on `main`.

If S changes after export or validation, repeat the affected checks and regenerate the export. Do not transfer a passing result to a different commit without evidence that binds the tested tree and configuration.

If the consumer worktree contains unrelated edits, validate clean V separately before creating the release tag. Preserve the unrelated edits and their index state.

For rollback, select a previously validated immutable S and re-import its export in a new consumer commit. Preserve the failed release record. Do not move an old tag or erase published history.

Retire GPUI-001 through GPUI-006 when a new U supplies their required behavior. Submit GPUI-007 and GPUI-008 only after agreement on their platform contracts. Reassess GPUI-009 when Cupertino no longer needs the effect or upstream supplies an equivalent supported capability. Retire GPUI-010 and GPUI-011 only when the new U includes all required local behavior, including the later lifecycle correction.

## Validation commands and limits

Run the existing macOS suite from the standalone root:

```sh
./script/check
```

[script/check](script/check) runs workspace formatting, workspace Clippy, the four GPUI library suites, scene tests, Metal tests, native window harnesses, and the popup example. The final continuous-corner invocation also checks compiled Metal shaders without `runtime_shaders`. The native harnesses require a macOS desktop session and Apple Metal.

The library suite uses one test thread. A historical parallel profiler failure remains in the [archive failure log](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/alloy-validation/20261003/gpui-parallel-failure.txt). Do not describe the default parallel suite as passing.

For snapshot tool changes, run:

```sh
ruff format --check script/gpui_snapshot.py script/test_gpui_snapshot.py
ruff check script/gpui_snapshot.py script/test_gpui_snapshot.py
python3 -B -m unittest discover -s script -p test_gpui_snapshot.py -v
```

The original signed D passed 491 library tests, 5 scene tests, 17 Metal tests, 1 popup example test, 3 compiled-shader tests, and 2 native harnesses. The [signed source log](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/alloy-validation/20261003/gpui-signed.txt) records those results. The [signed consumer log](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/alloy-validation/20261003/consumer-signed.txt) records the earlier Cupertino import. Those results are historical evidence, not acceptance of S.

The validated source environment was Rust and Cargo `1.98.1`, `aarch64-apple-darwin`, macOS `26.4`, and Xcode `26.6`. Linux, Windows, and Web source remain in the projection. This migration does not establish compilation or behavior on those platforms.

The downstream rendering effects are limited to supported opaque SDR macOS window content. Inactive Clear requires an Apple GPU, Metal 3.1, and a supported parametric RGB profile through public ColorSync. The WGPU path rejects unsupported materials.

No acceptance claim covers HDR/EDR, active Clear, transparent desktop sampling, mixed-DPI multi-monitor behavior, live cross-display migration, or complete VoiceOver and IME behavior. The hidden-popup regression exercises application deactivation. The external mouse callback uses the same state condition but has no separate synthesized external-application event check.

## 20261003.2 acceptance record

The standalone checks passed for the source and configuration committed in S. `./script/check` completed with exit status 0. The suite passed 517 tests and 2 native harnesses: 491 library tests, 5 scene tests, 17 Metal tests, 1 popup example test, and 3 compiled-shader tests. Workspace formatting and Clippy passed. Ruff and all 4 Python regression tests passed.

The clean consumer checkout at V passed source verification for 18 resolved packages on `aarch64-apple-darwin`. Consumer formatting, Clippy, and all 64 tests passed. The original consumer worktree also completed `devenv test` with exit status 0. The worktree log reports completion without a test count; the clean checkout log provides the 64-test result.

The consumer import preserved unrelated staged work. The non-vendor staged diff retained SHA-256 `866e25b09971ab69601bd8e6bf2a2fc8ce76bf4524a41e82f64c0b22d1e17619`. Existing Cocoa dependency deprecation warnings and the `block` future-incompatibility warning remain in the logs. No new lint suppression was added.

| Record | Fixed value or evidence |
| --- | --- |
| Source U | `4c841aaf1c4fa613e89a5d77096523d0ff593b56`. |
| Source D | `d21987f81a013ec67945892506bcc6aae8a2db0f`; tree `fbb778e445fcd9d4d9bc5d6150fa570f6a743485`. |
| Standalone S | `9d59ea617d75d02e4645eefd22844235431138c8`; tree `329c974731e4f75fa6f45868bbf0fdb1c59976a5`. |
| Snapshot tag | `gpui-alloy/20261003.2`; annotated tag object `ac8aa77ee84b5ff5482ac6302dd58e9ad72ca8bc`, which resolves to S. |
| Consumer V | `3208e4fb8e751b6619e5b25997893618011b2809` in `AprilNEA/gpui-cupertino`. |
| Previous consumer import | `ea9cc093403f45a26f32d0ae415007fef95e3b09`. |
| D → S projection | Passed against fixed Git objects. [Report](docs/validation/20261003-standalone/source-projection-review.md), [JSON](docs/validation/20261003-standalone/source-projection-review.json). |
| Standalone checks | Formatting, Clippy, 517 tests, and 2 native harnesses passed. [Log](docs/validation/20261003-standalone/standalone-check.log). |
| Python checks | Ruff and 4 regression tests passed. [Log](docs/validation/20261003-standalone/python-check.log). |
| Consumer source check | Fixed S and 18 resolved packages verified. [Log](docs/validation/20261003-standalone/consumer-source.log). |
| Clean V checks | Source verification, formatting, Clippy, and 64 tests passed. [Log](docs/validation/20261003-standalone/consumer-clean-check.log). |
| Original consumer worktree | `devenv test` completed with exit status 0. [Log](docs/validation/20261003-standalone/consumer-check.log). |
| Signatures and remote publication | Object IDs, signature results, repository state, and published refs are recorded in [publication.json](docs/validation/20261003-standalone/publication.json). |

The format 2 consumer export contains 26 packages and 438 inventory entries. The outer record excludes itself from that inventory. The export record SHA-256 is `e1cf291d98001e41b5cac87c8d81f832ac533b504a0cf33ca9b32265764ce34b`. The exporter SHA-256 is `9a82458aa24bedaaf9f592f57d2f956e612dfab1dc31265190e7624bebb69d45`.

The source fork now has the eleven topic branches and `downstream/gpui` at the recorded heads. The source fork's existing `main` and two PR branches remain unchanged. The renamed archive has `archived = true`; all original 15 branch heads and 19 annotated tag objects remain unchanged.

The new standalone repository is public. Its initial published `main` identifies S, and its published snapshot tag matches the tag object above. GitHub Actions is disabled. Consumer V is published on `AprilNEA/gpui-cupertino:feat/component-library`. GitHub reports valid signatures for S, V, and the snapshot tag. The source projection audit confirms that no standalone ref reaches U or D. Later documentation commits retain that independent history and do not move the snapshot tag.

The earlier publication evidence remains at the [fixed archive publication record](https://github.com/AprilNEA/gpui-alloy-archive/blob/3ec8404e11262fb038e15b583724e2a35809dfae/alloy-validation/20261003/publication.json). Preserve that record independently of this release.

The standalone checkout is `/Users/Xuan/Developer/AprilNEA/gpui-alloy`. The full-history checkout is `/Users/Xuan/Developer/AprilNEA/gpui-alloy-archive`. All six linked source worktrees retain their commit identities after repair. See the [local layout record](docs/validation/20261003-standalone/local-layout.json).
