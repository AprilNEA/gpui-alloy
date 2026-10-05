# GPUI Alloy 0.1.1

This release adds GPUI-012 native macOS accessibility focus forwarding. Public Rust APIs and the minimum Rust version remain unchanged. The patch version follows the Alloy compatibility policy.

All 31 packages are published and checksum-verified. Source validation, full-family registry validation, native focus regression, and isolated Cupertino validation passed. Current Cupertino uses exact =0.1.1 registry dependencies. Formatting, strict Clippy, and all 123 tests passed.

The initial focus-paint failure disappeared after rebuilding Cupertino artifacts. Fresh registry builds also passed without source or assertion changes. The Tooltip focus test failed with both vendor and registry dependencies. Cupertino now defers focus notifications until the frame completes. The Tooltip regression passed with both dependency sources.

Preserve all published packages and existing tags. The user must push the signed commits and release tag.
