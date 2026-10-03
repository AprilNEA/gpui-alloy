# GPUI Alloy maintenance

- Keep GPUI production sources identical to the recorded source integration commit.
- Make GPUI changes on independent topic branches in `AprilNEA/zed`.
- Update `ALLOY-SOURCE.json` and the source import record together.
- Keep the source repository and the standalone repository as separate Git histories.
- Preserve published tags and archived signatures.
- Keep source attribution, licenses, file modes, and symbolic links.
- Run `cargo fmt --all -- --check` before committing Rust changes.
- Run `./script/clippy` for Rust lint checks.
- Run `./script/check` for the macOS validation suite.
- Run Ruff and the Python tool tests before committing Python changes.
- Keep registry packaging changes in generated publication directories and record each transformation.
- Keep build output outside exported consumer snapshots.
- Record each validated standalone revision and consumer import in `ALLOY.md`.
- Keep the root README review marker until the human author removes the marker.
- Do not include unrelated consumer changes in an import commit.
