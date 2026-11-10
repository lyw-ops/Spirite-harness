# 2026-11-10 · Tier3 吃饭关键帧接入原生并安装 1.18 / build 20

用户看过 Tier3 试点的对照动图（320 px 与实际 160 px）后回复「可以，继续」。接入的正是所展示的那一版，时间线和像素都没有再改。

## 资源包

Consumer `pets/reimu/animations/eating/sources/task_3-eating-keyframes-v1/`：596×596、24 帧、10 fps、`loop: true`。
筷子夹饭送到嘴边并张嘴（7 帧）→ 筷子回到碗沿、闭嘴鼓腮（10 帧），其余为批准静帧；蒸汽符号循环与 `task_3-emote-loop-v1` 相同。
第 0 帧与第 23 帧是批准静帧的原始字节。`source.json` SHA-256
`bde3db8fb4a26fcacd2cf23b9f880542f00747c5bff937680c9cf3e156409d95`，23 个不同的帧文件。
两张关键帧是图像模型对批准静帧的改图（ChatGPT 应用内置 Codex 命令行的 `image_generation`）；只采用三个实测矩形内的像素
（边缘羽化 8 px），矩形记录在 `motion.keyframe_rectangles_exclusive`，其余逐像素等于批准静帧。
它取代 `task_3-face-loop-v1` 作为 Tier3 的运行时来源；旧包保留为来源记录并继续受仓库门禁校验。

## Consumer 改动（工作区，未提交）

`build.py` 的 Tier3 钉值改为新清单并升到 1.18 / build 20；`scripts/check-repository.sh` 把新包加入必备文件与循环包校验；
`desktop/README.md` 补充说明。Swift 源码没有变化（帧数、帧率、取帧规则与此前的循环相同）。

## 验证与安装

全新编译的 1.18 正式身份包：217 项行为、37 项原生 AppKit、状态契约、表情 3 项、站姿 5 项、Tier1/3/4/5 各 5 项、Tier2 4 项、
仓库门禁通过；严格验签在安装前、安装后、启动后均通过。可执行文件 SHA-256
`4c092e2c598d8c94c5f799a5b131aa5856309351750d606e5df8def7a834990d`。
替换 1.17 / build 19；回退包 `build/reimu-1.18-install-20261110/rollback-1.17-build19.zip`
（SHA-256 `2e66872f827e0f9667d9856d05549324d5c7ea61193f3dd16c1f6fc8a75cd590`，解包与原安装逐文件相同、验签通过）。
安装后的 `--validate-assets`：Tier3 24 帧、2.4 秒、`reason: none`，其余档位均为 `none`。

## 边界

「嚼」是一个保持的姿势，没有连续起伏（只有两张关键帧）。
安装时用户偏好「减弱动态」仍为开启（`reduced = 1`），开启期间所有循环停在第 0 帧；本轮没有改这个设置，也没有在屏幕上看过实际播放。
没有 commit、push、tag。
