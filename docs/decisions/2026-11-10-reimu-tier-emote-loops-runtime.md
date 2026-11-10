# 2026-11-10 · Tier1/3/4/5 表情符号循环接入原生并安装 1.14 / build 16

用户看过 v1 审阅动图后回复「可以，接入」。此前同一会话里用户已说「由你来全权决定做什么」，
因此接入完成并验证后直接安装，没有再单独出预览包等待确认。

## v1 → v2：为满足加载器合同重排了收尾

原生加载器要求循环的首帧和末帧都等于 base（`循环首尾不匹配`）。v1 的爱心是绕中心的正弦浮动，
末帧不在静止位。v2 把每条轨道改成在第 23 帧回到静止，并让静止点落在速度为零的端点：
爱心改为「从原位浮起再落回」，汗滴与热气在第 23 帧前重新成形，Tier5 汗滴改为衰减轻颤。
符号、幅度量级和 2.4 秒周期不变。**v2 的动图没有在安装前再给用户看一遍**，这是与获批画面的唯一差别。

## 资源包

Consumer `pets/reimu/animations/eating/sources/task_{1,3,4,5}-emote-loop-v1/`：596×596、24 帧、
10 fps、`loop: true`。第 0 帧与第 23 帧是批准静帧的原始字节；其余帧来自 Harness 0.8.0
`build/reimu-tier-emote-loops-v2`。清单摘要：

| 档位 | source.json SHA-256 |
| --- | --- |
| task_1 | `0954274f13246c8934070b9df0662202ea358774e8228a711b5208a1898672ee` |
| task_3 | `5db01e6a3837f53515646a3100892f1f073b91caf7f9f896c5a4f83c11c2ba53` |
| task_4 | `793a6397383faa361055c9f5a85c25e0aa0cfae29d4a84fccea7c5c5a4963289` |
| task_5 | `b8237c872e41c2a74a1b469f74bc1b3ac32f1440481d54e14133c0281e5576b9` |

旧的 `task_N-static-v1` 包保留不动，仍由仓库门禁校验。

## Consumer 改动（工作区，未提交）

- `build.py`：四个档位改钉新清单摘要，校验 24 帧 / 10 fps、逐帧摘要与首尾等于 base；版本 1.14 / build 16。
- `main.swift`：四个档位的 `ClipSpec` 改为 24 帧 / 10 fps 与逐帧文件名；自测改查循环帧选择。
- `PetBehavior.swift`：四个档位按 `Int(t × 10) % 24` 取帧；减弱动态仍保持第 0 帧。
  `workLoopDuration` 对这四档仍为 0：只有符号在动，任何时刻离开都安全，所以档位切换的时序与抢占规则一条没改。
- 测试：行为测试里四档从「静态保持」改为「播放 24 帧循环」；各档位包测试改查 24 帧 / 2.4 秒，
  并各新增一项「循环中段帧损坏只降级本档」；`scripts/check-repository.sh` 新增四个循环包的门禁。

## 验证

Harness：八个构建经公共 CLI plan/render/validate 通过；第 0 帧、第 23 帧与 reduced 全帧等于批准静帧；
符号外接框外扩 14 px 之外的变化为 0。160 px 下与静帧相差 ≥12/255 的像素数最大值为
Tier1 90、Tier3 108、Tier4 263、Tier5 298。

Consumer 全新编译的 1.14 正式身份包：198 项行为、37 项原生 AppKit（隔离 QA 域）、31 项状态契约、
表情 3 项、站姿 5 项、Tier1/3/4/5 各 5 项、Tier2 4 项、仓库门禁，全部通过；严格深层验签在安装前、
安装后、启动后均通过。可执行文件 SHA-256 `f806765e97b4dce8d5e768ca95dadfe6e67d4a7cb3349d917114c68c1d320e19`。

## 安装

替换 1.13 / build 15；回退包 `build/reimu-1.14-install-20261110/rollback-1.13-build15.zip`
（SHA-256 `9b9b309ea96fbfda186f8718fcd56ece4d1a09f007b6f8645f099bbc4372fa66`，解包与原安装逐文件相同）。
启动日志：`version 1.14 / build 16 / preview false`，真实 `working`、1 项任务、Tier1。

## 边界

仍然只是符号动效，不是吃饭动作。Tier1 汗滴在 160 px 下偏弱。制作者没有在屏幕上亲眼看循环播放，
帧选择由原生自测覆盖。

## 发布

用户随后回复「提交并推送」。Consumer 提交 `0c814aa95ec464bbadef6a2c3344b9724b73b302` 已推送到 `origin/main`，
`git ls-remote` 核对远端 `refs/heads/main` 为同一 SHA。该提交同时带上了 2026-09-20 留在工作区的过渡规格
说明文档改动，并更正了四处仍称这四档为「一帧静态保持」的文档。已安装的 1.14 可执行文件是在这些
文档改动之前由同一份 Swift 源码编译的。没有 tag，也没有发布安装包；runtime 的 visual 门仍是 in_review。
