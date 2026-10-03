> [!IMPORTANT]
> Remove this line to confirm you've reviewed this PR before submitting.

# GPUI Alloy

A maintained GPUI source distribution with tracked downstream patches. The repository contains GPUI, its required crates, resources, tests, and maintenance tools. Crate names and source paths retain their upstream form.

## Features & fixes

The pinned snapshot includes these changes relative to its recorded upstream baseline. Patch IDs link to the detailed maintenance ledger.

| Type | Change | Scope | Tracking |
| --- | --- | --- | --- |
| Fix | Cancel pending keyboard and pointer activation when click handlers disappear. | GPUI core | [GPUI-001](ALLOY.md#current-patch-ledger) |
| Fix | Respect interceptor propagation before raw capture and bubble handlers. | GPUI core | [GPUI-002](ALLOY.md#current-patch-ledger) |
| Test support | Expose accessibility actions and activation in test windows. | Test windows | [GPUI-003](ALLOY.md#current-patch-ledger) |
| Fix | Use the scheduler clock for Spring animation. | GPUI core | [GPUI-004](ALLOY.md#current-patch-ledger) |
| Feature | Keep `inert` subtrees painted while excluding input, focus, text input, and accessibility. | GPUI core | [GPUI-005](ALLOY.md#current-patch-ledger) |
| Feature | Scroll focused descendants into view, including nested scroll areas. | GPUI core | [GPUI-006](ALLOY.md#current-patch-ledger) |
| Feature | Preserve backdrop capture order and render backdrop effects. | macOS Metal | [GPUI-007](ALLOY.md#current-patch-ledger) |
| Feature | Render continuous rounded rectangles and borders. | macOS Metal | [GPUI-008](ALLOY.md#current-patch-ledger) |
| Feature | Render Inactive Clear with public ColorSync conversion. | macOS Metal; local-only | [GPUI-009](ALLOY.md#current-patch-ledger) |
| Feature / Fix | Add native anchored popups and fix hidden-popup lifecycle handling. | macOS | [GPUI-010](ALLOY.md#current-patch-ledger), [#64353](https://github.com/zed-industries/zed/pull/64353) |
| Fix | Remove native window decorations from untitled popups. | macOS | [GPUI-011](ALLOY.md#current-patch-ledger), [#64430](https://github.com/zed-industries/zed/pull/64430) |

GPUI-010's local lifecycle fix is not included in the linked upstream PR.

Validation covers macOS (`aarch64-apple-darwin`). The rendering additions target opaque SDR window content on macOS Metal. Inactive Clear additionally requires an Apple GPU, Metal 3.1, and a supported parametric RGB profile. See [validation scope](ALLOY.md#validation-commands-and-limits) for other platform and rendering limits.

## Use

Pin a validated Alloy commit and select the matching platform crate:

```toml
[dependencies]
gpui = { git = "https://github.com/AprilNEA/gpui-alloy", rev = "9d59ea617d75d02e4645eefd22844235431138c8" }
gpui_platform = { git = "https://github.com/AprilNEA/gpui-alloy", rev = "9d59ea617d75d02e4645eefd22844235431138c8" }
```

See [ALLOY.md](ALLOY.md) for validated revisions, patch branches, source exports, checks, and platform limits. See the [GPUI README](crates/gpui/README.md) for framework usage.

## Source history

Upstream contribution branches and the full source integration live in [AprilNEA/zed](https://github.com/AprilNEA/zed). This repository has an independent history. [ALLOY-SOURCE.json](ALLOY-SOURCE.json) records its Zed baseline and integrated source commit.

The earlier full Zed repository, signed histories, and `gpui-alloy/20261003.1` snapshot remain in [gpui-alloy-archive](https://github.com/AprilNEA/gpui-alloy-archive). Old commit and tag URLs must use that archive repository.

Each crate retains its upstream license. Keep the crate license files and source notices when redistributing the source.
