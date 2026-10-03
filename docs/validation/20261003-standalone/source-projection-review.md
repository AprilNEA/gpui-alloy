# D → 精简工作树源码与依赖审计

结论：在本次读取的候选工作树中，没有发现生产源码投影或依赖版本保留问题。检查仅读取固定 D、候选文件、Cargo.lock 和父任务生成的 metadata；没有执行 Cargo、构建或修改源码与锁文件。

## 固定对象与复核入口

- 完整源仓库：`/Users/Xuan/Developer/AprilNEA/gpui-alloy`。
- D：`d21987f81a013ec67945892506bcc6aae8a2db0f`。
- D tree：`fbb778e445fcd9d4d9bc5d6150fa570f6a743485`。
- 候选：`/tmp/gpui-alloy-standalone.n4rHPW/repo`。审计时尚未提交；本报告绑定文件摘要，不代表已验收最终 S。
- 原导出记录 SHA-256：`88a1781f7241d1f6a5f0f178a63230e0730085fce93c0f1049b66445a076615a`。
- 结构化结果：`source-projection-review.json`。包含逐文件 Git blob、SHA-256、mode、根配置值、依赖差异和 patch 解析结果。
- 首次工作树审计使用本地临时脚本 `review_projection.py`，该脚本未随仓库发布。复核依据为本目录 JSON、固定 D/S 和下文 Git tree/blob 比较方法。

## 源码投影

从原导出记录取得 26 个 crate 目录，连同 `assets/fonts`、`LICENSE-APACHE`、`LICENSE-GPL`，使用 `git ls-tree -rz D` 和 `git cat-file --batch` 读取固定对象；递归枚举候选对应目录，比较路径集合、原始字节和 Git mode。

| 检查 | 结果 |
| --- | --- |
| 完整 crate 目录 | 26 个，与导出记录和 metadata workspace members 一致 |
| 文件条目 | 430 项 |
| 普通文件 | 403 项，mode `100644` |
| 符号链接 | 27 项，mode `120000`，链接目标字节一致 |
| 缺失、额外或内容/mode 不同 | 均为 0 |

430 项不包含生成的根 Cargo.toml、README 和四份来源控制文件；原导出清单的 436 项包含这些生成或保留项。没有把目录权限、时间戳或缓存当作 Git 源码身份。

`alloy-source/Cargo.toml`、`Cargo.lock`、`.cargo/config.toml`、`rust-toolchain.toml` 均与 D 中相应原文件逐字节相同。其 SHA-256 见 JSON。已保留的导出记录与其来源摘要吻合。

## 显式根配置变换

- 根 workspace members 为上述 26 个 crate。resolver、workspace package 和 lints 的 TOML 值与完整源保持一致；147 项保留的 workspace dependencies 没有字段或值变化。
- 根 `[patch.crates-io]` 仅保留 metadata 中可达的 `async-process`、`async-task`、`calloop`、`windows-capture`。其余原 patch 包不在本次 metadata 中。
- `calloop` 新增明确 `rev = eb6b4fd17b9af5ecc226546bdd04185391b3e265`，固定到原锁文件已经选定的 commit。其余三个 patch 的 git/rev 配置不变。
- 根 profile 保留 dev 的基础值和 build-override，以及 release 的基础值。未复制原 dev.package 特殊优化、release.package 的 Zed 配置、dbg 和 release-fast profile。这属于独立工作区配置变换，不应描述为全部构建配置原样保留。
- 工具链仍为 Rust `1.98.1`、minimal profile；组件保留 rustfmt/clippy。未要求 rust-analyzer、rust-src 或三个附加编译 target。
- Cargo 配置保留通用 rustflags、`tokio_unstable`、Windows 的 `windows_slim_errors` 和 `MACOSX_DEPLOYMENT_TARGET = 10.15.7`；删除完整 Zed 的 aliases、Windows livekit 静态 CRT 参数和 aarch64 Linux libwebrtc 链接器参数。

这些配置变化未修改 crate manifest 或源码。完整 TOML 值保存在 JSON，便于对照后续独立构建日志。

## 锁文件与依赖图

| 项目 | 完整源 | 精简候选 |
| --- | --- | --- |
| Cargo.lock 格式 | 4 | 4 |
| package 数 | 1824 | 874 |
| SHA-256 | `9ff58114305da0bf66438fe64c571a64bfd65c05422960a20d4f2b1f20ff0e20` | `f1b9fa1c2dd5ceabd9d3ff9a3e2b7aa8357d9b8ea25de9dd92126452af8b5547` |

精简锁保留 874 个原包，删除 950 个包，没有新增 package 身份。按 name、version、仓库 URL 与 Git fragment 比较后，所有保留版本、registry checksum 和 Git commit 均保持不变。原始 source 字符串只有一项差异：

```text
calloop 0.14.3
old: git+https://github.com/zed-industries/calloop#eb6b4fd17b9af5ecc226546bdd04185391b3e265
new: git+https://github.com/zed-industries/calloop?rev=eb6b4fd17b9af5ecc226546bdd04185391b3e265#eb6b4fd17b9af5ecc226546bdd04185391b3e265
```

