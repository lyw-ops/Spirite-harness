# 2026-11-11 · Tier1/2/4/5 吃饭关键帧接入原生并安装 1.19 / build 21

用户看过四档候选的对照动图和随附的不足清单后回复「都可以，接入」。接入的正是所展示的候选，时间线和像素都没有再改。
至此五个工作档位吃饭时手和嘴都在动。

## 资源包

Consumer `pets/reimu/animations/eating/sources/task_N-eating-keyframes-v1/`，596×596、10 fps、`loop: true`，首末帧是批准静帧的原始字节。

| 档位 | 帧数 | source.json SHA-256 | 取代 |
| --- | --- | --- | --- |
| task_1 | 24 | `93cc28dd3dd1ff481d0534ded79462bddbe7cf00990c5a92f807e295fa461689` | `task_1-emote-loop-v1` |
| task_2 | 16 | `a378809c6be6175c11ea1f8affb5e8bd09a9e3f061e6bdad106c7233574fec46` | `task_2-chew-v9` |
| task_3 | 24 | `bde3db8fb4a26fcacd2cf23b9f880542f00747c5bff937680c9cf3e156409d95`（未变） | `task_3-face-loop-v1` |
| task_4 | 24 | `88e3b6f3fb5a67089efbe02d1b59d2d5f2dde5474ee6d9dc1b584b25b474260a` | `task_4-face-loop-v1` |
| task_5 | 24 | `b032d715f96a6e9790c25233d0e9ad39d9fa5107492510c5ca78bcf42e1e22bf` | `task_5-face-loop-v1` |

被取代的包全部保留为来源记录并继续受仓库门禁校验；`task_2-chew-v9` 仍是网页运行时 `assets/reimu/eating/task_2` 的来源，那一侧没有改。
`export_packages.py` 重跑后 Tier3 的清单与 README 字节不变。

## Consumer 改动（工作区，未提交）

`build.py` 把 Tier1/2/4/5 改钉到新清单（Tier2 补上 base 摘要校验）并升到 1.19 / build 21；`scripts/check-repository.sh` 把四个新包加入必备文件，
循环包校验按档位取帧数（Tier2 为 16）并以 `task_2-chew-v9/base.png` 作为 Tier2 的批准静帧；`desktop/README.md` 补充说明。
Swift 源码没有变化：Tier2 仍是 16 帧 / 1.6 秒，其余 24 帧 / 2.4 秒。

## 验证与安装

全新编译的 1.19 正式身份包：217 项行为、37 项原生 AppKit、状态契约、表情 3 项、站姿 5 项、Tier1/3/4/5 各 5 项、Tier2 4 项、仓库门禁通过；
严格验签在安装前、安装后、启动后均通过。可执行文件 SHA-256 `02e07e2473636e8ced54fb443e264578f0b05247e406a61b980a149db397c6a1`。
替换 1.18 / build 20；回退包 `build/reimu-1.19-install-20261111/rollback-1.18-build20.zip`
（SHA-256 `cd94e7ff080f6fac01a9ecb50897758abbb8fc4d53183e70a11725b84bcba50f`，解包与原安装逐文件相同、验签通过）。
安装后的 `--validate-assets`：五档 `reason: none`，帧数 24 / 16 / 24 / 24 / 24。

## 边界

候选记录里列出的不足原样带入（Tier1 两拍咀嚼差别轻、Tier2 重画区域线条偏柔且 K1 袖子下缘有淡重影、Tier5 手挨着左侧星星、每档只有两张关键帧）。
安装时用户偏好「减弱动态」仍为开启（`reduced = 1`），开启期间所有循环停在第 0 帧；本轮没有改这个设置，也没有在屏幕上看过实际播放。
## 发布

用户于 2026-11-11 要求「提交并推送」：Consumer `3b46b9c85ff0c5dc3c6c94c40bac9fc578f2035d` 已推送到 origin/main，Harness 记录随后提交。没有 tag 或 release。
