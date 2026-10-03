> [!IMPORTANT]
> Remove this line to confirm you've reviewed this PR before submitting.

# GPUI Alloy

A maintained GPUI source distribution with tracked downstream patches. The repository contains GPUI, its required crates, resources, tests, and maintenance tools. Crate names and source paths retain their upstream form.

## Use

Pin a validated Alloy commit and select the matching platform crate:

```toml
[dependencies]
gpui = { git = "https://github.com/AprilNEA/gpui-alloy", rev = "<validated-commit>" }
gpui_platform = { git = "https://github.com/AprilNEA/gpui-alloy", rev = "<same-validated-commit>" }
```

See [ALLOY.md](ALLOY.md) for validated revisions, patch branches, source exports, checks, and platform limits. See the [GPUI README](crates/gpui/README.md) for framework usage.

## Source history

Upstream contribution branches and the full source integration live in [AprilNEA/zed](https://github.com/AprilNEA/zed). This repository has an independent history. [ALLOY-SOURCE.json](ALLOY-SOURCE.json) records its Zed baseline and integrated source commit.

The earlier full Zed repository, signed histories, and `gpui-alloy/20261003.1` snapshot remain in [gpui-alloy-archive](https://github.com/AprilNEA/gpui-alloy-archive). Old commit and tag URLs must use that archive repository.

Each crate retains its upstream license. Keep the crate license files and source notices when redistributing the source.