将 Cargo.lock 依赖的简写和带版本写法解析为完整 package 身份后，40 个保留包的依赖边发生裁剪，共删除 65 条边、新增 0 条边；没有依赖被改指另一版本或 Git commit。这与从完整 Zed workspace 缩小成员及 feature 使用范围一致；不能宣称整个依赖图不变。

父任务提供的 metadata 包含 26 个 workspace members、874 个 packages。从全部 workspace members 遍历 resolve graph，874 个包全部可达。四个保留 patch 的解析结果为：

| patch | 解析版本 | Git commit |
| --- | --- | --- |
| async-process | 2.5.0 | `0b6d6713570af61806e1e5cb40e0f757cb93fd9d` |
| async-task | 4.7.1 | `b4486cd71e4e94fbda54ce6302444de14f4d190e` |
| calloop | 0.14.3 | `eb6b4fd17b9af5ecc226546bdd04185391b3e265` |
| windows-capture | 1.4.3 | `f0d6c1b6691db75461b732f6d5ff56eed002eeb9` |

## 范围限制

本报告证明本次候选的源码投影和依赖身份保留。metadata 可达不等于各平台可构建；独立 workspace 的格式、Clippy、单元测试、原生测试及最终快照验收仍以父任务对应日志为准。候选尚未固定为 S，提交前若修改上述路径或根锁，需要对变更后的对象重新核对。


## 固定 S 的 Git 对象复核

固定 S 为 `9d59ea617d75d02e4645eefd22844235431138c8`，tree 为 `329c974731e4f75fa6f45868bbf0fdb1c59976a5`。本节读取 Git tree/blob，不依赖候选工作树内容。先前「尚未提交」描述保留为第一轮工作树审计的历史状态；本节将该结果绑定到 S。

从 S 的 Cargo.toml 和 crate manifests 重新递归普通、optional、build、dev 及各 target 的 path 依赖，闭包仍为 26 个 crate，与 workspace members 和原来源记录完全一致。430 项 payload 的路径集合、Git blob、类型及 mode 与 D 和前次审计完全相等（403 个普通文件、27 个符号链接）。四份原始根配置备份与 D 原字节及前次摘要一致。

根 Cargo.lock 与前次审计逐字节相同；根 workspace 的 resolver/package/lints、147 项继承依赖、四项 patch 和 profiles 均延续前次审计结果。根 Cargo config 与工具链的 TOML 值与前次审计一致。固定文件如下：

| S 中的文件 | SHA-256 |
| --- | --- |
| `Cargo.toml` | `0452c6b59bc879e6fe797a19011c5e0162d6e74ea6aec0f8bfdd5431a73c8ed2` |
| `Cargo.lock` | `f1b9fa1c2dd5ceabd9d3ff9a3e2b7aa8357d9b8ea25de9dd92126452af8b5547` |
| `.cargo/config.toml` | `b341c65c1a18dd332f59d6b0cacc764594f17d96ca84f1e471d6749400758e0c` |
| `rust-toolchain.toml` | `887f9be066a15585a2c583578e84b0fcb541126d81546276bad3d2ff00d61167` |
| `ALLOY-SOURCE.json` | `8114835e4400468cf615802262bd54c5f09522b6687a126dea5b0302ef216d30` |
| `script/gpui_snapshot.py` | `9a82458aa24bedaaf9f592f57d2f956e612dfab1dc31265190e7624bebb69d45` |
| `script/check` | `c2af1bd820ed31a2e3dcdb30d836f3696767e5773227f158925e59065b296837` |
| `script/clippy` | `e81b8d52459bb3b2134d6b5e8ed5af118a09245e87e20204a45240dff9cfb720` |

`alloy-source/ALLOY-SNAPSHOT.json` 仍为 `88a1781f7241d1f6a5f0f178a63230e0730085fce93c0f1049b66445a076615a`，绑定旧 exporter `fa10e78736b16d03c92c6740850a5845c18ffc21b101b61cb885da370831c000`。上表的独立仓库 exporter 是本轮首次固定摘要，不冒称与旧 exporter 相同。`ALLOY-SOURCE.json` 的 U、D 和原 snapshot 摘要均吻合。

S 无父提交；从 S 可达的提交只有 S。当前精简仓库全部 refs 的可达图也不包含 U 或 D。原源仓库与候选仓库、refs 均未修改，没有运行 Cargo、构建或签名操作。完整复核结果在 JSON 的 `fixed_git_verification` 字段。

本报告中的本地路径表示审计时的位置。迁移后的精简仓库位于 `/Users/Xuan/Developer/AprilNEA/gpui-alloy`，完整历史位于 `/Users/Xuan/Developer/AprilNEA/gpui-alloy-archive`；关联 worktree 的修复与提交核对见 [local-layout.json](local-layout.json)。
