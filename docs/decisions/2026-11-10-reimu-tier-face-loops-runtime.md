# 2026-11-10 · Tier3/4/5 脸部动作接入原生并安装 1.17 / build 19

用户看过脸部候选的动图与放大姿态图后回复「接入这三个」。接入的正是所展示的那一版，没有再改动效。

## 资源包

Consumer `pets/reimu/animations/eating/sources/task_{3,4,5}-face-loop-v1/`：596×596、24 帧、10 fps、`loop: true`，
在符号循环之上加入脸部动作（Tier3 咀嚼、Tier4 面条晃动、Tier5 张合嘴）。第 0 帧与第 23 帧是批准静帧的原始字节。
脸部姿态是已批准像素在量好的小框内的连续形变，框内存在新的像素值；框与每帧幅度记录在各包 `source.json` 的 `motion` 里。

| 档位 | source.json SHA-256 |
| --- | --- |
| task_3 | `60c219c019ef8931b8cfeb2acd6e24cd60c9d64beaf678cd12a00a35a4211b1c` |
| task_4 | `7c1406a5fc5150832a031c15a6b28bfc93a0115e5bdda0d186cd88b3764dec80` |
| task_5 | `aea015ac5490daaaf616abe18afcb061a5cbbd661245207bf81098059cc74192` |

Tier1 没有脸部动作，继续使用 `task_1-emote-loop-v1`。三个被取代的 `task_N-emote-loop-v1` 包保留为来源记录，仍受仓库门禁校验。

## Consumer 改动（工作区，未提交）

`build.py` 改钉三个新清单并升到 1.17 / build 19；`scripts/check-repository.sh` 对三个脸部循环包做与符号循环包相同的校验；
`desktop/README.md` 补充说明。Swift 源码没有因这次接入而变化（帧数、帧率、取帧规则与符号循环相同）。

## 验证与安装

全新编译的 1.17 正式身份包：217 项行为、37 项原生 AppKit、31 项状态契约、表情 3 项、站姿 5 项、
Tier1/3/4/5 各 5 项、Tier2 4 项、仓库门禁通过；严格验签在安装前、安装后、启动后均通过。
替换 1.16 / build 18；回退包 `build/reimu-1.17-install-20261110/rollback-1.16-build18.zip`
（SHA-256 `d8080ba8cba4e8a13bcd354aed3d05ffd7bc520f0033b5d41a6865a327d2bd3b`，解包与原安装逐文件相同）。
启动日志：`build 19`，真实 `working`、Tier2。

## 边界

动作轻微：160 px 下每个档位脸部只有约 105–111 个像素在变。Tier5 肉串边缘有少量残留色。
安装时用户偏好「减弱动态」仍为开启，开启期间所有循环停在第 0 帧；本轮没有改这个设置，也没有在屏幕上看过实际播放。
没有 commit、push、tag。

## 发布

用户随后回复「提交并推送」。Consumer 提交 `2c62a77067d53746824946eeeb4c6c8ff2522175` 已推送到 `origin/main`，
`git ls-remote` 核对远端 `refs/heads/main` 为同一 SHA。没有 tag，也没有发布安装包。
