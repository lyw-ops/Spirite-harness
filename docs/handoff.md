# Project handoff

## 2026-11-11 1.27 / build 29 已安装并发布：举御币、飘起来、扫地 + Codex 审过的台词

用户说「做完，台词你可以让codex去根据博丽灵梦的人物性格和习惯去review」，看过三张对照动图后回复「可以，安装」。
`docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md`，`REIMU-GOHEI-FLOAT-SWEEP-001`，工作目录 `build/reimu-standing-{gohei,float,sweep}-v1/` 和 `build/reimu-line-review-v1/`。
三个动作各两张 Codex 关键帧：站姿第四下点击举御币、拖动时飘起来（整张取用）、扫地（早晨问候 + 待机自发）。Codex 审了全部 135 句台词，建议改的 16 句都已采纳。
三个包带确认记录重新导出，`build.py` 改钉摘要，1.27 / build 29 通过全部测试（行为 353、原生 49、16 个资源包与状态测试、仓库门禁）后安装；
回退包 `build/reimu-1.27-install-20261111/rollback-1.26-build28.zip`。安装后用户回复「提交并推送」，Consumer `a81b57b` 已推送。
构建输入现在是 `--gohei`、`--float`、`--sweep`、`--night-sleep`、`--yawn`、`--droop`、`--poof`、`--tea-break`，都可以用已安装应用的 `Resources` 下对应目录。
至此设计路线里的七个新图动作都做完并装上了；没做的只有画出来的站 ↔ 坐过渡（`REIMU-WORK-TRANSITIONS-001`）。

## 2026-11-11 1.26 / build 28 已安装并发布：夜里伏桌睡

用户对我建议的下一个动作回复「做」，看过对照动图后回复「可以，安装」。`docs/decisions/2026-11-11-reimu-night-sleep.md`，`REIMU-NIGHT-SLEEP-001`，
工作目录 `build/reimu-night-sleep-v1/`。不画新图：9 月的睡姿和三张过渡姿态原样打包成 `night_sleep-v1`；新做的是规则
（深夜 23–7 点、空闲且没人理满 20 分钟入睡；点击和天亮播醒来姿态；开工、等确认、出错、拖动、喂食、暂停立刻离开）。
包带确认记录重新导出，`build.py` 改钉摘要，1.26 / build 28 通过全部测试（行为 334、原生 46、夜间睡眠 4 及其余、仓库门禁）后安装；
回退包 `build/reimu-1.26-install-20261111/rollback-1.25-build27.zip`。安装后用户回复「提交并推送」，Consumer `eb978dc` 已推送。
菜单「深夜没人理就趴桌睡」默认开；减弱动态下照样入睡、不播中间姿态（这两处是我定的，已告诉用户）。用户还没在应用里看到它。
构建多了一个输入 `--night-sleep`（Consumer 仓库里的包，或已安装应用的 `Resources/Sleep`）。

## 2026-11-11 1.25 / build 27 已安装并发布：出错时垂头叹气

用户对我建议的下一个动作回复「画」，看过对照动图后回复「可以，安装」。`docs/decisions/2026-11-11-reimu-failure-droop.md`，`REIMU-FAILURE-DROOP-001`，
工作目录 `build/reimu-standing-droop-v1/`。`droop-v1` 带确认记录重新导出，`build.py` 改钉摘要，1.25 / build 27 通过全部测试
（行为 311、原生 44、垂头 4 及其余、仓库门禁）后安装；回退包 `build/reimu-1.25-install-20261111/rollback-1.24-build26.zip`。
安装后用户回复「提交并推送」，Consumer `46e5799` 已推送。构建多了一个输入 `--droop`（Consumer 仓库里的包，或已安装应用的 `Resources/Droop`）。
减弱动态开着时出错只出台词；用户确认时还没在应用里看到它。

## 2026-11-11 1.24 / build 26 已安装并发布：等你确认时托腮；清理同步冲突副本

用户对「接着做什么」里的两项回复「做，可以处理一下冲突副本」。

- 等确认时托腮：`docs/decisions/2026-11-11-reimu-waiting-slouch.md`，`REIMU-WAITING-SLOUCH-001`。不加新图，`needs_input` 时显示已批准的托腮循环；
  行为 301、原生 43 及其余检查通过，1.24 / build 26 已安装，回退包 `build/reimu-1.24-install-20261111/rollback-1.23-build25.zip`。
  安装后用户回复「提交并推送」，Consumer `05cde7d` 已推送。视觉门仍是 `in_review`：用户还没看到效果。
- 冲突副本：`docs/decisions/2026-11-11-reimu-conflict-copies-cleanup.md`，清单 `build/reimu-conflict-copies-cleanup-20261111/moved.tsv`。
  585 个有原件的副本和 8 个空目录移到了废纸篓 `~/.Trash/reimu-conflict-copies-20261111/`（没有永久删除）；4 个没有原件的没动。
  原因（仓库在被同步的 `~/Documents` 里）没有消除，副本还会再出现，提交时继续只按文件名添加。

## 2026-11-11 1.23 / build 25 已安装并发布：站姿打哈欠、烟雾过渡

用户说「画打哈欠」，随后说「然后我也建议我们做一些过度动画」；看过两张对照动图后回复「都可以，安装」。
两个包带确认记录重新导出，`build.py` 改钉摘要，1.23 / build 25 通过全部测试（行为 292、原生 42、哈欠 4、烟雾 4、收工茶 5 及其余、仓库门禁）后安装。
Consumer `cb16088` 已推送。回退包 `build/reimu-1.23-install-20261111/rollback-1.22-build24.zip`。

- 哈欠：`docs/decisions/2026-11-11-reimu-standing-yawn.md`，`REIMU-STANDING-YAWN-001` 完成，工作目录 `build/reimu-standing-yawn-v1/`。
- 烟雾过渡：`docs/decisions/2026-11-11-reimu-poof-display-bridge.md`，`REIMU-POOF-BRIDGE-001` 完成，工作目录 `build/reimu-poof-bridge-v1/`。
  它是如实标注的显示桥，不是画出来的起身 / 坐下；`REIMU-WORK-TRANSITIONS-001` 的门没有动。

要留意：确认依据是动图（烟雾那张是离线合成，不是录屏），用户确认时还没在应用里看到；安装时偏好 `reduced = 1`，
减弱动态开着时哈欠只出台词、烟雾不出现。下次构建的输入：`--tea-break`、`--yawn`、`--poof` 都可以用已安装应用的 `Resources/TeaBreak`、`Yawn`、`Poof`。
设计里还没做的：御币、垂头、漂浮、扫地、夜间睡觉，「等确认时用托腮图」，1.20 台词逐句确认。

## 2026-11-11 用户确认漫画对话框和收工茶：「都可以」

用户醒来后对「对话框和收工茶的样子可以吗？」回复「都可以」。`REIMU-MANGA-BALLOONS-001`、`REIMU-TEA-BREAK-001` 的视觉门改为 `approved`，两个任务完成。
`REIMU-DIALOGUE-ACTIONS-001` 的台词仍是 `in_review`：用户用过 1.20 并在此基础上提了对话框的要求，没有提出异议，但也没有逐句确认。
已安装的仍是 1.22 / build 24，应用没有变化。下一步候选：设计里剩下的六个动作，按顺序是站姿打哈欠；每个动作画图前都要用户点头。

## 2026-11-11（深夜）漫画对话框 1.21、收工茶 1.22 已安装并发布；多余的预览应用移入废纸篓

用户睡前留言「后续的所有操作都由你决定你推进，包括推送提交等」，以下都是据此推进的，**成品用户都还没看过**（三个台账任务的视觉门均为 `in_review`）。

- **漫画对话框（1.21）**：台词画在独立的点击穿透小窗口里，四种形状按语气选用，默认在头顶并避开任务状态框。`docs/decisions/2026-11-11-reimu-manga-balloons.md`，`REIMU-MANGA-BALLOONS-001`。
- **收工茶（1.22）**：从工作中进入「这一轮已结束」时，她在同一张矮桌前喝茶（48 帧 / 4.8 秒），状态结束后回到站姿。三个姿态由 Codex 图像生成改 Tier3 批准静帧得到，
  矩形外逐像素等于 Tier3。`docs/decisions/2026-11-11-reimu-tea-break.md`，`REIMU-TEA-BREAK-001`，工作目录 `build/reimu-tea-break-v1/`（`build.sh` 一步重建）。
- **清理**：6 个旧的 `灵梦桌宠预览.app` 移到废纸篓（未永久删除），清单在 `build/reimu-app-cleanup-20261111/`；研究脚本改读 `build/reimu-preview-resources-1.13/`。
  `docs/decisions/2026-11-11-reimu-redundant-app-cleanup.md`。
- 发布：Consumer `3683450`（1.20 + 1.21）、`4dc36a9`（1.22）已在 origin/main；Harness 记录随本提交发布。
- 安装链：… → 1.19 → 1.20 → 1.21 → 1.22，每一步的回退包在 `build/reimu-1.NN-install-20261111/`。现在构建输入直接取已安装应用的 `Contents/Resources`，收工茶取 Consumer 仓库里的包。

等用户醒来要问的：对话框和收工茶的样子是否认可（不认可就用回退包退回）；「减弱动态」仍为开启，喝茶和小表情在屏幕上是静止的；
其余六个新动作（站姿哈欠、举御币、垂头、飘起来、扫地、夜里伏桌睡）和「等确认时改用托腮图」还没有做。

## 2026-11-11 灵梦动作与对话设计：第一批已安装 1.20 / build 22

用户要求由我担任设计师，按灵梦人设和其他桌宠的经验设计更多动作和对话。设计稿与回执：
`docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md`，台账 `REIMU-DIALOGUE-ACTIONS-001`（视觉门 `in_review`）。

已落地（不需要新图）：真实工作事件触发的一句话（开工、任务增减、一轮结束、等确认、出错、被中断、久坐 50 分钟、启动问候；
菜单「工作状态变化时说一句」默认开，偏好键 `muteRemarks`）；点击阶梯加第三下「半眼盯人」；各场景台词加厚并各自轮换；
拖动 / 放下 / 喂食台词轮换；待机被点时带时段与季节句；三个站姿眼皮小表情。行为 254 项、原生 38 项及各档位检查、仓库门禁通过。
回退包 `build/reimu-1.20-install-20261111/rollback-1.19-build21.zip`。

未做：需要新图的七个动作只有设计（收工茶、站姿哈欠、举御币、垂头、飘起来、扫地、夜里伏桌睡），画图需要用户对那一批点头；
「等确认时改用托腮图」不需要新图但会改一个状态的默认画面，也留给用户决定。
用户偏好「减弱动态」仍为开启，三个小表情在屏幕上不会动，只有文字出现。写这一条时两个仓库都还没有提交；随后已发布，见上一条。

## 2026-11-11 五档吃饭关键帧全部接入，已安装 1.19 / build 21，已发布

用户看过 Tier1/2/4/5 候选后回复「都可以，接入」。Consumer 新增 `task_{1,2,4,5}-eating-keyframes-v1`（Tier2 为 16 帧），
`build.py` 四档改钉并升到 1.19 / build 21，仓库门禁扩展，Swift 未变；217 行为 / 37 原生及各档位检查通过。
回退包 `build/reimu-1.19-install-20261111/rollback-1.18-build20.zip`。详见 `docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md`。

用户随后要求提交并推送：Consumer `3b46b9c` 已在 origin/main，Harness 记录随本提交发布。用户偏好「减弱动态」仍为开启，循环在屏幕上是静止的。
可做的后续：每档再加一张关键帧让咀嚼有起伏；Tier2 重画区域线条偏柔；待机、戳一戳等非吃饭状态仍没有手嘴动作。

## 2026-11-10 Tier3 吃饭关键帧已接入并安装 1.18 / build 20；Tier1/2/4/5 候选待确认（均未提交）

用户看过 Tier3 试点后回复「可以，继续」。Consumer 新增 `task_3-eating-keyframes-v1`（筷子夹饭 → 张嘴 → 放回碗沿 → 鼓腮），
`build.py` 改钉 Tier3 并升到 1.18 / build 20，仓库门禁扩展，Swift 未变；217 行为 / 37 原生及各档位检查通过。
回退包 `build/reimu-1.18-install-20261110/rollback-1.17-build19.zip`。详见 `docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-runtime.md`。

其余四档的关键帧也已画出并合成候选循环（Tier2 为 16 帧，其余 24 帧），像素门全部通过，对照动图已发给用户，**尚无答复，未接入**。
Tier2、Tier5 各重画一次（生成端把改动贴回矩形留下接缝 / 「咬」画成吐舌头）。`intake.py` 新增按档位启用的变化区域遮罩。
详见 `docs/decisions/2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md`。

下一步：用户确认哪几档可以后，用 `build/reimu-eating-keyframes-v1/export_packages.py`（需为该档补 `MOTION` / `APPROVAL` 文案）导出资源包并改钉；
Tier2 仍是 16 帧契约。安装链：1.9 → 1.13 → … → 1.17 → 1.18。用户偏好「减弱动态」仍为开启，循环在屏幕上是静止的。

## 2026-11-10 吃饭关键帧试点成功（Tier3）：手和嘴真的在动，待用户确认

用户回复「做」。用 ChatGPT 应用内置的 Codex 命令行（`/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex`，
`exec -s workspace-write`，带 `image_generation`）画出 Tier3 的两张关键帧；`build/reimu-eating-keyframes-v1/intake.py` 只取实测范围内的像素、
其余锁回批准原图，`verify.py` 通过全部像素门（首末帧与 reduced 等于批准静帧、范围外变化为 0、160 px 下变化 518–607 px）。
计划的改图框偏小，按第一次交付的差异图给 Tier3 加了两个接收矩形。详见
`docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-pilot.md`。未接入、未提交。
下一步：用户确认后把 Tier3 做成资源包接入，并用同一流程画 Tier1/2/4/5（每档交付后按实测复核范围）。

## 2026-11-10 吃饭时手和嘴不动：已写关键帧作业单，等待画稿

用户要求先解决吃饭时嘴和手没有动作。核查结论：五张吃饭图是扁平单图，Tier2 的「分层」只是切块（手层只有手指、身体有空洞），
程序做不出真实的手部动作；用户此前已否决两种变通方案，所以本轮没有再做变通。写了给图像模型的作业单
`build/reimu-eating-keyframes-v1/codex-eating-keyframes-task.md`（副本在 `~/Desktop/灵梦/`）：每档两张关键帧、量好的改图框
（98%–100% 在不透明轮廓内，透明背景不再是问题）、可检查的验收门，Tier3 先做试点。交付目录 `~/Desktop/灵梦/eating-keyframes-delivery/`。
下一步：收到 `task_3-k1.png` / `task_3-k2.png` 后写接收工具、锁定未改区域、合成循环、出对照动图。
详见 `docs/decisions/2026-11-10-reimu-eating-keyframes-work-order.md`。

## 2026-11-10 香火箱与更萌站姿试稿均被否决，站姿保持原样

用户回复「有点怪异，我们可以做一个更萌一点的博丽灵梦形象」。香火箱候选记为 rejected（脚本画的扁平道具与角色画风不搭）。
「更萌」理解为站姿（约 3.5 头身、全套里最不 Q 的一张），未向用户确认。`build/reimu-cuter-standing-v1/` 用平滑的局部等比
重采样把已批准站姿做成大头比例：A/B/C 三档，B（头 1.42×、身体 0.74×）的角色比例与坐姿 Tier1 一致（头发最宽行都是 374 px）。
只重采样已批准像素。正式接入要从 1254 原图对三张眼姿同参数处理并重钉站姿资源包。详见
`docs/decisions/2026-11-10-reimu-cuter-standing-study.md`。

**结果**：用户回复「不太行，保持原样吧」，三档试稿全部否决（账本 visual rejected），已安装的 1.17 与站姿素材均未改动。
这两轮说明：脚本画的道具和对已批准画面做比例重采样都不被接受；形象或道具要变，需要真正的新画稿。

## 2026-11-10 场景道具候选：香火箱与铜钱（待视觉确认，未接入）

用户确认人设台词「差不多」，并提出按场景做道具，例如香火箱。`build/reimu-props-v1/` 里有脚本绘制的香火箱
（站姿右侧、落在鞋线上、与角色零重叠）和方孔铜钱，以及投币互动的示意动图。设想：香火箱只在站姿场景出现，
点击它投一枚香火钱并按人设回应。原生代码未动。详见 `docs/decisions/2026-11-10-reimu-props-offering-box-intake.md`；
账本 `REIMU-PROPS-OFFERING-BOX-INTAKE-001` 的 visual 为 in_review。`REIMU-SCENE-REACTIONS-001` 的台词用户回复「差不多」。

## 2026-11-10 Tier3/4/5 脸部动作已接入并安装 1.17 / build 19；Consumer `2c62a77` 已发布

用户看过候选后回复「接入这三个」。Consumer 新增 `task_{3,4,5}-face-loop-v1`（符号循环 + 咀嚼 / 面条晃动 / 张合嘴），
`build.py` 改钉并升到 1.17 / build 19，仓库门禁扩展；Swift 源码未因此变化。217 行为 / 37 原生 / 31 状态与各档位检查通过。
回退包 `build/reimu-1.17-install-20261110/rollback-1.16-build18.zip`。详见
`docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md`。

当前安装链：1.9 → 1.13 → 1.14 → 1.15 → 1.16 → 1.17，每一步的回退包都在 `build/reimu-1.NN-install-20261110/`。
用户随后要求提交并推送：Consumer `2c62a77067d53746824946eeeb4c6c8ff2522175`（场景台词、待机只站立、脸部循环）已在 origin/main 核对；
Harness 的记录随本条一起提交。账本里 `REIMU-SCENE-REACTIONS-001` 的 visual 仍是 in_review（台词未逐句确认）。
用户偏好「减弱动态」仍为开启。Tier1 眨眼与更明显的张合嘴需要画稿。

## 2026-11-10 按场景回应 + 灵梦人设台词 + 待机只站立，已安装 1.16 / build 18（未提交）；脸部动作候选待审

用户确认「v2可以」，并提出：戳她时文字不符合场景；台词和动作多参考博丽灵梦人设；待机只正常站立；给一些脸部动作。

- 已安装 1.16：点击台词按场景选取并按人设重写；工作吃饭时单击/双击不再切回站姿；待机默认只站立
  （右键菜单可重新打开偶尔吃饭和托腮）。217 行为 / 37 原生 / 31 状态通过。详见
  `docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md`。
- 脸部动作：只用已批准像素做局部形变的候选在 `build/reimu-tier-face-loops-v1/`。Tier3/4 干净但轻微，Tier5 可用但不精致，
  Tier1 眨眼失败已移除（刘海遮眼）。未接入。详见 `docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md`。
- 注意：真实偏好里「减弱动态」当前是开启的（12:36:58 UTC 从右键菜单切换），开启时所有循环停在第 0 帧。本轮未改它。
- 本轮误删过 1.14 回退包目录，已从被替换的原包重建并核对摘要一致。

Consumer 与 Harness 均有未提交改动。下一步：用户看脸部候选；眨眼与张合嘴需要画稿（给图像模型的局部改图工单）。

## 2026-11-10 表情符号循环已接入、安装 1.14 / build 16 并发布 Consumer `0c814aa`

用户看过 v1 动图后回复「可以，接入」。Tier1/3/4/5 现在在原生里播放 24 帧 / 10 fps 的符号循环，
已安装并运行（启动日志：1.14/build 16，真实 working、1 项任务、Tier1）。完整记录见
`docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md`。

- 为满足加载器「首尾帧等于 base」的合同，动效从 v1 重排为 v2（`build/reimu-tier-emote-loops-v2/`）：
  末帧回到静止，爱心改为从原位浮起再落回。v2 未在安装前再给用户看，账本 runtime 的 visual 记为 in_review。
- Consumer 工作区新增四个 `task_N-emote-loop-v1` 包，改了 `build.py`、`main.swift`、`PetBehavior.swift`、
  行为测试、四个档位包测试和仓库门禁；档位切换时序与抢占规则未改（这四档离开仍不等待）。
- 198 行为 / 37 原生 / 31 状态 / 各档位加载回退 / 仓库门禁通过，验签三次通过。
- 回退：`build/reimu-1.14-install-20261110/rollback-1.13-build15.zip`；再往前是
  `build/reimu-1.13-install-20261110/rollback-1.9-build11.zip`。

用户随后要求提交并推送：Consumer `0c814aa95ec464bbadef6a2c3344b9724b73b302` 已在 origin/main 核对；
Harness 的记录随本条一起提交。账本 runtime 任务只剩 visual（v2 待用户看）。真正的吃饭动作仍需首尾帧视频路线
（`build/reimu-video-loop-kit-v1/`，要用户自己跑视频模型）。

## 2026-11-10 已安装 1.13 / build 15；Tier1/3/4/5 表情符号循环动效待视觉确认

用户回复「由你来全权决定做什么」。据此做了两件事，均有决定记录：

- **安装**：从已发布 Consumer `c2684cc` 全新编译正式身份 1.13/build 15 并替换 1.9/build 11，只含用户已批准的
  Tier1–5 画面。198 行为 / 37 原生 / 31 状态及各加载回退检查通过，安装前后与启动后严格验签通过；启动日志为
  真实 `working`、3 项任务、Tier3。回退包 `build/reimu-1.13-install-20261110/rollback-1.9-build11.zip`。
  见 `docs/decisions/2026-11-10-reimu-1.13-installation.md`。
- **候选动效**：把 Tier1/3/4/5 批准静帧按 alpha 连通域无损拆出独立符号层（汗滴、热气、爱心、星星），
  用公共 CLI 做成 24 帧 / 10 fps 循环；第 0 帧与 reduced 全帧等于批准静帧，符号区域外变化为 0。
  账本新增 `REIMU-TIER-EMOTE-LOOPS-INTAKE-001`：technical passed，**visual in_review**，未接入 Consumer。
  见 `docs/decisions/2026-11-10-reimu-tier-emote-loops-intake.md`。

没有做的：上一条里的「下压回弹」衔接自查后判定改善有限，没有接入；首尾帧视频路线需要用户自己跑视频模型，
素材包保留。没有 commit、push、tag。下一步：用户看过动图后，把循环接进 Consumer（新资源包、摘要钉、
帧计划、各档位测试），再按既有流程出原生预览。

## 2026-11-10 参照 DeepSeek 桌宠的对照研究：两份视觉研究素材，未接入

用户要求参照近期的 DeepSeek Harness 社区桌宠改善灵梦。调研对象：dsh-pet（大肥鱼，28 段透明动画）、
deepseek-pet（大蓝鲸）、dsh-whale-musume（鲸鱼娘）、dsh-deepseek-girl-pet（16 方向追视）、dafeiyu-pet。
它们的共同做法：动作用首尾帧约束的 AI 视频在纯色底上生成再抠像；所有动作从同一标准站姿起止、角色大小
和地面线固定；睡觉拆成入睡/循环/醒来三段接力；换立绘用「下压→切换→弹起」而不是交叉淡化；气泡台词带
时间感与任务感。

本轮只做了两份可看的研究，均在忽略目录下，没有改 Consumer、没有构建或安装 App、没有 commit/push，
账本未新增任务：

- `build/reimu-pose-swap-polish-v1/`：站姿 ↔ Tier2 的「直接切换」对「下压→换图→回弹」对照。只用已批准
  像素，经公共 CLI plan/render/validate，两套 112 帧均通过；回弹版只在两次切换各 6 帧上不同，其余 100 帧
  逐像素相同，缩放 0.93–1.0 不会被原生窗口裁切。它是显示层衔接，不是角色动作。自查：改善有限，主要跳变
  来自站姿与坐姿角色比例不同（头发最宽行 245 px 对 374–454 px，约 1.5–1.85 倍）。**待用户看图决定**。
- `build/reimu-video-loop-kit-v1/`：站姿与 Tier1/3/4/5 静帧的首尾帧视频输入图和提示词。底色按实测选品红
  `#FF00FF`（六张批准图不透明像素到品红的最小 RGB 距离 ≥ 156；绿在 Tier4/5、蓝在 Tier1/5 有上百像素落在
  160 以内）。提示词未经实测，溢色与静止区域漂移要等第一段真实视频再量。

两个需要用户决定的规格冲突：抠像是 `2026-09-20-reimu-work-transitions-spec.md` 目前禁止的；整图缩放
只能标作显示层衔接。另外已安装的仍是 1.9/build 11，不含已发布源码里的 Tier1–5 工作吃饭档位。

## 2026-09-20 standing → Tier2 终点接缝可行性实验未通过

本轮只验证“新固定榻榻米层 + 新坐姿角色层 + 新固定桌餐层”是否值得继续制作中间动作。
两仓fetch后HEAD仍分别等于`origin/main`的Harness `37d9384`与Consumer `c2684cc`；四个冻结
端点摘要及standing 596回执`02a087e…`再次匹配，旧未提交规格、账本、交接和失败记录均保留。

通过内置imagegen共消耗5/6次调用：坐姿角色初稿、一次alpha定向修复、一次改变策略的干净重生、
榻榻米初稿、桌餐初稿。角色三次都存在主轮廓外低alpha脱离组件；榻榻米主组件触底并裁切；桌餐
内容正确但桌体更深、桌腿更长且仍有低alpha组件。最接近的角色身份可识别，但严格素材门未过，
因此没有挑选三层参数，也没有生成candidate、review-sheet、seam GIF、overlay或diff占位证据。

实验判定为`failed before composition`，不值得现在制作pose 1–5；应先取得三张exact-zero背景、
安全边距且端点几何更近的独立原稿，再重做同一终点实验。完整提示词、原稿、摘要、alpha证据和
596/320px明暗审阅见`build/reimu-standing-tier2-seam-feasibility-v1/`，决定记录见
`docs/decisions/2026-09-20-reimu-standing-tier2-seam-feasibility-failed.md`。账本仍只有
specification ready，其余implementation/technical/visual/consumer pending，publication
unpublished。没有生产接入、安装、commit或push。

## 2026-09-20 standing → Tier2 单帧串行 AI-only 路线仍未通过素材门

本轮两仓 fetch 后 HEAD/origin/main 仍为 Harness `37d9384`、Consumer `c2684cc`。
四个端点摘要前后不变；standing 596 回执由原始1254图重新确定性派生，使用 LANCZOS、
`596/1254`、`(0,0)`、PNG compress_level=9，完整摘要仍为
`02a087e34141aed4f65cb07a006f7275fadaf4aacb034f69c7aea598202a25b0`。

独立桌餐层、榻榻米层和 pose1 共生成七张新候选（含修复/策略改变）；没有生成多格场景。
背景修复仍出现非均匀绿幕，pose1 从干净 standing 重新编辑后仍失败，且屈膝不够明确。
因此停止，未执行 chroma key、自动抠图或合成，未继续 pose2–6，未创建正式素材包或预览。
原始未提交内容保留；生产 Swift、provider、安装、提交、推送均未触及。
账本仍 specification ready，其余 implementation/technical/visual/consumer pending，
publication unpublished。七张候选、提示词、完整摘要与像素门报告见
`build/reimu-work-transition-standing-to-tier2-serial-v1/failure-report.json`；决定记录见
`docs/decisions/2026-09-20-reimu-standing-tier2-serial-generation-blocked.md`。

## 2026-09-20 standing → Tier2 entry 素材生成失败，按硬门停止

本轮只尝试`standing_to_tier_2`首个垂直切片。两仓fetch后仍分别为Harness
`37d9384cc91ef3b3f0c349405d15f174f7c66c2f`与Consumer
`c2684cc3fecbdfbe0ae238a13f8e22fef333295d`，均等于`origin/main`；上一轮未提交规格/账本/文档
修改完整保留。standing图与manifest、Tier2 frame 0与source manifest的四个冻结摘要在前后审计
中完全不变。

standing的596端点回执已用统一`596/1254`、Pillow LANCZOS、`(0,0)`确定性派生，SHA-256为
`02a087e34141aed4f65cb07a006f7275fadaf4aacb034f69c7aea598202a25b0`，鞋线映射到
`y=584.5933014354067`。imagegen两轮完整场景原稿虽有六个真实角色姿态，但背景不是纯键色/透明，
桌子、榻榻米和餐点也逐格重绘漂移；改为显式分层后，固定桌餐层可用，但六姿态角色层及最后一次
背景提取仍带可见渐变，不能成为透明角色层。

因此按冻结规格和hatch-pet收敛规则停止。没有用本地抠图、整图变换、fade、光流、morph、历史cut
像素或静态占位掩盖失败；没有生成八帧资源包、manifest、Harness full/reduced收据、原生预览或
Consumer导入。失败证据与摘要保存在
`build/reimu-work-transition-standing-to-tier2-v1/failure-report.json`，决定记录见
`docs/decisions/2026-09-20-reimu-standing-tier2-entry-generation-blocked.md`。账本保持specification
`ready`，implementation/technical/visual/consumer均`pending`，publication仍`unpublished`。
没有生产接入、安装、commit或push。

## 2026-09-20 工作档位过渡规格已冻结，只有 specification ready

`REIMU-WORK-TRANSITIONS-001`现已有可实施合同，见
`docs/decisions/2026-09-20-reimu-work-transitions-spec.md`。本轮重新fetch并核对Harness
`37d9384cc91ef3b3f0c349405d15f174f7c66c2f`与Consumer
`c2684cc3fecbdfbe0ae238a13f8e22fef333295d`均和`origin/main`一致；实际manifest继续证明
Tier2为16帧、10 fps、1.6秒循环，Tier1/3/4/5各为一帧125 ms静态保持。唯一档位边界仍是
`min(max(activeTaskCount, 0), 5)`。

规格冻结5个standing/fallback进入、5个退出和20个有向跨档逻辑身份；只有端点像素、摆放、
缩放、支撑线、方向、时序和取消点全部兼容并分别获原生视觉批准时才允许共享资源，当前没有
预授权共享。Tier2普通离开在有效过渡存在时等1.6秒安全边界，静态档离开不等待；高优先级
事件立即抢占，过渡中变化只读取最新观察状态，reduced motion直接选择目标代表帧。任何单路
资源缺失、摘要不符或加载失败只关闭该路并回到现有直接切换。

未来素材包固定使用596×596 RGBA、显式统一缩放和原生支撑线、`loop: false`、独立端点与帧
摘要、来源和reduced-motion声明；整图摇动、旋转、缩放、平移或交叉溶解不算角色动作，普通
cut/fade只能标作显示层衔接。历史`build/reimu-idle-meal-transition-20260907-v1/cut/`只可参考
摆放经验，不是本任务素材，像素不得复用冒充新过渡。

首个建议切片是`standing_to_tier_2`：新创作6–9帧、12 fps、500–750 ms的原始姿态或分层
序列，以批准站姿的确定性596端点回执起步，以Tier2 frame 0结束，再进入现有10 fps循环。
下一切片才是`tier_2_to_standing`，用于专门验证离开安全边界。本轮没有生成图片、manifest、
预览、Swift节点或App；implementation、technical、visual、consumer仍pending，publication
仍unpublished，也没有安装、commit或push。

## 2026-09-20 Tier1 Consumer 源码已发布，未安装

Consumer收口提交`c2684cc3fecbdfbe0ae238a13f8e22fef333295d`已推送至`origin/main`，
`git ls-remote`独立核对一致。发布范围包含`work_eating_task_1`、单一档位策略中的exact-count
one选择、安全循环边界、高优先级立即抢占、最新任务数恢复、独立摘要钉死静态包、隔离回退、
批准后构建门与测试文档。

源/base/frame仍为SHA-256
`8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e`，批准后manifest为
`ad9e4b9887359df3d2567d434ab169993b33e5026578e50351a0722c0624b84f`。没有安装应用、创建
tag或发布安装包；Tier1仍是一帧静态保持，不是多帧吃饭动画。详见
`docs/decisions/2026-09-20-reimu-tier1-publication.md`。

## 2026-09-20 Tier1 原生静态切片已获视觉批准，进入源码收口

用户查看`build/reimu-tier1-runtime-v1/runtime-preview/runtime-review.gif`、
`review-sheet.png`和`qa/native-size-review.png`后回复“收口”。批准绑定task_1原图
SHA-256 `8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e`
及已展示的原生大小、摆放、支撑/裁切、单帧静态保持、Tier1–5切换、高优先级抢占与最新
任务数恢复；不包含多帧吃饭动画、过渡、安装、tag或安装包发布。

Consumer manifest只更新批准说明，批准后SHA-256为
`ad9e4b9887359df3d2567d434ab169993b33e5026578e50351a0722c0624b84f`；图像与唯一帧摘要
不变。`--work-tier-1`生产构建门已释放，仍严格钉死manifest、身份、画布、播放与图像摘要。
批准后MacOSX26.5.sdk预览与`/private/tmp`临时正式身份双构建、严格签名、198项行为、37项
原生AppKit、125项Consumer工具（无跳过）、14项bridge、31项状态、Tier1–5各4项隔离回退、
表情3项、站姿5项、浏览器runtime、Consumer仓库门禁及Harness 674项聚合检查均通过。没有
安装应用；源码提交与远端核对已由上方发布记录完成。详见
`docs/decisions/2026-09-20-reimu-tier1-visual-approval.md`。

## 2026-09-20 Tier1 原生静态垂直切片技术预览完成，等待视觉确认

当前Tier2–5已发布，Consumer未提交工作区补入唯一缺失的exact-count Tier1：独立
`work_eating_task_1`身份和静态资源包只通过现有`PetBehavior.foodTier(activeTaskCount:)`
策略在真实`working + count=1`时选择。Tier2动态循环切入等待1.6秒安全边界，所有静态餐档
离开无额外等待；高优先级事件立即抢占，恢复读取最新任务数。Tier1资源损坏只降级Tier1。

596×596 RGBA源、运行时base、唯一125ms帧及普通/减少动态Harness输出逐字节相同，SHA-256为
`8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e`。没有重绘、分割、
缩放或整场摇动；这仍是静态保持，不是吃饭动画完成。

独立1.13/build15预览位于`build/reimu-tier1-runtime-v1/`。MacOSX26.5.sdk全新源码编译、稳定
ZIP全新解包与严格签名通过；198项行为、37项原生AppKit、125项Consumer工具、14项bridge、
31项状态、Tier1–5各4项加载回退、表情3项、站姿5项及仓库门禁通过。隔离截图覆盖Tier2动态
切入Tier1、全部五档、count=9封顶Tier5、needs_input抢占及最新count=4恢复，5次Tier1捕获
相同。160pt Tier1约118×137.5pt，支撑余量2.5pt且无裁切；较矮占地来自原稿伏桌姿态，未
人为放大。技术与Consumer接入已验证，用户视觉确认仍待完成；`--work-tier-1`强制preview。
没有安装、Tier1 commit、push、tag或发布。详见
`docs/decisions/2026-09-20-reimu-tier1-native-static-slice.md`。

## 2026-09-20 Tier5 Consumer 源码已发布，未安装

Consumer收口提交`d2b6bef76d9b5330f5e56a7ee61fbe86c6cdf9ac`已推送至`origin/main`，
并由`git ls-remote`核验远端`refs/heads/main`为同一SHA。提交包含已批准的独立
`work_eating_task_5`身份、唯一封顶策略下的5及以上选择、安全循环边界、高优先级抢占、
最新数量恢复、独立摘要校验/回退、资源包、测试与交接记录。

Tier5 runtime账本的publication门据此关闭。没有安装应用、创建tag或发布安装包；一帧
task_5仍是静态保持，不是多帧吃饭动画。完整边界见
`docs/decisions/2026-09-20-reimu-tier5-publication.md`。

## 2026-09-20 Tier5 原生静态切片已获视觉批准，正式打包门已解除

用户查看`build/reimu-tier5-runtime-v1/runtime-preview/review-sheet.png`、
`runtime-review.gif`与`qa/native-size-review.png`后回复“可以，收口后接着做”。本次批准绑定
原图SHA-256 `ffd3752c4cdf333a88dc70e766dc4fbdf584662bb242365b3a3ff8a2860f8342`和已展示的
原生大小、摆放、支撑/裁切、单帧静态保持、Tier2/3/4/5切换、5及以上封顶选择、
`needs_input`立即抢占及最新count=4恢复。这不构成多帧吃饭动画、额外过渡或安装批准。

Consumer资源manifest只更新批准说明，当前SHA-256为
`0b48b3730b2b26e6043af5a229bd0033fc6b97615e1d67dc14a4897cc4fd9a3f`，所有PNG与播放声明
不变。`build.py --work-tier-5`不再强制preview；批准后的preview与临时非preview门验证都
完成全新源码编译并通过严格签名。没有安装、tag或安装包发布。完整边界见
`docs/decisions/2026-09-20-reimu-tier5-visual-approval.md`。

## 2026-09-20 Tier5 原生静态垂直切片技术预览完成，等待视觉确认

Consumer当前未提交工作区新增独立`work_eating_task_5`身份和静态资源包。唯一
`PetBehavior.foodTier(activeTaskCount:)`策略继续将5及以上封顶为Tier5；真实count=4仍选
Tier4，没有复制第二处`>= 5`判断。Tier2动态循环切入Tier5等待1.6秒安全边界，Tier3/4/5
静帧离开无额外等待；failure、needs_input、点击、拖动和暂停立即抢占，恢复读取最新任务数。
Tier5资源缺失、manifest或摘要不匹配只降级Tier5，不影响其他档位、站立、手动吃饭或托腮。

现有596×596 RGBA源、运行时base、唯一125ms帧及普通/减少动态Harness输出逐字节相同，
SHA-256为`ffd3752c4cdf333a88dc70e766dc4fbdf584662bb242365b3a3ff8a2860f8342`。没有重绘、
分割、缩放或整场摇动；这仍是静态保持，不是吃饭动画完成。

独立1.12/build14预览位于`build/reimu-tier5-runtime-v1/`。MacOSX26.5.sdk全新源码编译、
稳定ZIP全新解包与严格签名通过；190项行为、36项原生AppKit、125项Consumer工具、14项
bridge、31项状态、Tier2/3/4/5各4项加载回退、表情3项、站姿5项及仓库门禁通过。隔离截图
覆盖Tier2/3/4、count=5、count=9封顶Tier5、needs_input抢占及最新count=4恢复，5次Tier5
捕获相同。160pt原生测量中Tier5约119.5×154.5pt，底部支撑余量2.5pt，无裁切；Tier2/3/4/5
同尺度差异均保留展示。技术与Consumer接入已验证，用户视觉确认仍待完成；`--work-tier-5`
强制preview。没有安装、Tier5 commit、push、tag或发布。详见
`docs/decisions/2026-09-20-reimu-tier5-native-static-slice.md`。

## 2026-09-20 Tier 4 Consumer 源码已发布，未安装

Consumer收口提交`aa820f07a1352f5e9291548f08187e408aada5bd`已推送至`origin/main`，
并由`git ls-remote`核验远端`refs/heads/main`为同一SHA。提交包含已批准的独立
`work_eating_task_4`身份、精确count=4选择、单一档位策略、安全循环边界、高优先级抢占、
最新数量恢复、独立摘要校验/回退、资源包、测试与交接记录。

Tier4 runtime账本的publication门据此关闭。没有安装应用、创建tag或发布安装包；一帧
task_4仍是静态保持，不是多帧吃面动画。完整边界见
`docs/decisions/2026-09-20-reimu-tier4-publication.md`。

## 2026-09-20 Tier 4 原生静态切片已获视觉批准，正式打包门已解除

用户查看`build/reimu-tier4-runtime-v1/runtime-preview/review-sheet.png`、
`runtime-review.gif`与`qa/native-size-review.png`后回复“可以”。本次批准绑定原图SHA-256
`9f0b18946eca4c7c0d27a8dbbd5f966da615867913d8e91c8454dd629de0b238`和已展示的原生大小、
摆放、支撑/裁切、单帧静态保持、Tier2/3/4切换、`needs_input`立即抢占及最新count=2恢复。
这不构成多帧吃面动画、额外过渡、安装或发布批准。

Consumer资源manifest只更新批准说明，当前SHA-256为
`c187f8d4390d4f082001c599dab6d2dbd8e699662c9a42cbe84bed9cd3300221`，所有PNG与播放声明
不变。`build.py --work-tier-4`不再强制preview，但本轮没有生成正式身份包，也没有安装、
commit、push、tag或发布。账本中intake视觉门已完成；runtime下一未满足门是publication。
完整边界见`docs/decisions/2026-09-20-reimu-tier4-visual-approval.md`。

## 2026-09-20 Tier 4 原生静态垂直切片技术预览完成，等待视觉确认

Consumer当前未提交工作区新增`work_eating_task_4`与独立静态资源包，只在真实
`working + activeTaskCount == 4`时选择；5及以上仍封顶Tier5 fallback。Tier2切入等待
现有1.6秒安全循环边界，Tier3/4静帧可立即离开；failure、needs_input、点击、拖动、暂停
仍立即抢占，恢复读取最新数量。Tier4资源缺失、摘要或manifest不匹配只降级Tier4。

现有596×596 RGBA源、运行时base和唯一125ms帧逐字节相同，SHA-256为
`9f0b18946eca4c7c0d27a8dbbd5f966da615867913d8e91c8454dd629de0b238`。没有重绘、分割、
缩放或整场摇动；这仍是静态保持，不是吃面动画完成。

独立1.11/build13预览位于`build/reimu-tier4-runtime-v1/`。MacOSX26.5.sdk全新源码编译、
严格签名与全新ZIP解包验证通过；181项行为、35项原生AppKit、125项Consumer工具、14项
bridge、31项状态、Tier2/3/4各4项加载回退、表情3项、站姿5项及仓库门禁通过。隔离截图
覆盖Tier2/3/4、needs_input抢占与最新count=2恢复，5次Tier4捕获相同。160pt原生测量中
Tier4与已批准Tier3支撑余量同为2.5pt，Tier4约117.5×148.5pt、Tier3约120.5×147pt；
Tier2更宽的既有跨档差异在同尺度图中保留。技术与Consumer接入已验证，用户视觉确认仍待完成；
`--work-tier-4`强制preview。没有安装、commit、push、tag或发布。详见
`docs/decisions/2026-09-20-reimu-tier4-native-static-slice.md`。

## 2026-09-20 Tier 3 正式包已补齐全新源码编译回执

已关闭下方Tier 3视觉批准与consumer发布记录中的本机Swift工具链缺口。默认macOS 27.0 SDK的
Swift接口由`swiftlang-6.4.0.31.4`生成，与当前编译器`6.4.0.34.1`补丁号不匹配；同一套
Command Line Tools内的macOS 26.5 SDK可被当前编译器正常导入。使用该SDK、`/private/tmp`
隔离模块缓存和已发布consumer commit `6a1318257d9bedc2b9a937304ea4b434ca874409`，已在
非preview模式全新编译1.10/build 12，无需安装或改动系统工具链。

新可执行文件SHA-256为`c4e59cc9311fd25e836f3d7c4bf55c3d2eefc66ad44d6cb09476c75a6f7d0ae0`；
正式本地ZIP `build/reimu-tier3-runtime-v1/release/灵梦桌宠-1.10-build12.zip` SHA-256为
`97c4708052e3aff9fe2a93e314446aeed0e16cbe9ee589f10c34450cac00a6d8`。全新解包通过严格
深层签名、正式身份及素材自检；172项Swift行为、31项状态契约、表情3项、站姿5项、Tier 2/3
各4项加载与隔离回退检查通过。旧复用二进制包保留在`release/legacy/`用于审计。没有安装、tag或
GitHub release；task_3仍是已批准静帧，跨档过渡和完整多帧动作仍属于独立后续工作。完整命令边界与
摘要见`docs/decisions/2026-09-20-reimu-tier3-fresh-source-build.md`。

## 2026-09-19 0.8.0 keyframe/pulse 与项目工作流完成本地收口

本条覆盖下方“技术门 pending”的早期状态。0.8.0 keyframe tracks、离散 pulse 曲线、schema/parser/
validator/docs/tests 与首版证据分层工作流作为同一完整源码快照收口；两个旧 installed-CLI acceptance
脚本不再硬编码0.5.0/0.7.0，而从`pyproject.toml`读取当前版本，并继续严格要求runtime、distribution、
CLI三者一致。完整决策与证据边界见`docs/decisions/2026-09-19-0.8.0-workflow-closure.md`。

验证结果：Harness完整M4/M5工程门通过（pytest、compileall、core/provider本地重装、pip check、diff、
离线acceptance）；M3 installed-CLI acceptance执行54条命令，单图/分层full与hold、0–4退出码和来源不变性
均通过；项目聚合门和layered smoke通过。consumer固定在已发布`d7394914fe2bffc5cec03d49c54d2d7285d56cd5`，
显式使用本仓0.8.0 CLI重跑125项工具测试全部通过，之前因CLI不可见而跳过的9项集成测试本次全部执行。
consumer工作区保持干净。

账本据此把`HARNESS-KEYFRAMES-001`与`HARNESS-WORKFLOW-001`的technical门标为passed，前者consumer门
标为verified；两者publication仍为unpublished。本条随本次本地提交收口，但没有push、tag、包上传、
真实provider调用或App安装；也没有把技术通过解释成灵梦新动作的视觉批准。下一项仍是
`REIMU-ACTIONS-001`：先用现有task_2做“2项任务＝持续吃饭”的端到端切片，再扩展六档、挂机饭团和抓取。

## 2026-09-19 引入证据分层的 Harness 项目工作流（本地草案）

参考 KLS 当前实践，把适合动画工程的部分落为可执行骨架：`workflow/tasks.json` 是唯一任务账本，
`workflow/update.py` 生成 `README.md`、`STATUS.md` 与 `TREE.mmd`；`scripts/verify.py` 运行项目视图、
空白检查、byte-compile、pytest 和一条 layered CLI smoke，并把命令、日志、Git身份、脏树状态及
前后源码快照写入忽略目录 `build/verification/`。来源、规则和发布流程见 `docs/workflow.md`。

六个门分别是 specification、implementation、technical、visual、consumer、publication。
程序测试通过不能自动批准视觉，Harness预览不能自动证明consumer原生接入，本地receipt/commit也不能
自动证明push或release。状态页从账本推导，不手填overall；依赖图同时保留文字和符号，颜色不是唯一信号。
发布前可从Git index生成视图，避免把无关未暂存工作吸收到状态文档。

初始账本如实记录三件事：工作流基础设施尚待最终技术receipt与发布；现有0.8.0 keyframe/pulse工作虽有
实现与文档但仍未据此宣称已发布；灵梦六档工作吃饭、挂机饭团与独立被抓取动作已有固定到consumer
commit `d7394914fe2bffc5cec03d49c54d2d7285d56cd5`的规格证据，但完整素材、技术QA、视觉批准、consumer
接入与最终发布仍是后续门。本文档条目不覆盖此前0.8.0与灵梦素材的未提交工作，也没有自动commit/push。

## 2026-09-17 睡眠短链固定背景修复及原生预览完成

本条覆盖上一版桌面稳定门禁失败状态。最终交付位于Harness `build/sleep-chain-stable-v2/`：
`preview.gif`、`review-sheet.png`、`睡眠短链预览.zip`、`release/`与qa/；其他reel/locked/final/stable为已否决中间实验，不用于后续。

- 不生成新脸或改变已确认sleep源；使用上轮imagegen四个关键帧和人工显式上/下场景合成。
  y<690来自关键帧，690–719为30px线性过渡带，y>=720完整复制选定睡姿；桌面/榻榻米位于固定区域。
  这是完整场景替换面板，不是自动分离头/手臂骨架。原始文件未修改；处理脚本prepare.py保留。
  早期内部面板有脸缘重影、硬切有发梢接缝，均未采用。最终仅下半场景锁定，不声称头部轮廓/所有袖子逐像素不变。
- verify.py检查60帧：替换区域外变化0；y>=720变化0（含RGBA）；sleep帧等于选定原图在透明底的合成；
  三个动态表情的RGB变化必须存在，防止把全静态误判成功。reduced60帧全部等于第一帧awake。
  Harness full/reduced校验通过，仍保留原图alpha=1散点的CONTENT_TOUCHES_EDGE，不声称零警告。
  查看过放大awake图与160px联系表；新动态神情/节奏尚待用户视觉确认。
- consumer新增preview-only `--sleep PACKAGE --sleep-chain --preview`；保留之前静态睡姿入口。
  右键“入睡/醒来短链（12秒）”或启动`--preview-sleep-chain`播放压缩预览，12秒后回站姿。
  五个资源槽（sleep/awake/yawn/drowsy/sleep）由FramePlan时间表选择；仍使用已批准睡姿摆放。
- 150项行为测试、34项原生自检、consumer仓库检查通过。喂食/拖动/失败/暂停/点击即时抢占；
  reduced原生预览冻结已选sleep静帧；不进入自动动作池。这里是手动短链，不代表真实5分钟空闲/75秒瞌睡已实现。
- App只在临时目录编译/自检，规避工作区fileprovider反复写FinderInfo的问题；严格签名通过，ZIP逐文件核验通过。
  正式1.9二进制摘要不变，没有安装、commit或push。未留下额外常驻桌宠。

剩余：本版过渡视觉确认；完整站立/托腮进入伏桌、醒来回站姿的身体动作；生产睡眠调度与唤醒抢占规则。
不能把压缩12秒预览直接当作自动睡眠链。原始选图及已确认静态原生摆放不需重复审批。


## 2026-09-17 睡姿原生摆放已确认，入睡/醒来关键帧预览 v1

用户反馈“合适，接着做”，因此selected睡姿及sleep-table-native-v1原生大小/摆放已确认，
不再待确认。已确认scale 0.8482811774958408、xFraction 0.0751829509829442、supportEdge 1207/1254。

本轮使用内置imagegen基于选定睡姿制作drowsy、yawn、awake三个候选，用户尚未逐一认可。
睡着源保持b05094ad…不变。完整来源、源摘要、只读差异检查见
Harness `build/sleep-chain-keyframes-v1/sources/`、`qa/source-audit.json`。
用公共Harness v2显式whole-scene互斥图层与hold keyframes串成12秒/5fps/60帧短预览：
睁眼→哈欠→困倦→短闭眼→半醒→伏桌睡着→半醒→睁眼。
`sequence.gif`、160px `contact-sheet.png`为视觉审阅产物；不是生产睡眠时长。
这是四张完整场景的互斥选择，不是身体分层骨架，也没有整场景呼吸/浮动或光流插帧。

验证：公共plan/render/validate通过；全运动60帧逐像素等于选中源在透明底的alpha-over合成，
reduced60帧全部等于首帧awake合成。full仍有已知CONTENT_TOUCHES_EDGE（选定源alpha=1散点），
reduced无警告。已查看160px联系表；未声称动态原生摆放已验收。
**美术稳定门禁未通过**：三张生成帧的下部场景(y>=820)各有约29.7–29.8万RGBA像素变化，
桌子/榻榻米被重绘；形态与色阶可能跳动。技术渲染通过不能当作视觉稳定或生产通过。
qa/verification.json明确production_ready=false。没有把候选接到App或自动睡眠池。

下一步先解决固定环境图层与头部关键帧的一致性，再实现/验证生产链；
保留既有设计要求：真实idle约5分钟后才可入睡，不能直接idle→sleep_table；
瞌睡阶段原设计约75秒，任何工作状态变化/交互应退出；失败/拖动等高优先事件不能等唤醒动画才处理。
暂停/系统睡眠取消，减弱动态冻结且不自动触发；恢复不得补播。以上是待实现规则，非本轮新增测试结果。
完整站立/托腮到伏桌的身体衔接、醒来恢复站姿、独立肢体骨架仍未完成。
正式1.9、consumer原生源码均未改；未新建App、未安装/commit/push，现有未提交修改保留。


## 2026-09-17 选定睡姿已完成原生静态预览，等待摆放反馈

使用用户选定exec-63c4aa0e原图，字节和眼口位置不变；无新绘画、无图像清理。
Harness `build/sleep-table-native-v1/` 包含 Sleep/source.json、base.png、公共plan/render/validate静态hold、
`睡姿预览.zip`、qa/、placement.json、receipt.json、before/与本轮integration.patch。

- consumer增加optional Sleep注册项与preview-only `--sleep PACKAGE`；精确锁定用户选图SHA，正式构建拒绝此参数。
- 右键“睡姿预览（静态60秒）”或preview的`--preview-sleep`入口；60秒后回站姿。
  使用preview身份；喂食、拖动、失败、点击可抢占，暂停/系统睡眠取消；减少动态保留同一静帧。
  这是手动静态摆放预览，不是完整睡眠动作，未加入自动池；base数据不伪造。
- 摆放根据alpha>1/255的可见边界测量：scale 0.8482811774958408、xFraction 0.0751829509829442，
  supportEdge 1207/1254；对齐已认可托腮的可见占地宽度/左边，并以站姿鞋线为支撑。
  只忽略边界测量中的alpha=1散点，不修改原图。尚未获用户原生摆放确认。
- 141项行为测试、33项原生自检、仓库检查通过；160/240/320/400/596可见边界和支撑线检查通过。
  已查看AppKit渲染的160px截图：完整桌子/榻榻米，选定脸和眼口比例保持。
  Harness渲染与选图逐像素一致，0错误；保留ZERO_MOTION（静态hold）和CONTENT_TOUCHES_EDGE
  （原图边缘alpha=1散点）两条警告，不声称零警告。实际alpha>1主体未被裁切。
- 项目目录的fileprovider反复写回FinderInfo，工作区App严格签名不稳定。临时目录的完整字节副本严格签名通过，已打成睡姿预览.zip；验证路径见qa/verified-location.json。工作区展开副本改名preview-bundle-source，避免作为额外App显示。
- 正式1.9安装版二进制摘要复核未变，未启动额外常驻预览，未安装、commit或push。

下一步：用户确认原生大小/支撑线后，为打哈欠→瞌睡→睡着→醒来补齐独立姿态/过渡素材和行为测试。
不要直接把静态睡姿加入自动池，也不要通过整张场景上下浮动假装呼吸；桌子/榻榻米应稳定。
完整分层骨架和睡眠链尚未完成。睡姿静态源在项目build中保存，不把历史被否决pose_prop骨架接回来。


## 2026-09-17 sleep_table 静态候选 v1，等待视觉反馈

用户明确授权进入新的睡姿阶段。内置imagegen以已认可double_cheek/idle_blink/base.png为编辑参考，
制作闭眼伏在桌面双袖上的静态候选，保留深棕发、红白蝴蝶结、圆桌和榻榻米方向。
交付：Harness `build/sleep-table-static-v1/candidate.png`（1254×1254 RGBA，真实透明alpha，边界未裁切），
同目录README.md、inspection.json、preview.html。生成原文件保留，未覆盖既有素材。
已看完整候选图；160/320px HTML预览已制作，但浏览器file URL被安全策略阻止，未完成浏览器小尺寸目检。
当前是完整静态单图，桌子/榻榻米也经生成重绘，不是逐像素锁定，不是分层骨架或动画。
用户尚未认可新睡姿。下一步先收集姿态反馈，再确定生产摆放与动画衔接；不把闭眼hold声称为完整睡眠链。
运行中1.9桌宠和既有资源未动；无commit/push。


## 2026-09-17 旧 App 已按用户要求清理

8个旧预览/中间构建/重复App已移入废纸篓；最近旧版展开回退目录也在压缩逐文件核验后移入废纸篓。
保留正式 `/Users/lyuyuwei/Applications/灵梦桌宠.app`（1.9/build11）与桌面指向它的快捷方式。
回退备份现在为Harness `build/slouch-production-integration/rollback-1.8-build10.zip`；
恢复时解压后将其中 `installed-1.8-build10.backup` 改回 `灵梦桌宠.app`，再按需替换。
清理清单和废纸篓位置见同目录 `cleanup.json`。源码、资源、截图、QA报告和窄补丁未删。
此前README中的candidate/preview/first-build App路径及展开backup路径现为历史证据路径，已不在原处；
依赖这些旧包的对比脚本不能直接重跑，应使用保留回执或从废纸篓恢复对应包。
正式版内容摘要与签名复核通过；未commit/push。


## 2026-09-17 用户确认后已安装 1.9 / build 11

用户回复“是”授权替换。正式路径 `/Users/lyuyuwei/Applications/灵梦桌宠.app` 已更新并启动，
启动回执确认preview=false、Slouch140帧/fallback none，standing140/eating40正常；启动后严格签名通过。
全部文件内容与已验证candidate一致，二进制SHA256为
`271e7de844950599cd6a1b5311e995e362d6b7f07e1f0c3c31ce85e7dacefc22`。
原1.8/build10完整保存在Harness `build/slouch-production-integration/installed-1.8-build10.backup`，
保留原应用身份/偏好设置路径，未改用户偏好。旧独立预览已退出，正式版已启动。
安装首次复制未保留执行权限，已按候选文件权限修复，再完成资源/启动/签名验证；资源字节未改。
证据：同目录 `installation.json`、`qa/installed-assets.json`、`qa/installed-launch.json`。
自动托腮已由确定性行为及原生自检验证；未等待随机挂机现场触发，不声称已完成长期观察。
本条覆盖此前“安装待确认/未替换”状态；没有commit/push。


## 当前接手摘要 · 2026-09-16（包发布 0.8.0：keyframe tracks + pulse 曲线，已安装未提交）

维护者明确授权把此前停在工作区的 keyframe 工作发布为 **0.8.0**。
（HARNESS.md 第 7 节的「No automatic commit, publishing or deployment」指的是工具不得自动发布；
本次是维护者要求的显式动作。）**本轮没有 commit、没有 push、没有打 tag。**

### 为什么现在发布

消费方 `gensokyo-codex-pets` 需要「同一组内恰有一个图层被合成」的语义来做眨眼。
已发布的 0.7.0 曲线只有 `ease_in/ease_in_out/ease_out/hold/linear/sine/triangle`，
没有一个能表达离散开关——连续曲线会让两个眼层同时半透明叠加。
不发布而直接安装工作区，会让消费方 manifest provenance 里的 `harness_version` 说谎
（记 0.7.0 却用了 0.7.0 没有的功能），所以必须升版本。

### 0.8.0 的内容（此前各轮留在工作区，本轮未新增功能）

keyframe tracks（`keyframes:[{at,value,interpolation}]`，与 curve track 字段严格互斥，
冲突报 `TRACK_MODE_CONFLICT`）、离散 `pulse` 曲线（duty 内 +1、其余 -1）、
`KEYFRAME_INTERPOLATIONS`、`sample_keyframes` / `keyframe_position` / `sample_track` 统一采样，
以及 schema、HARNESS.md、animation-plan.md、layered-sprites.md 的对应文档。
共 14 个文件、2716 行新增。**核心逻辑不是本轮编写的，本轮只做版本发布与验证。**

### 本轮实际改动

`pyproject.toml` 与 `src/sprite_harness/__init__.py` 0.7.0 → 0.8.0；
`HARNESS.md` 与 `README.md` 中描述「当前包」的两处版本说明同步更新。
`docs/roadmap.md`、`docs/architecture.md`、`docs/animation-plan.md`、`docs/renderer.md`、
`docs/layered-sprites.md` 里的 "M4/M5 … 0.7.0" 是历史陈述，**故意未改**；
`verification/m4-m5/release/` 是 0.7.0 的验证快照，同样未动。

### 验证

- 669 项测试通过。
- `pip install '.[dev]'` 后 CLI 与 runtime 均报 `0.8.0`，模块从 site-packages 解析；
  `SUPPORTED_CURVES` 含 `pulse`，`KEYFRAME_INTERPOLATIONS` 就位。
- **向后兼容确认**：消费方 eating `task_2` 在 0.8.0 下重建，`plan_digest`
  仍是 `sha256:f1571c6a101e34c2…`，与 0.7.0 逐字节一致——升级未改变任何既有产物。
- **新能力端到端确认**：消费方 slouch `pose_prop` 35 帧 / 5 fps 循环，
  经公共 CLI `plan → render → validate → preview → contact-sheet → report`，
  `warnings none`，`plan_digest sha256:7cdb6701858356b7…`；
  逐帧比对 `................................CC.`，闭眼恰在第 32/33 帧，
  且每帧与预期互斥合成**差 0**。

### 未完成

未 commit、未 push、未打 tag。是否提交这 14 个文件（含此前各轮未提交的工作）
需要维护者确认。

## 当前接手摘要 · 2026-09-07（1.7 / build 9 单一合并应用 + 监控探针，优先于全部历史记录）

用户本轮两项要求：「你还是发监控和探针吧」与「我的电脑里有多个灵梦App，我需要留下一个，
将他们的功能合并」。**前一轮「不发探针、不监控」的约束已被用户明确解除，本轮据此执行。**
**电脑上现在只有一个灵梦应用：`/Users/lyuyuwei/Applications/灵梦桌宠.app`，1.7 / build 9。**
安装版 1.3 已被它取代，但完整保留为还原点；没有删除任何文件。
本轮没有新绘图、没有改钩子信任、没有注入模拟事件、没有 commit/push、没有发布、没有派生任务。

### 唯一保留的应用

- `/Users/lyuyuwei/Applications/灵梦桌宠.app`，**1.7 / build 9**，
  bundle ID `local.reimu.onigiri.desktop`，名称 `灵梦桌宠`（不再是预览身份）。
  可执行文件 SHA-256 `8f05abc9efa2ec1d8b4104c501a9f1fd0f16cab0fceaeac78ee1bb5f7be359c6`。
  已启动并在运行；构建、安装后与启动后 `codesign --verify --deep --strict` 均通过。
- 构建记录 `/Users/lyuyuwei/.codex/artifacts/reimu-unified-20260907/灵梦桌宠.app`
  与安装副本**逐字节相同**。`~/Desktop/灵梦/灵梦桌宠.app` 是指向安装路径的符号链接，
  自动跟随本次替换，不是第二个应用。
- 资源与已批准 1.6 预览**逐字节相同**，且是 1.3 资源的严格超集（只多出已批准的
  `Standing/` 眨眼包）。**本轮没有生成任何新美术**，唯一站姿基准摘要复核未变
  （`4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7`）。

### 合并的实际内容

1.0 → 1.7 是同一份 `desktop/macos/` 源码的线性演进，**旧包没有 1.7 缺少的功能**。
历史上唯一被移除的行为是 1.3 的「工作中无限吃饭循环／自主咀嚼暂停」，
它此前已由用户批准的站姿默认与有限挂机吃饭取代，本轮未恢复。
所以合并 = 把预览身份承载的 1.6 功能集，用安装身份重建为 1.7，其余包全部归档。
1.7 的功能集：已批准站姿默认与每 7 秒 250 ms 眨眼、紧凑真实状态栏、真实 idle 60 秒后
25% 概率的 8 秒挂机吃饭与 180 秒冷却、右键 4 秒喂食、单击／双击／四连击生气、
拖动与落地、失败优先、暂停、减弱动态、休眠恢复、菜单与指针门禁。行为规则本身未改。

### 归档：17 个历史包，未删除任何东西

`/Users/lyuyuwei/.codex/artifacts/reimu-app-archive-20260907/`：`bundles/` 下 17 个包、
11 个不同可执行文件，按来源目录命名；`manifest.json` 记录原始路径／版本／bundle ID／
可执行文件摘要，全部与移动前一致；`scripts/restore.sh <archived_path>` 可按原路径还原，
不会自动执行。安装版 1.3 还原点为 `bundles/installed-1.3-20260906/灵梦桌宠.app`
（SHA-256 `31c9d9323a6d…`），另有同摘要副本在 `bundles/reimu-anger-20260906_release/`。
偏好域未改写：安装身份沿用它自己的 x=1227 / y=645 / 160 px；预览域原样保留但已无应用。

### 新增的观察能力

角色行为与工作接收器仍然分离。`PetBehavior.onTrace` 是默认 `nil` 的可选记录回调，
记录 base 变化、动作开始／结束（含 `completed`／`preempted_by_*`／`drag`／`left_idle`／
`failed`／`autonomy_off`／`cancelled`）、`meal_attempt`（真实 roll、是否命中、重试间隔）、
门禁与安静计时重置。**随机抽样次数与顺序未改，66 项既有行为检查逐项不变。**
`PetLog` 写 `~/Library/Logs/ReimuPet/behavior.jsonl`，逐行 JSON，1 MiB 上限、一代 `.1`
轮转；`--behavior-log PATH` 改路径，`--no-behavior-log` 关闭，QA 模式不写真实日志。
右键菜单新增真实倒计时一行（非闲置／被抑制／进行中／最早多少秒后尝试，并明示仍是 25%
概率）与「在 Finder 中显示行为日志」。**打开菜单本身是抑制门禁，会重置 60 秒安静计时**，
因此行为日志才是不打扰的观察方式；菜单该行工具提示已写明。

### 监控进程（已启动）

Harness `build/reimu-unified-monitoring-20260907-v1/watch.py`：只读工作快照与桌宠自己的
日志，按变化写 `~/Library/Logs/ReimuPet/watch.jsonl`，持续刷新
`~/Library/Logs/ReimuPet/watch-summary.json`（各状态累计秒数、可触发闲置秒数、挂机尝试
与命中、完成／被打断餐数、手动喂食与点击、门禁计数、首次自动吃饭时间、重启与缺失采样）。
首次观察到真实自动吃饭时发一条本地通知（`--no-notify` 关闭）。
本轮以 12 小时上限、5 秒采样启动，PID 在 `~/Library/Logs/ReimuPet/watch.pid`；
读取 `cat ~/Library/Logs/ReimuPet/watch-summary.json`，
停止 `kill "$(cat ~/Library/Logs/ReimuPet/watch.pid)"`。
交接时刻状态：25 次采样、全程 `working`、可触发闲置 0 秒、挂机尝试 0 次 ——
**因为有真实会话在工作，闲置尚未开始，仍无真实随机挂机结果。**

### 探针结果（全部是真实事件的只读核对）

- **钩子配置**：Codex 10 个、Claude 14 个观察钩子全部在位，无缺失、无外来钩子，
  非 `hooks` 键（`autoMode`）原样保留；钩子信任未改。见 `qa/probe-hooks.json`。
- **真实事件覆盖**：接收器数据库已有 2048 行真实事件。`working`、`round_ended`、
  `interrupted`、`closed` 已由真实事件驱动；**`needs_input` 与 `failed` 从未被真实事件
  驱动过** —— 前者需 `PermissionRequest`／受 matcher 限制的 `Notification`／
  `Elicitation`，后者需 `StopFailure`，这些类型至今 0 行。`PostToolUseFailure` 确实会到达
  （4 次），但 `observer.py` 故意映射为 `working`（工具失败可由代理自行恢复）。
  **本轮没有为了点亮这两个状态而制造任何事件。** 见 `qa/probe-event-coverage.json`。
- **监控与桌宠一致性**：同一批快照由原生 `--status-snapshot`、监控脚本和
  `observer.summarize` 三方评估，**48 次比较零分歧**，含畸形快照、缺失文件和真实快照副本。
  这次探针查出并修好了监控自身的缺陷：合法状态集漏了 `failed`，会把含失败会话的正常快照
  误判为损坏。见 `qa/probe-monitor-agreement.json`。

### 检查与仍未验证

行为 **84**（原 66 项不变 + 18 项记录检查）、原生自检 **29**（原 25 项不变 + 4 项日志检查）、
状态约定 **28**、生气素材 **3**、站姿素材 **5**、Harness **669**（exit 0）、
所选 `cut/` 重新验证零错误零警告、Consumer 仓库检查通过、两仓 `git diff --check` 干净。
证据在 Harness `build/reimu-unified-monitoring-20260907-v1/`（`README.md`、`unified.json`、`qa/`）。

**仍未验证：** 真实随机挂机的日常体感（监控在采集，尚无结果）；`needs_input` 与 `failed`
的真实事件路径；真实任务标题／工具说明／多任务列表／任务跳转；真正的起坐绘画、
悬浮／落地、瞌睡／唤醒。程序化通过不等于视觉批准。两仓大量既有未提交改动全部保留。

### 下一次接手提示

先 `cat ~/Library/Logs/ReimuPet/watch-summary.json` 看监控是否已捕捉到首次真实自动吃饭，
再按用户对 1.7 的反馈微调。没有新反馈时不要重跑已通过的检查、不要重新生成已批准素材、
不要恢复归档包。后续另阶段只选一个方向：真实任务信息接入，或真正起坐／悬浮落地／
瞌睡唤醒的独立绘画与视觉审核。安装替换与发布仍需用户明确要求。

---

## 历史接手摘要 · 2026-09-07（1.6 / build 8 独立预览，已被上方 1.7 单一合并应用取代）

用户在 8142 对齐换图预览后回复「可以，实行后完善交接文档并生成提示词」，
**已确认默认 `cut/` 直接切换、站坐大小／位置及 8 秒挂机吃饭，并授权独立原生接入。**
站姿眨眼 v1 与紧凑真实状态栏此前也已单独确认，不要再次按旧 pending 状态等待。
**本轮实现完成，最终 1.6 / build 8 独立预览已启动；安装版 1.3 保留，未安装替换。**
本轮没有新绘图、接收器／钩子修改、探针、监控、commit/push、发布或派生任务。

### 当前包、素材与阅读入口

- 当前唯一最终候选：
  `/Users/lyuyuwei/.codex/artifacts/reimu-native-idle-meal-20260907-final/灵梦桌宠预览.app`。
  版本 **1.6 / build 8**，bundle ID `local.reimu.onigiri.preview`；沿用独立预览偏好。
  可执行文件 SHA-256：`4d50588b44a4a397d8c107788fc0dc6e35f8405b11fc415bea087cae1955efb4`。
- 同日 `reimu-native-idle-meal-20260907/` 是中间构建，**不是最终包**，已停止进程并保留文件。
  旧 `reimu-native-standing-20260907/` 的 1.5/build 7 也完整保留，由最终候选接替。
- 已安装 `/Users/lyuyuwei/Applications/灵梦桌宠.app` **1.3** 的全部 47 个文件保持原摘要。
  不得将视觉批准或“实行”解释为覆盖安装版的授权，安装仍需用户明确要求。
- Harness：`AGENTS.md` → `HARNESS.md` → `docs/handoff.md`。
  Consumer：`AGENTS.md` → `HANDOFF.md` → `desktop/README.md`，再读
  `docs/desktop-experience.md` 与 `docs/reimu-action-system.md`。
- 唯一站姿：Harness `build/reimu-neutral-20260906/selected-v1/neutral-standing.png`，
  原 1254×1254 RGBA，SHA-256
  `4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7`。
  选择记录为 `build/reimu-neutral-20260906/selection.json`，选择的是
  `exec-cb15409b-d9b0-4f49-81e5-79fc95f28591.png`，不是后来全白袜版本。
- 已批准眨眼源：`build/reimu-neutral-idle-blink-20260906-v1/final/` 与 `reduced-final/`；
  三张原眼姿、140 帧／20 fps／7 秒，闭合过程 250 ms。身体／alpha／画布／脚底不变。
- 已批准站坐预览：`build/reimu-idle-meal-transition-20260907-v1/cut/`；`fade/` 未选定，
  `dissolve/` 因双脸重影已否决；不按修改时间选择。
  原网页 8142 是一次性 12 秒示范，不是原生定时循环器。
  收尾检查：8142 返回 HTTP 200；旧 8140／8141 当前未运行，本轮无需恢复，素材仍保留。
- 本轮证据：Harness `build/reimu-native-idle-meal-20260907-v1/`，含 `approval.json`、
  `README.md`、`next-session-prompt.md`、`qa/`。下一次接手提示词已生成在该目录。

### 实际原生行为

- 默认仍为已确认站姿／低频眨眼。只有真实 `idle` 连续安静 60 秒后才首次尝试挂机吃饭；
  每次命中概率 25%，未命中则等随机 30–45 秒再尝试；迟到的时钟只尝试一次，不补播。
- `idle_meal` 单次 8 秒，原 40 帧／4 秒精确两轮；结束直接回原睁眼站姿并续低频眨眼。
  完成或被打断的自动／主动吃饭均阻止下一次自动吃饭至少 180 秒；每次互动及动作结束
  还要求重新安静 60 秒，取两项限制中较晚者。冷却是本进程内单调时钟，不跨退出持久化；
  重启后仍须新的真实闲置 60 秒。手动喂食不受自动冷却限制，重复请求不排队。
- `working`、等待输入、失败、轮次结束、未知、断连均不自动吃饭；`round_ended` 不冒充
  真实闲置。自动吃饭中收到非 idle 状态立即回站姿；真实状态／任务数从不被动作写入。
- 右键喂食保留 4 秒一次；点击可打断自动吃饭，双击、四连击生气、锁定／冷却保持。
  失败立即打断所有反应；拖动立即接管，放下后回最新工作状态。
- 暂停、系统／应用减弱动态、休眠取消自动吃饭；恢复后重新等待，不补播。
  鼠标按住或菜单打开期间不触发自动吃饭，结束后重新等待；素材校验降级也禁用自动吃饭。
- 坐姿与生气图统一沿用已批准的整体等比定位：在 596 参照画布中原 688 方图显示为
  482 方图，Harness bottom_center 偏移 x=2.796511627906966、y=63.26162790697674。
  AppKit 对应 rect=(59.796511627906966, -63.26162790697674, 482, 482)，按窗口宽/596
  等比缩放；命中检测也反算同一个 rect。原 688 图与 1254 站姿按原字节打包，没有重采样源。
- Harness 预览 alpha 支撑边缘 bottom=585；原生使用 AppKit 高质量采样，在 Retina／缩小
  输出中极低 alpha 抗锯齿边缘可有数像素差别，**不称与 Pillow 逐像素一致**。
  鞋底与坐姿裙摆／阴影支撑边缘在视觉上对齐；不是人体脚踝骨架、完整人体分层或绘制起坐。

### 检查、证据边界与下一步

- 本轮 **66 项行为、25 项原生窗口／菜单／计时器、28 项状态约定、3 项生气素材、
  5 项站姿素材**检查通过。挂机边界使用隔离时钟／随机源；不向真实快照注入测试事件。
- Harness 全套 **669 项**通过；所选 `cut/` 重新经公共 CLI/JSON 验证零错误零警告，
  显式 `PYTHONPATH=src`；Consumer 仓库检查及两仓空白检查通过。
  最初系统 Python 缺 Pillow，随后使用既有 Harness `.venv/bin` 重跑仓库检查通过，未安装依赖。
- 最终包构建和启动后 `codesign --verify --deep --strict` 通过。
  Documents 的 `.app` 曾被文件提供程序重加 FinderInfo 而验签失败，因此继续输出到
  `.codex/artifacts`；构建器只清理新输出的 FinderInfo／ResourceFork，不清理来源。
- 制作者查看原生绘制导出的 596／160 px 浅深底对照：`qa/native-comparison-*.png`；
  透明通道、坐姿大小与支撑位置正常。CUA 已打开最终包并看到站姿及真实“工作中 · 2 项”。
  中间构建的右键喂食按钮实际执行后卡片仍为 2 项；CUA 随后选中了状态框窗口，
  因而未捕获这一次真人桌面坐姿全过程，不能冒称已经完整人工验证原生自动挂机。
- 原生自动 8 秒完整生命周期、抢占与恢复已由程序化测试覆盖，**真实闲置随机触发的
  长期体感和最终原生组合尚留用户日常查看**；不安排监控，不重复索要已批准网页视觉。
- Claude 基础连接此前已用真实日志验证；本轮未重复检查。完整审批／失败／重连链路仍
  未全面验证。真实任务标题、工具／文件说明、活动条目列表和跳转仍未实现。
- 下一步先依用户对 1.6 的反馈微调；若无问题，再单独选择一个后续动作或真实任务信息
  接入阶段。真正起坐姿势需另画另审，不一次展开完整动作库，不自动安装。
- 两仓大量既有未提交改动保留。本轮只改 Consumer 行为／窗口／构建版本／行为测试与
  相关文档，以及 Harness 交接和新 build 证据。工作接收器、WorkStatus、StatusBubble、
  源素材和旧安装包保持原摘要；没有声称 GitHub 已同步。

---

## 历史接手摘要 · 2026-09-07（1.5 与待审换图阶段，已被上方 1.6 取代）

用户在 596／160 px 浅深底播放与关键眼姿展示后回复「可以」，**已明确确认站姿眨眼
v1 的眼型与每 7 秒一次、250 ms 的节奏，并授权接入独立原生预览**。
紧凑状态栏也已确认。**默认站姿现已接入 1.5 / build 7 独立预览并启动；未替换安装版。**
原生组合效果仍由用户查看，不把程序检查或网页站姿批准称为新版安装批准。
下方旧记录中的版本、Claude 延期、站姿眨眼 pending 和旧默认吃饭规则均不能覆盖本摘要。

### 本轮最新推进：有限吃饭与换图衔接预览

用户回复「那就往下做」，授权继续下一阶段。本轮已制作并打开
[离线动作预览](http://127.0.0.1:8142/)，目录为 Harness
`build/reimu-idle-meal-transition-20260907-v1/`。**当前候选是 `cut/` 与 `fade/`，
减弱动态为 `reduced/`；仍待用户确认大小、时长与衔接方式，未接入原生挂机调度。**

- 完整片段 12 秒／240 帧／20 fps，只播放一次：站立 2 秒、进入 200 ms、吃饭 8 秒
  （原 40 帧／4 秒循环精确播放两次）、返回 200 ms、恢复站立 1.6 秒并保持。
- 596 px 共用画布。站姿等比缩放 `596/1254`；坐姿等比缩放 `482/688`，位置偏移
  x≈2.797、y≈63.262 px（Harness bottom_center 变换坐标）。全部帧 alpha 支撑边缘
  bottom=585（最低可见 y=584），无整图上下浮动。站姿以鞋底、坐姿以裙摆／阴影
  支撑边缘对齐，**不是已确定共同人体脚踝或脚底的骨架锚点**。
- `cut/` 是对齐后直接切换（页面默认）；`fade/` 是 200 ms 淡出淡入，每帧仅有一个
  完整姿势可见。**两者均为换图方式，没有新绘制的起坐中间姿势，也不是人体分层。**
- 早期 `dissolve/` 虽结构通过，但制作者在第 42 帧看到双脸重影，已否决并从页面选项
  移除，保留为诊断记录；不得把它当选定方案，见 `qa/dissolve-rejected.json`。
- 所有缩放／定位／透明度与帧序均走 Harness 公共 CLI/JSON，显式 `PYTHONPATH=src`；
  本轮无新绘图、无付费 API，原基准与现有吃饭帧不可变。Pillow 只做预览尺寸导出及像素 QA。
- 当前候选 full／hold 均零错误零警告；导出 596／160 px 的动画与静态减弱动态展开后
  共 1440 帧逐像素核对通过，APNG 完整片段仅播放一次。减弱动态的导出是普通静态 PNG，
  不冒称保留了动画帧块。浏览器查看浅／深底、切换中间帧、播放结束保持站立、减弱动态；
  375/414/768/1024/1440 px 页面均无横向溢出，160 px 对照不缩小。

挂机节奏只记录为草案：连续闲置 60 秒后考虑，每 30–45 秒尝试、25% 概率触发，
吃完冷却至少 180 秒。页面不运行调度，不接工作接收器，不显示虚构任务状态／数量。
**下一步先确认本预览，再接独立原生调度**，届时保留右键喂食、失败优先、暂停、
减弱动态、点击冷却、四连击、拖动恢复及动作结束解析最新状态；若用户需要真实起坐动作，
须另用内置 imagegen 绘制并审核完整过渡姿势，不能将本轮淡入淡出冒充该成果。

当前原生预览仍是下述 **1.5/build 7**，安装版 **1.3** 不变。下面原生 37/23/28/3/5 项
检查是上一阶段证据，本轮未修改或重跑原生状态机／接收器；Claude 基础连接不重复验证。
本轮记录、复现命令与保留检查见新目录 README、`qa/`。未安装、commit/push、发布或派生任务。
本轮 Consumer 仓库检查及两仓 `git diff --check` 通过；安装版 1.3 的 47 个文件、
当前原生 1.5 的全部文件、选定基准和 Consumer 运行时代码保持原摘要。


### 阅读入口与当前产物

- Harness：`AGENTS.md` → `HARNESS.md` → `docs/handoff.md`。
- Consumer：`AGENTS.md` → `HANDOFF.md` → `desktop/README.md`，再读
  `docs/desktop-experience.md` 与 `docs/reimu-action-system.md`。
- **当前独立原生预览**：
  `/Users/lyuyuwei/.codex/artifacts/reimu-native-standing-20260907/灵梦桌宠预览.app`，
  **1.5 / build 7**，bundle ID `local.reimu.onigiri.preview`。沿用独立预览偏好，
  与安装版偏好隔离；本轮实际查看 160 px 人物并展开卡片。
- 当前可执行文件 SHA-256：
  `8e6d48caf177eee2ffdb1ab4c540145260ede092023e89d80394fcdcf359a73d`。
- **保留安装版**：`/Users/lyuyuwei/Applications/灵梦桌宠.app`，**1.3**；未覆盖、未退出。
  上一份 `.codex/artifacts/reimu-compact-status-20260907/灵梦桌宠预览.app`
  **1.4.1 / build 6** 完整保留，已被本次站姿预览取代为当前候选。
- 本轮授权、导入、检查与保留证据：Harness
  `build/reimu-native-standing-20260907-v1/` 的 `README.md`、`approval.json`、`qa/`。
  上轮网页重新展示证据在 `build/reimu-standing-review-20260907/`；其 pending 是当时快照。

### 实际运行行为与范围

`PetBehavior.swift` 单独负责角色行为；`WorkStatus.swift`、工作接收器、
`StatusBubble.swift` 和钩子信任均未改。默认外观为站姿：工作中、已观察闲置、轮次结束
使用已确认的低频眨眼；等待、失败、中断、未知或从未观察到事件保持原睁眼站姿。
这些状态的含义和真实计数不因人物站立而改变。普通点击／双击使用站姿眼部帧，
拖动与放下保持站姿静帧；没有新增飞行或落地绘画。

右键喂食仍使用已审核 40 帧、4 秒吃饭素材，一次播放后解析最新状态并回到站姿。
四连击仍显示原已审核坐姿皱眉、红色怒气符号与「むっ！」1.2 秒，点击锁定和冷却保留。
失败优先、暂停、减弱动态、系统休眠恢复和拖动恢复保留；减弱动态保留文字反馈、
保持原站姿。站姿／吃饭／生气各自使用正确 alpha 画布作命中判断。

**工作状态不再驱动无限吃饭循环**，原工作中偶尔暂停咀嚼的调度已随默认站姿移除。
本轮尚未启用自主挂机吃饭；吃饭作为偶尔的有限时长活动仍需下一阶段独立预览。
目前喂食／生气与站姿之间是直接换图，没有声称已绘制起坐过程或完成脚底共用锚点。
不将平面图裁块当人体分层。食物档位公式与 35 动作 JSON 设计登记表未改。

紧凑卡片保留 160/240/320/400 px 人物对应 208/240/280/280 pt 宽、60 pt 高、
28 pt 按钮及展开／收起、边缘定位。**仍只显示真实通用状态和数量；真实任务标题、
工具／文件说明、多任务列表与任务跳转尚未实现。** 网页框体示例文字不是事件接入。

### 唯一美术基准与导入

唯一选定基准：Harness `build/reimu-neutral-20260906/selected-v1/neutral-standing.png`，
1254×1254 RGBA，SHA-256
`4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7`。
选择记录 `build/reimu-neutral-20260906/selection.json` 指定
`exec-cb15409b-d9b0-4f49-81e5-79fc95f28591.png`；不是后来的全白长袜稿，勿按修改时间选图。

已确认眨眼来源仍为 `build/reimu-neutral-idle-blink-20260906-v1/` 下
**`final/` 与 `reduced-final/`**，不是旧 `full/`、`reduced/`。
本轮 Consumer `desktop/macos/import_standing.py` 通过显式 `PYTHONPATH=src` 的 Harness
公共 CLI 只读复验两套构建，核对已批准 plan digest 与全部帧摘要，再按文件字节
去重复制成新 Harness build 的 `Standing/`：三张 1254 px 原始 PNG + 140 帧／20 fps 清单。
没有重画、重渲染、重采样或改变 alpha、画布、身体及脚底；打包后再次核对摘要。
原生启动校验清单与 PNG，闭眼文件损坏时明确退到已验证原站姿并在菜单提示，
原站姿丢失则拒绝启动；不会悄悄改用别的立绘。

- [站姿网页预览](http://127.0.0.1:8140/) 保留；其 pending 文案是原构建快照，批准以本摘要
  与新 `approval.json` 为准。未为改状态而覆写旧美术构建。
- [网页状态框示例](http://127.0.0.1:8141/#desktop) 保留，仅供样式参考。
- 上轮两服务 HTTP 200，本轮未重建网页。若 8140 停止，从 Harness 根运行
  `.venv/bin/python -m http.server 8140 --bind 127.0.0.1 --directory build/reimu-neutral-idle-blink-20260906-v1`；
  8141 同理使用 `build/reimu-status-bubble-20260907-v1`。

### 检查结果与证据边界

- Harness full／hold 公共 CLI 验证均零错误、零警告，原帧时序与全部摘要匹配。
- 行为状态机 **37 项**通过；原生窗口／菜单／计时器 **23 项**通过，含四档卡片尺寸、
  27 种屏幕位置、两套图像及 alpha 选择、暂停、减弱动态、拖动位移和恢复。
- 原生状态约定 **28 项**、生气素材 **3 项**、站姿正常／损坏／缺失素材 **5 项**通过。
- CUA 实际查看 160 px 站姿和展开卡片，显示真实「工作中 · 2 项」；实际右键喂食后
  截图确认回到站姿，卡片前后仍为 2 项。没有发送探针或向真实状态注入测试事件。
  原生 self-test 使用隔离 QA 偏好，状态约定测试仅用临时快照。
- 本轮物理拖拽手感未重新人工验证；不能用程序位移检查替代。原生整体搭配仍待用户查看。
- Documents 内开发包曾重新出现 FinderInfo 导致严格签名失败，来源未确定。
  新包按约定构建在上述 `.codex/artifacts` 路径；构建时和 CUA 启动后严格验签通过。
  构建器只清理新输出的 FinderInfo／ResourceFork，不清理源素材元数据。

### 下一步与保留约束

本轮默认待机接入完成，当前独立预览留给用户查看；安装替换仍需用户明确要求。
有限吃饭与换图衔接预览已完成，见顶部本轮推进；确认候选后再接入调度，真实起坐绘画仍未制作；
不一次展开拖拽悬浮、落地、瞌睡和唤醒。真实任务元数据及跳转是独立工程缺口。

Claude 此前延期已解除，基础连接已有真实日志验证。本轮没有重复连接检查、发送探针、
改配置／钩子信任或安排监控；完整审批、错误与重连路径仍未全面验证。
新绘图用内置 imagegen；已授权 Pillow 抠图和眼部补丁，可运行 matte 脚本为
`selected-v1/matte.py`。本轮没有生成任何新美术。

Consumer 编辑前 fetch 成功；两仓大量既有未提交工作保留。未 commit/push、发布素材、
派生任务或调用子代理。Consumer 仓库检查及两仓 `git diff --check` 通过；安装版 47 个
文件、旧 1.4.1 预览、选定基准与原眨眼构建全部文件摘要保持不变，既有工作仅本轮
列出的源码／文档变更。完整清单见本轮 `qa/preservation.json`。

---

以下为保留的历史记录，请按顶部摘要解释其当时状态。

## 2026-09-07：状态栏缩小至紧凑版，Claude 连接验证已恢复

用户反馈状态栏太大，并通知「我的 Claude 可以连接了」。当前预览升级为
**`~/.codex/artifacts/reimu-compact-status-20260907/灵梦桌宠预览.app`**，1.4.1/build 6；
旧 1.4 包保留但已被取代，安装的 1.3 不变。160/240/320/400 px 人物分别配
208/240/280/280 pt 宽的状态框，框高 88 → 60、按钮 36 → 28，总高 136 → 96；
字体改为 14/12 pt，并缩小内边距。20 项原生检查通过，包含四档尺寸与 27 种屏幕位置。

**Claude 的此前延期已被用户本次通知解除，已恢复基础连接验证。** 配置中已有
14 种接收器钩子，已安装接收器脚本与 Consumer 源码摘要一致；只读事件日志确认近期收到
真实 UserPromptSubmit、16 对 PreToolUse/PostToolUse 和 Stop。Claude 界面也显示已
完成的 16 条命令响应。UI 的本地会话 ID 与钩子会话散列不是同一标识，不声称
已完成 ID 映射。未新建 Claude 任务、发送探针、注入事件或改配置；本次结论限于
近期基本生命周期接收，未覆盖全部审批、错误或重连路径，也未安排监控。

本轮记录与 QA：`build/reimu-compact-status-claude-20260907/`。仅缩小原生 UI，
没有改原画、站姿眨眼、工作接收器、角色行为状态机或真实状态。Consumer 编辑前
fetch 成功，两仓既有工作保留；未 commit/push 或发布。常态站姿与挂机吃饭衔接仍待后续。

## 2026-09-07：原生任务状态框 1.4 独立预览已完成

用户要求继续后，Consumer 已实现原生两行深色状态框：真实状态／活动数量、未知
提示、展开／收起、独立折叠偏好和屏幕边缘位置调整。框体是跟随人物的独立浮窗，
收起不移动人物或按钮锚点、不重启动画；透明角落和空隙可穿透。
当前实际显示通用工作状态，没有冒充任务标题、具体操作、活动列表或任务跳转。

本轮记录目录 `build/reimu-native-status-bubble-20260907-v1/`；唯一当前可运行包为
**`~/.codex/artifacts/reimu-native-status-bubble-20260907/灵梦桌宠预览.app`**，
版本 1.4/build 5。build 根部和 preview 子目录中的两份应用均为已取代的开发候选。
预览 bundle ID／偏好与已安装版本分开。
原生 1.3 未覆盖；全部 47 个安装文件摘要不变。现有审核吃饭／生气素材原样复用，
没有重画、改 alpha、导入待确认站姿或启用新的挂机吃饭调度。Harness core 未改。

最终原生检查 19 项（含 27 种框体屏幕位置）通过，行为 30 项、状态 28 项、表情
加载 3 项通过。CUA 实际验证展开／收起、真实数量从 2 变 1、160 px 人物选择。
物理拖拽手感仍需人工检查，不与原生位移／布局检查混淆。新应用目录起初带有
FinderInfo 导致签名拒绝，已让构建器仅清理新产物的两种签名不兼容元数据；
Documents 中的包启动后又出现 FinderInfo／FileProvider 标记并再次验证失败，
未确定具体是谁加回属性。可运行包已改在上述本机目录重新构建；详见本轮 README
与 `qa/packaging-note.json`，不能把早期仅构建时的签名通过当作后续稳定性证明。
最终本机目录包在 CUA 启动后再次通过严格签名验证，根目录仅余 provenance 属性；
摘要／全部原文件保留检查及最终记录见 `qa/preservation.json`、`qa/verification.json`。

两仓既有改动保留，Consumer 编辑前 fetch 成功。未改工作接收器、行为状态机、
钩子信任或真实工作快照，未 commit/push／发布素材。Claude 继续延期，未启动检查、
重试或监控。接下来确认原生框体搭配与常态眨眼，再接默认站姿及有限时长的挂机吃饭。

## 2026-09-07：吃饭／喂食版本归入挂机动作库

用户明确：「可以，我打算把灵梦吃饭喂食这一版本做成挂机动作之一」。后续以已选
常态站姿／低频眨眼为默认待机，保留当前吃饭版本作为偶尔触发的挂机活动，右键
喂食仍为主动入口。吃完回到最新状态；仍闲置时回站姿。吃饭允许在没有工作任务时
发生，不据此更改任务数或推断任务状态。

已更新 Consumer `docs/reimu-action-system.md` 顶部最新决定、
`docs/desktop-experience.md` 和 HANDOFF。旧 `work_eating`／档位限制已注明属于之前的
工作量与静态图集方案，不作为未来挂机吃饭的门槛。此次仅固定设计方向，没有改
运行时／JSON 登记表、工作接收器、素材或原生 1.3 安装。原吃饭和生气素材完整保留；
频率、时长、站坐衔接待后续独立预览。常态眨眼仍按原流程单独确认，动作逐阶段推进。

文件保留与检查记录在 `build/reimu-idle-meal-decision-20260907/`；Consumer 编辑前
fetch 成功。未 commit/push 或发布，Claude 继续延期，未检查、重试或安排监控。

## 2026-09-07：框体外观已确认，整体体验对齐 Codex 桌宠

用户看过状态框后回复：「可以，这个其实我想做的跟Codex的桌宠系统一个样子」。
**状态框外观确认已获得**；下面旧记录中「框体未确认」的部分被本条取代。
目标包括悬浮角色、可收起任务卡片、多任务活动列表与点击返回任务，沿用现有独立
灵梦应用和已确认互动。详细对照见 Consumer `docs/desktop-experience.md`。

本轮核对官方 Pets 产品说明、本机随附图集契约及现有 Consumer 状态代码。现有真实
事件仍缺任务标题、操作说明和可跳转任务标识；预览示例没有变成真实接入。
下一次原生框体先使用真实通用状态，具体标题／操作／跳转待来源验证；本轮未改
运行时、优先级、素材、钩子或安装应用。常态眨眼尚待原先要求的单独视觉确认，
原生 1.3 保留。动作继续逐阶段推进，不同时展开悬浮、落地、瞌睡、唤醒。

本条及 Consumer 体验说明／交接为本轮改动，批准和文件保留证据在
`build/reimu-codex-experience-20260907/`。Consumer 编辑前 fetch 已成功；未 commit/push、
未发布素材。Claude 继续延期，未检查、重试或安排监控。

## 2026-09-07：新增截图式圆角任务状态框预览

用户在常态眨眼 v1 之后提出希望有截图那样的框框。已制作
[独立状态框预览](http://127.0.0.1:8141/#desktop)，详情见
`build/reimu-status-bubble-20260907-v1/README.md`。深灰胶囊、白色标题、灰色操作说明、
收起／展开、长文本省略与手动状态示例均可查看；收起保留占位，人物不挪位置。
复用上一轮导出 PNG 与精确帧序，图像摘要不变；没有重新生成美术或改动 Harness core。
浅／深底、160／320 px、375–1440 px 页面及文字／收起控件已检查。

**框内是明确标注的示例文字，未接入真实任务。** 只读核对 Consumer 接收器和
WorkStatus 后确认目前只有状态／数量，没有任务标题、工具说明或文件名；不得将
「正在读取 handoff.md」示例冒充真实事件。真实元数据桥接留到后续接入阶段。
本框体与常态眨眼均未获用户视觉确认、未安装，原生 1.3 保留；两个仓库仅更新交接，
既有修改保留，未 commit/push 或发布。Claude 仍按用户要求延期，未检查／重试／监控。

## 2026-09-07：选定常态站姿的待机眨眼 v1，待视觉确认

本轮按用户指定的 `selected-v1/neutral-standing.png` 唯一基准完成独立预览；没有采用
后续全白长袜稿，也没有安装到原生桌宠。阅读
[本轮 README](../build/reimu-neutral-idle-blink-20260906-v1/README.md)、
[预览](http://127.0.0.1:8140/) 和 `qa/animation-qa.json`。目录日期保留本轮开始的 09-06。

内置 imagegen 分别画半闭眼／闭眼，原始 RGB 草稿与提示词已保存；仅取两个明确眼区，
Pillow 合回用户选择的 1254×1254 基准。所有原始文件未改，基准 SHA 仍为
`4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7`。
三张完整姿势通过 Harness v2 的互斥 opacity 关键帧切换，**不是人体解剖分层**。
20 fps／140 帧／7 秒循环，眨眼 250 ms；身体、画布、原有脚底位置固定，无上下浮动。

当前构建明确为该目录 **`final/`** 与 **`reduced-final/`**。完整／减弱动态公共 CLI
plan/render/validate 和 preview/contact-sheet 已运行，零错误零警告；原尺寸逐帧 RGBA
与对应姿势一致，alpha 固定，首尾 PNG 字节相同，减弱动态全部保持原睁眼。
眼区动态并集 7,745 像素，眼区外改变 0；bbox `[353,39,932,1230)`、脚底 y=1229。
596／160 px APNG 解码 RGBA 精确相同，WebP 仅全透明隐藏 RGB 被编码器清零；可见 RGB
及 alpha 精确相同。浏览器已检查浅／深底、两种尺寸、关键姿势、触发播放及减弱动态。
这些是结构／制作者检查，**用户视觉批准仍 pending**。

早期 `full/` 覆写重跑后出现缺帧及非预期的 ` 2` 后缀文件，原因未确认；已保留但废弃，
没有拿旧 QA 当成当前通过。用全新输出目录完成最终检查，详见 `qa/discarded-runs.json`。
调用当前 checkout 的公共 CLI（显式 `PYTHONPATH=src`）；未修改 Harness core。

Consumer 仅更新交接；已安装的 1.3、行为／工作接收器、钩子信任与真实状态不变。
Claude 按用户明确要求延期：没有检查、重试或监控。两仓既有未提交修改保留，
本轮未 commit/push、未发布素材。下一步先让用户确认此预览，再决定原生接入；
拖拽悬浮／落地与打瞌睡／唤醒尚未展开。
最终独立文件／像素完整性核对及 Consumer 仓库检查通过，两仓 diff whitespace 检查通过；
除交接外既有工作区文件摘要未变，已安装应用全部 47 个文件摘要未变。证据见本轮
`qa/final-integrity.json`、`qa/workspace-after.json`、`qa/browser-review.json`。

## 2026-09-06：常态站姿立绘迭代，尚未安装

**当前选择修正：用户更喜欢 `exec-cb15409b-d9b0-4f49-81e5-79fc95f28591.png`。**
这是第 4 版第一次裙摆编辑，仍露少量小腿、袜口较短；后续长袜覆盖露出小腿的版本
未选用。已另存 `build/reimu-neutral-20260906/selected-v1/`，当前透明图为其中
`neutral-standing.png`，选择与摘要见上级 `selection.json`。透明图已检查浅/深底及
596/160 px；后续以 selected-v1 为当前视觉基准，不以修改时间挑选 revision-4 最后一张。
此反馈是当前版本偏好，未安装到 1.3 桌宠，也未批准整套动画或完整模型表。

**最新第 4 版：用户澄清裙子长是覆盖更多既有小腿，另要求两只袜子更长、更随意。**
两次内置 image_gen 编辑后，裙摆向下覆盖小腿，袜筒延伸到裙摆下方并带松褶；
保持原人物身高/腰线和此前加大的鞋子。最新本地文件为同目录
`revision-4/neutral-standing.png`，1254×1254 RGBA；纯 Pillow 抠图后已检查浅/深底
596 px 与 160 px。原图、两次提示词和 QA 都在 revision-4，仍未安装或获最终模型批准。

用户将下一步改为制作常态灵梦；先生成空手自然站姿，随后要求加长裙子、细化小腿，
眼睛和气质参考原吃饭团图，最后要求鞋子稍大。内置 image_gen 三轮原图与提示词已
保存到 `build/reimu-neutral-20260906/`。最新是
`revision-3/neutral-standing.png`（1254×1254 RGBA），保留长裙、细腿和较放松的眼神，
鞋子略放大。生成源为白底 RGB，沿用用户已允许的本地抠图流程；当前纯 Pillow
`revision-3/matte.py` 已完成，浅/深底 596 px 和 160 px 合成已目视检查。
`revision-3/qa.json` 记录源/成品摘要和透明度；不透明内部 RGB 变化为 0。
初稿根目录 matte.py 因缺 NumPy 未运行成功，未安装依赖；不要将其误作最终流程。
这是立绘审阅，不是已批准动作或模型表；原生桌宠保持 1.3，Claude 继续延期。

## 2026-09-06：生气表情已接入并安装 1.3

用户确认带怒气符号和「むっ！」的最终预览后，Consumer 原生桌宠已接入该姿势。
快速四连击保持 1.2 秒，随后返回最新工作状态；暂停/减弱动态/休眠抑制图像切换，
失败会清除反应。原 40 帧和单击/双击/喂食动作不变。新增图片独立携带并校验摘要，
缺失/损坏只降级该表情且菜单明确提示，不影响原吃饭动画。
安装位置仍为 `~/Applications/灵梦桌宠.app`，1.2 备份在
`~/.codex/artifacts/reimu-anger-20260906/previous/灵梦桌宠.app`。
30 项行为、28 项状态契约、13 项原生和 3 项表情资源检查通过；实际 CUA 四连击
确认皱眉、红色怒气符号、日文和「让我吃完嘛」，随后恢复真实「工作中 · 2 项」。
记录见 `build/reimu-anger-install-20260906/installation.json` 与 `qa/`。
Harness core、钩子、Claude 配置均未改；Claude 仍按用户要求延期。Consumer 交接已更新，
本地未 commit/push，完整 35 动作、飞行/睡眠与六档视觉仍未完成。

## 2026-09-06：被戳表情进入美术审阅

**续作：用户已同意皱眉方向/局部处理，并要求添加红色怒气符号与生气日文。**
最新文件为同目录 `angry-final.png`（688×688 RGBA），配独立 `anger-overlay.png`；
内置 image_gen 生成符号和「むっ！」，本地 Python 彩度提取去掉生成器画出的棋盘格，
将已确认草案的两块眉眼局部合回原图。`build_reaction.py` 可复现；
`reaction-qa.json` 证明眉眼/特效范围外改变像素为 0，表情帧保持原始 alpha。
饭团、袖子、饰品及其他部位保留原始像素。浅/深色合成及 160 px 已目视检查，
浏览器保持表情/深色背景控件已实测。预览页已更新，旧版见 `full-frame-drafts.html`。
这是已制作好的独立表情预览，尚未接入或替换原生 1.2 应用；不是完整新动作验收。
下方「等待答复」是上一轮状态，现已解除。

用户确认 1.2 后授权继续；本轮通过内置 image_gen 制作两张皱眉关键姿势草案，
保存在本地 `build/reimu-poke-art-20260906/`。先看该目录 README、index.html、
prompts.md 和 qa.json。预览地址 `http://127.0.0.1:8139/`，已检查 160 px 对比与切换控件。
第一版画出了假棋盘格；第二版为白底 RGB，眉眼方向可审阅，但脸外受保护实色区域
有 11.46% 像素超过通道差 24，整图替换会跳动。两版均未采用为运行帧。
已询问用户表情方向及本地 Python 眉眼补丁处理，当前等待答复；尚未进行补丁合成。
后续需保持补丁外原图像素及饭团/袖子遮住脸侧饰品的关系，验证真实透明通道和
160 px 播放后再接入。没有修改已安装 1.2、行为代码、40 帧、钩子或 Harness core。
素材仅供本地示例，未 commit/push；Claude 按用户要求继续搁置。

## 2026-09-06：交互原型 1.2 已安装

用户明确先搁置 Claude 验证、等待其通知，并授权继续下一阶段。Consumer
`desktop/macos/PetBehavior.swift` 已实现独立输入/瞬态状态机：单击、双击、四连击、
右键喂一口、拖拽接管/放下恢复、低频咀嚼停顿。反应结束返回最新工作状态；
任务数变化不重置动作；失败优先；连续输入不排队，落地锁内丢弃的点击不计入下一次连点。
复用已确认的 40 帧，未改原图、钩子信任或 Harness core。飞行、举御札、趴桌睡觉等
新姿势没有制作，完整 35 动作/睡眠链/六档视觉仍待后续素材与行为验收。

应用仍为 `~/Applications/灵梦桌宠.app`，现版本 1.2，原 1.1 保存在
`~/.codex/artifacts/reimu-interaction-20260906/previous/灵梦桌宠.app`。
26 项状态机、28 项工作状态契约、12 项原生窗口/计时器/菜单检查通过，
素材仍为严格钉住的 40 帧/4 秒。实际 CUA 验证「嗯？」「戳到啦」「让我吃完嘛」
「再吃一口」与回到真实工作状态；物理拖拽返回 AXError.notImplemented，仅位移/边界和
拖拽 FSM 有程序化验证。见 [本轮 QA](../build/reimu-interaction-20260906/qa/interaction.json)
与 [安装记录](../build/reimu-interaction-20260906/installation.json)。
Consumer 根 HANDOFF/desktop README 已更新；仓库检查通过，本地未 commit/push。
Claude 按用户要求暂不继续测试或安排监控。


## 2026-09-06 新增：独立工作事件桌宠 1.1

**最新：当前旧任务重载后也已真实接通。** 本条「继续验证」触发 SessionStart、
UserPromptSubmit、PreToolUse、PostToolUse，散列会话 ID 与当前 CODEX_THREAD_ID 一致；
生产快照显示 working / 1 项，实际桌宠 UI 显示「工作中 · 1 项」。没有注入模拟事件，
没有改代码或信任配置。本轮结束事件需在回复结束后才能产生；其他真实桌面任务的 Stop
已在前次验证。见 [当前任务实测](../build/reimu-work-observer-20260906/qa/codex-current-task-live.json)。
下方旧任务未上报的历史问题已解除，此任务无需再次重启。Claude Code 仍显示额度耗尽，
Send 禁用，仅 Claude 真实接入测试待额度恢复。运行范围仍是已收到钩子的本机会话。


**续验更新：Codex 桌面来源已确认，覆盖仍不完整。** 接收器中另一个桌面任务的散列 ID
与应用 `list_threads` 一致，共 25 个真实事件（开始、提交、11 次工具开始/返回、结束）。
真实记录经原生加载器回放，25 项状态检查通过；这不等于该任务实播 UI 已目视验证。
见 [桌面来源报告](../build/reimu-work-observer-20260906/qa/codex-desktop-live.json)。
上次较早载入的任务没有任何钩子事件；现已解除（见上方最新记录）。当时会话未重载配置只是
待验证原因。下一步由用户在本轮结束后重新载入任务/应用，再检查；不向真实状态注入假事件。
Claude Code 的组织额度限制与禁用的发送按钮仍存在。此次只验证和记录，不修改运行代码。


用户授权先接工作事件再扩展交互。运行接收器和 AppKit 源码已放入 Consumer
`gensokyo-codex-pets/desktop/`，安装到同一 `~/Applications/灵梦桌宠.app`。
详见 Consumer `desktop/README.md` 与根 `HANDOFF.md`；Harness core 不增加 provider 行为。
复用原确认的 40 帧，工作时吃饭/眨眼，闲置低频眨眼，等待/中断静止。
本阶段未生成新图、未实现 35 动作 FSM 或六档食物视觉。

用户已亲自通过 Codex CLI `/hooks` 信任钩子。真实 Codex CLI 只读测试成功收到
SessionStart → UserPromptSubmit → Stop → SessionEnd，实际桌宠显示「工作中 · 1 项」，
随后回到已观察任务闲置。见
[真实 CLI 报告](../build/reimu-work-observer-20260906/qa/codex-live.json)。
该 CLI 报告本身不验证桌面任务；桌面单任务证据见上方续验更新。Claude 桌面 Code UI 已确认，但组织额度用尽、
发送按钮禁用，真实 Claude 事件待验证；不能用 CLI 未登录推断桌面未登录。

14 项 Python 接收/安装测试、28 项跨语言状态测试、12 项原生自测通过；
隔离事件注入实际确认工作、输入/审批请求、轮次结束和中断四种 UI 状态。
所有模拟事件仅在 `build/reimu-work-observer-20260906/qa/ui-state/`，
测试进程已退出，现运行不带 `--work-state-path` 的真实接收模式。
钩子只保存事件及散列 ID，不保存 prompt/工具内容，不返回权限决定；
未收到/超时数据保持未知语义，Stop 不宣称任务成功。
旧独立应用保存在 `~/.codex/artifacts/reimu-work-observer-20260906/previous/`；
原 Codex 自定义宠物仍保留，未绕过受限 UI 修改其内部设置。
本地未 commit/push；后续先完成两个桌面来源的真实事件验收，再进入交互 FSM。


## 2026-09-06 新增：坐姿饭团参考图独立示例

**最新调整：减少 Codex 待机停顿版已覆盖同一自定义宠物包，待刷新。** 用户反馈“他动的好慢”。
只读检查当前 app.asar 确认 idle 帧时长乘 6，非 idle 播三遍后也回到慢速 idle；
初版预览遗漏了 6 倍规则。现 idle 使用 `[0,29,0,5,0,4]` 原有姿势，包含吃饭与眨眼，
最长连续不变画面由 4,260 ms 减为 1,920 ms，整轮仍为 Codex 固定的 6.6 秒。
预览现按实际时序导出；图集回检和计时检查通过，见
[motion-v2 说明](../build/reimu-codex-onigiri-20260906/README.md)。安装使用新图名并原子更新同一 pet.json；
旧版本保存在 `history-v1/`。用户需刷新宠物列表；Codex UI 仍受工具限制，未声称新版实播已验证。

**最新：Codex 自定义宠物包已安装，等待用户在设置中选用。** 用户澄清要替换 Codex 桌宠并明确要求
“帮我替换掉”。已完成 [Codex 简化适配](../build/reimu-codex-onigiri-20260906/README.md)，安装于
`/Users/lyuyuwei/.codex/pets/reimu-onigiri-example/`，显示名「灵梦 · 吃饭团」。
1536×2288 v2 图集使用已确认透明帧：idle 眨眼、running 吃饭团，其余行保持坐姿。
这是明确的两动作简化版，不声称完整标准动作或方向视线。源摘要、73 个有效格、15 个空格、
无损解码与安装摘要校验通过，深色逐帧图已目视检查。独立 `.app` 已退出。
控制工具返回 `Computer Use is not allowed to use the app 'com.openai.codex' for safety reasons.`，
故尚未选中或验证 Codex 内实际播放；用户需在「设置 → 宠物 → 刷新」选择「灵梦 · 吃饭团」。
未绕过工具限制操作内部设置，未覆盖内置宠物，未写入 Consumer/core，未 commit/push。

**最新交付：独立 macOS 桌宠已安装并试运行。** 用户回复“可以，怎么做成桌宠？”确认透明版，
随后“可以”授权独立应用。见 [桌宠说明](../build/reimu-desktop-example-20260906/README.md) 和
[确认记录](../build/reimu-desktop-example-20260906/approval.json)。实际应用在
`/Users/lyuyuwei/Applications/灵梦桌宠.app`，桌面 `灵梦/灵梦桌宠.app` 为启动快捷方式。
原样播放透明版 40 帧；透明置顶、拖动与位置记忆、160/240/320/400 px、暂停、减弱动态、退出。
7 项实际素材加载器检查、12 项原生程序化检查通过；实际界面核对 240/320 px 显示、右键暂停/继续、
大小菜单、退出与重新启动，位置和偏好恢复一致。物理拖动 CUA 返回 AXError.notImplemented，
其位移与边界逻辑仅有程序化验证。签名严格校验通过；当前已启动，保留 320 px 试运行位置。
这是本机 Apple Silicon / macOS 13+ 原生 AppKit 示例，未写入 Harness core 或 Consumer，未 commit/push。

**透明素材制作记录：** 用户在 v2 白底确认后要求“生成一个透明底版本”。
内置 image_gen 两次返回无 Alpha 的 RGB 棋盘格图，均未采用；随后用户明确回复
“允许，使用本地抠图”。已完成
[transparent-v1](../build/reference-onigiri-eat-blink-20260906/transparent-v1/README.md)：
40 帧 / 10 fps / 4 秒，使用同一张透明遮罩，保留原动作、人物、饭团、饰品、粉字和原有平涂地面阴影。
每帧 274,737 个全透明像素、4,094 个半透明轮廓像素；原 5,203 个动态像素 RGBA 不变，
194,513 个不透明内部像素 RGB 不变。仍可见像素叠回白底与原对应帧 RGB 相同。
右侧发丝封闭背景间隙采用显式种子 (454,350)；米饭、袖子、眼白等内部白色保留。
7 张完整替代姿势经 Harness v2 可见性关键帧切换，每帧恰好一张可见，**不是解剖分层**。
plan/render/validate、atlas、减弱动态、596/160px APNG/WebP 解码和 14 项运行测试通过，
Harness 零错误零警告。浏览器在深色/绿色/棋盘格上检查了 596/160px、咀嚼峰值、闭眼、回退和减弱动态。

新的 [透明预览](http://127.0.0.1:8137/index.html) 可切换背景。
[静态透明 PNG](../build/reference-onigiri-eat-blink-20260906/transparent-v1/base.png) 和
[透明动画 WebP](../build/reference-onigiri-eat-blink-20260906/transparent-v1/exports/eat-blink-596.webp) 已交付。
[完整透明交付包](../build/reference-onigiri-eat-blink-20260906/transparent-v1/onigiri-transparent-v1.zip)
约 34.3 MB；封装/解压后 82 文件校验、14 项运行测试通过，见其 `delivery-verification.json`。
Consumer 当前相同 builder 的精确帧源入口现已通过；**未运行完整 Consumer 构建或发布**。
透明版现已得到用户“可以，怎么做成桌宠？”确认；封存包内 pending 为制作时快照，独立确认记录见上方。
已确认白底交付包 71 文件校验仍通过；本轮无 Consumer 写入、commit 或 push。
下方“白底导入被拒绝”是上一阶段记录；该问题已由本透明候选在精确帧源入口这一层解决。

用户要求先读交接，随后按新提供的第三方同人坐姿饭团 JPEG 自动跑一版，只含吃东西和眨眼。
已完成 [本例 REVIEW](../build/reference-onigiri-eat-blink-20260906/REVIEW.md)。用户进一步指出
咀嚼时脸颊遮挡饰品，现已修复，当前示例为
`build/reference-onigiri-eat-blink-20260906/ornament-v2/final/`，见
[v2 REVIEW](../build/reference-onigiri-eat-blink-20260906/ornament-v2/REVIEW.md)。
`final/` 保留为有遮挡问题的 v1，较轻的首稿仍在 `loop/`。
这条独立示例线不替换下方已选 v4 idle、chew-v9 task_2 或 Consumer 预检候选。

**v2 修复证据：** 原图饰品及白色褶边在表情后合成，6,787 像素保护区全程与原图一致；
只修复 428 像素，bbox [392,269,414,299)，保护区外与 v1 差异 0，眨眼与时序不变。
动态并集现为 5,203 像素，仍 40 帧 / 10 fps / 4 秒。Harness 与 atlas 回检通过，
仍保留 40 条白底触边提示；596/160px 导出及浏览器鼓腮峰值、闭眼叠加已复查。
本次是合成修复，未重新生成美术或修改核心代码；用户已于 2026-09-06 回复
“我觉得OK，可以进行下一步了”，确认本例 v2，见
[approval.json](../build/reference-onigiri-eat-blink-20260906/ornament-v2/approval.json)。
原 plan / QA 的 pending 是制作时快照，保持其摘要绑定不变，以该独立确认记录为准。

**已完成下一步：原样交付与独立播放器接入。**
[delivery/](../build/reference-onigiri-eat-blink-20260906/ornament-v2/delivery/README.md)
封存 40 帧、基准、596/160px WebP/APNG、SHA 清单和用户确认，提供自包含播放器及压缩包。
[压缩包](../build/reference-onigiri-eat-blink-20260906/ornament-v2/reference-onigiri-approved-v2.zip)
约 31.3 MB；71 文件核验、解压后的 14 项运行测试和篡改检测通过，见
[delivery-verification.json](../build/reference-onigiri-eat-blink-20260906/ornament-v2/delivery-verification.json)。
使用 Consumer 当前工作区原版 `app/animations.js`，绑定独立的
`reimu / reference_onigiri_example / eat_blink`，不使用任务数状态。
14 项加载器/播放器测试通过；真实浏览器检查 596/160px、逐帧、系统/手动减弱动态、
清单缺失/单帧缺失回退和 390px 页面。逐帧 PNG 与已确认版字节相同，6,787 饰品像素全程不变。
帧清单验证零错误零警告，不取消原 layered build 的 40 条白底触边提示。

**正式 Consumer 导入仍未通过：** 实际调用其原版 `load_exact_frame_source`，
在基准 RGBA PNG 的 alpha=[255,255] 处拒绝：要求图片包含可见像素及透明像素。
未放宽校验、加透明边框或改变已确认画面；未运行完整 Consumer 构建/发布。
下一步正式桌宠接入需要单独制作并检查透明背景派生版。
本轮 Consumer fetch 成功，HEAD/origin-main 均为 `eeb42236b18e534ac8befd5f71561feed6cd5484`；
其工作区仍有既有改动，不把 HEAD 相同写成工作区已发布。文件清单前后相同，本轮无 Consumer 写入、commit 或 push。
[交付播放器](http://127.0.0.1:8136/delivery/index.html) 是当前接入预览；
[新预览](http://127.0.0.1:8136/preview.html) 使用独立本地服务；8124 本轮空响应，未停止该服务。
下面各项为 v1 初版制作记录，涉及当前版本和动态像素数时以上述 v2 为准。

- 688×688 原尺寸、40 帧、10 fps、4 秒循环，四次咀嚼与一次眨眼。用户原 JPEG 字节未变；
  保留白底、阴影与原构图，**不是透明抠图桌宠**。
- 内置 image_gen 四次编辑得到半闭眼、闭眼、轻/较强咀嚼；仅取显式记录的眼区、下颊/嘴区，
  通过 Harness v2 的 PNG 覆盖片和离散 opacity 关键帧合成。这些是合成素材，不是原画解剖分层。
  完整提示词、原始生成图、输入 SHA、选区和脚本均保存在本例目录。
- 最终 validate：0 errors / 40 `CONTENT_TOUCHES_EDGE` warnings（白色不透明背景每帧触边）。
  动态并集 5,631 像素，bbox [265,220,414,324)；动态区外变化 0、alpha 不变、首尾 PNG 字节一致。
- 596/160px APNG 和无损 WebP 已导出；APNG 完整帧 disposal=0、blend=0，CRC 与解码像素已核验。
  WebP 合并为 18 个计时帧，展开后 40 帧/4 秒以及解码 RGBA 完全一致。减弱动态固定第 0 帧；
  8×5 atlas 已 export/validate-export。浏览器检查了两种尺寸、咀嚼峰值、闭眼、控件和导出格式。
- 当前源码相关回归为 **220 passed in 2.50s**（layers / plan / schemas）；未重跑全套或修复
  下方记载的 generation 偶发失败。未修改既有 core/schema/tests，不把局部通过称为全量全绿。
- 本机 `.venv/bin/sprite-harness` 是旧 site-packages，拒绝新 `keyframes`；本轮明确使用
  `PYTHONPATH=src .venv/bin/python -m sprite_harness`，未重装或改动环境。
- [预览页](http://localhost:8124/build/reference-onigiri-eat-blink-20260906/preview.html)
  和 [QA](../build/reference-onigiri-eat-blink-20260906/qa.json) 可直接查看。
  此处为 v1 制作时记录；当前 v2 已确认及下一步接入结果以上文为准。无 Consumer 写入、commit、push 或发布。

`build/` 仍为本机忽略目录。下方原始最新美术选择和历史记录完整保留，继续约束原有资源线。

## 当前交接摘要 / Read this first — 2026-09-06

本节是当前状态入口；下方日志保留各阶段的原始结论，不代表现在仍需执行。
历史中的“下一步”“待审核”“尚未实现”“全量测试通过”和旧 Git HEAD，
必须结合本节与实际文件解读，不能当成最新指令。
**最新决定：“还是用v4吧”——结束本轮改鞋，采用原始 v4。**

v11–v15 鞋型试稿全部未采用，保留为历史；不再处于待审核状态，也不继续延长、收短或改方向。
这些试稿的任何像素都没有进入原始 v4、眨眼关键帧、循环、Consumer 预检候选或生产资源。
当前继续使用 `legs-forward-v4`、`blink-v2-legs-v4`、`blink-loop-v2-legs-v4`，
以及已完成的 `reimu-idle-consumer-preflight-20260906/final/` v4 集成候选。
本次选择不执行生产发布、commit 或 push。

**最新进行项：task_2 耳旁装饰交界修复。** 用户反馈吃饭时脸会盖住装饰并授权“修改”。
已修正程序化脸颊位移，生成 [chew-v10-ornament-guard 候选](../build/reimu-task2-ornament-guard-20260906/REVIEW.md)：
两侧装饰、描边与发丝间隙保护区全程保持基准，下颊保留咀嚼；16 帧、10 fps，Harness 零错误零警告。
候选待视觉确认，尚未进行 Consumer 导入/预检/发布；生产 task_2 与已有 idle 预检中的 task_2
仍是 v9。这里的 chew-v10 是吃饭动画版本，与未采用的 shoe-vamp-v10 无关。idle 继续原始 v4。

同日较早用户回复“可以”，授权继续 v4 idle 集成预检。已完成独立候选精确帧源包、
两次不发布构建及浏览器检查，入口为
[预检 REVIEW](../build/reimu-idle-consumer-preflight-20260906/REVIEW.md)。当前采用其 `final/`
候选；生产 Consumer 仍未改变。之后用户评价“鞋子还是有点问题，其他的都OK”，
试改后最终选择原始 v4。应保留这两次表态，不要重新发起全面美术审核或继续改鞋；
idle↔task_2 的几何差异保留为已知事项，独立的生产发布决定仍未作出。

### 1. 范围、阅读顺序与权限

1. 先读根目录 [AGENTS.md](../AGENTS.md)、[HARNESS.md](../HARNESS.md)，再读本摘要。
2. 当前美术交接看下方资源表、对应 `REVIEW.md` 和 `qa.json`；核心契约问题再读
   [animation-spec.md](animation-spec.md)、[animation-plan.md](animation-plan.md)、
   [layered-sprites.md](layered-sprites.md)。不要靠版本号最大或浏览器最后打开的页面选资源。
3. Harness：`/Users/lyuyuwei/Documents/ChatGPT/Spirite harness`，负责通用校验、合成、
   预览和导出。Consumer：`/Users/lyuyuwei/Documents/ChatGPT/gensokyo-codex-pets`，
   负责任务来源、0–5 状态映射、播放与回退；需要操作它时先读其 `AGENTS.md`、`HANDOFF.md`。
4. 后续已获预检授权：所有候选资源与配置写在 Harness `build/reimu-idle-consumer-preflight-20260906/`。
   Consumer 已 fetch 并只读核对，生产配置与资源未变；没有新的发布、commit 或 push。
   历史上 task_2 的发布授权不能自动用于新的 idle 发布。
5. 项目仍是可扩展分层桌宠系统；现在的精确扁平帧是合法交付路径，**不是真分层源文件**。
   任务数量、eating 状态和 Codex 标准动作行是不同概念，不要互相替代。

### 2. 当前采用什么，以及实际部署到了哪里

| 对象 | 当前版本与位置 | 状态 |
| --- | --- | --- |
| Harness 待机静态基准 | [legs-forward-v4/candidate-596.png](../build/reimu-idle-intake-20260905/legs-forward-v4/candidate-596.png) | 用户多次重申采用的唯一当前腿鞋版本 |
| 待机三张关键帧 | [blink-v2-legs-v4/](../build/reimu-idle-intake-20260905/blink-v2-legs-v4/) 的 `neutral.png`、`half.png`、`closed.png` | v4 下半身 + 已确认的 blink-v1 眼部像素 |
| 待机循环与导出 | [blink-loop-v2-legs-v4/](../build/reimu-idle-intake-20260905/blink-loop-v2-legs-v4/) | 已导出、结构验证通过；尚未进入 Consumer |
| Consumer 集成候选 | [final/candidate-consumer/](../build/reimu-idle-consumer-preflight-20260906/final/candidate-consumer/) | 独立副本：v4 精确帧源包、idle 配置、40 帧运行预览；不属于生产 Consumer |
| Consumer 的 eating/idle（任务数 0） | `assets/reimu/eating/idle/animation.json` | 仍是旧基准的 **1 帧静态回退**，不是上述 v4 眨眼循环 |
| Consumer 的 eating/task_2 | `assets/reimu/eating/task_2/animation.json` | 已发布 `chew-v9-asymmetric-cheeks`，16 帧、10 fps、1.6 秒 |
| task_2 装饰交界修复候选 | [reimu-task2-ornament-guard-20260906/candidate/](../build/reimu-task2-ornament-guard-20260906/candidate/) | `chew-v10-ornament-guard`；仅 Harness 候选，未替换生产 v9 或 idle 预检副本 |
| Consumer 的 task_1、task_3、task_4、task_5 | 各自 `assets/reimu/eating/<state>/animation.json` | 均仍为 1 帧静态回退，不是已完成的动态状态 |

特别注意版本重名：**idle 的 legs-forward-v4** 与 **task_2 的 chew-v9** 属于不同资源线。
被弃用的 `lower-body-redesign-v9` 和 `shoe-vamp-v10` 不影响已发布的 chew-v9。
不要把 Consumer 的 Codex `idle` atlas 行替换成 eating/idle，反之亦然。

### 3. v4 待机交付内容与视觉确认边界

- 596×596 RGBA；neutral 文件与 v4 原图字节一致。半闭眼/闭眼来自此前确认的
  `blink-v1` 眼区，眼区之外固定，腿鞋全程不动，首尾文件相同。
- 40 个逻辑帧、10 fps、4 秒一轮：睁眼 3.4 秒 → 半闭眼 0.1 秒 → 闭眼 0.2 秒
  → 半闭眼 0.1 秒 → 睁眼 0.2 秒。不是持续大幅运动；需要看过第 3.4 秒才能看到眨眼。
- 596px 和 160px 均有透明 APNG 与无损 WebP。APNG 为完整画布帧，disposal=0、blend=0；
  原构建已检查 CRC 和解码 RGBA。WebP 合并为 5 个计时帧，可见 RGBA、alpha 和时长一致，
  但编码器会丢弃 alpha=0 下不可见的 RGB；不能称其全部 RGBA 字节相同。
- 原始 v4 最终选择明确，且用户已表示鞋子之外“其他的都OK”。旧 kneeling `blink-loop-v1`
  的眨眼节奏已获认可，新 v4 循环沿用该节奏。源构建 `qa.json` 与预检报告中的
  playback review pending 是生成时快照，本轮没有重写它们；结合本页最新用户决定解读。
  **独立预检已获授权并完成，正式 Consumer 激活与发布尚未执行。** 不再重启腿鞋试验。
- 当前 task_2 继续固定饭团、双手、身体和睁眼，以不对称双颊咀嚼；不要恢复旧的往返手臂、
  张嘴或全脸缩放方案。idle 可以眨眼，不意味着 task_2 也应加入眨眼。

### 4. 保留的依赖和 legacy（不要删除或自动采用）

| 文件组（均在 `build/`） | 用途与禁止事项 |
| --- | --- |
| `reimu-idle-intake-20260905/blink-v1/` | 原已确认的眼部关键帧、mask 和源哈希；当前构建依赖，不可因“旧版”删除 |
| `reimu-idle-intake-20260905/blink-loop-v1/build_loop.py` | 当前 v4 构建直接 import 其 APNG 写入/验证函数；旧动画外观不采用，代码依赖仍需保留 |
| `scene-repair-v2/`、`legs-forward-v1/`、`legs-forward-v2/` | 美术来源与历史中间版；不覆盖当前 v4 |
| `legs-forward-v3/`、`legs-forward-v5/` | 未采用的腿鞋方向；v3 错误落地姿势、v5 鞋形不合适 |
| `reimu-idle-intake-20260906/shoe-single-v6/`、`shoe-single-v7/`、`shoe-single-v8-reference/` | 未采用的单鞋试验；包括短圆马蹄感、楔形、落地角度等失败记录 |
| `reimu-idle-intake-20260906/lower-body-redesign-v9/`、`shoe-vamp-v10/` | 未采用的整体重画与鞋面试验；均不得合入 v4 或动画 |
| `reimu-idle-intake-20260906/shoe-v11-subtle/`、`shoe-v12-direction-locked/`、`shoe-v13-slender/`、`shoe-v14-longer/`、`shoe-v15-shorter-heel/` | 最新五张鞋型试稿均为 `NOT_ADOPTED`；各自保留图、提示词、REVIEW 和 QA，不再待审核 |
| `reimu-idle-consumer-preflight-20260906/` 根下的首轮 `candidate-consumer/`、`preflight-a/`、`preflight-b/` | 首轮继承静态计划、出现 ZERO_MOTION 警告；仅保留过程证据，当前预检一律使用 `final/` |

后续生成试稿没有任何像素进入当前 v4 循环。原始生成图可能改动其他鞋、腿根、衣裙、桌面、
画布配准；v9 还含烘焙棋盘格。不能把这些图当成合格透明资源或精确局部替换。
历史 intake 根目录 `REVIEW.md` 中“眨眼关键帧缺失”只描述当时状态：现在 Harness 已有上述三帧，
但真正可独立复用的 idle 身体/手臂/表情分层仍不能宣称齐全。

### 5. 验证证据、时间与 SHA-256

**本次文档整理现场核对**：原始 v4 与 `final/` 候选 base SHA 一致；v11–v15 QA 均为
`NOT_ADOPTED`；生产六状态 manifest 帧数仍为 `1, 1, 16, 1, 1, 1`。
重新执行 `final/preflight-a/idle/build` 的 Harness validate 得到 **0 errors / 0 warnings**。
本次未重跑全部预检、浏览器播放或全量测试，以下测试结果分别属于同日已完成的运行。

**同日最终预检结果**（[report.json](../build/reimu-idle-consumer-preflight-20260906/final/report.json)）：

- 两次独立 `--no-publish` 构建均为 0 errors / 0 warnings；47 个文件字节一致，
  仅 report.json 含各自构建路径，规范化路径后相同。
- 40 帧、10 fps、4 秒；3,625 像素的动态并集全部位于已确认眼区，眼区外变化 0，
  alpha 全程一致，首尾 PNG 字节一致。见 [pixel-checks.json](../build/reimu-idle-consumer-preflight-20260906/final/pixel-checks.json)。
- 实际候选 manifest + 原 Consumer loader 的四个检查通过：正常加载、缺失 manifest、
  状态绑定错误、闭眼帧缺失；后三项明确回退到 v4 base，task_2 保持可用。
  这些是本地文件支持的模拟传输检查，见 [runtime-checks.json](../build/reimu-idle-consumer-preflight-20260906/final/runtime-checks.json)。
- 浏览器检查了 596/160px、160px 闭眼画面、减弱动态固定第 0 帧、0↔2 切换；
  idle 显示 40 帧、task_2 显示 16 帧。两状态的几何不完全一致，没有执行全图缩放或配准。
- Consumer 176 个文件的前后清单一致；`check-repository.sh` 在 Harness venv PATH 下通过。
  首次用系统 Python 运行因缺少 Pillow 失败，切换既有 venv 后通过，没有安装依赖或修改代码。

**同日首次交接记录**（保留原始测试结论）：

- v4 三张关键帧、40 个循环帧与 `qa.json` 所记源哈希逐一一致，四个 APNG/WebP 导出哈希一致。
- Harness `validate --json`：v4 关键帧、v4 循环、task_2 chew-v9 正式 build，均 **0 errors / 0 warnings**。
- Consumer 只读核对：六个状态的 base 和全部运行帧符合各自 manifest 中的 SHA；帧数分别为
  `idle=1, task_1=1, task_2=16, task_3=1, task_4=1, task_5=1`。未重跑 Consumer 全仓测试或浏览器实时播放。
- Harness 全量测试当时为 **668 passed / 1 failed（15.85s）**，不是全绿。
  失败：`tests/test_generation.py::test_fast_oversized_adapter_response_has_stable_error`，
  第 370 行预期 `ADAPTER_RESPONSE_TOO_LARGE`，实际 `PROCESSING_ERROR`。
  随后单独重跑该测试 **1 passed（0.48s）**。原因未定位，不能把单测重跑通过称为已修复；
  核心发布前需独立排查。后续预检和本次文档整理均未修复该问题或放宽测试。

```text
v4 neutral:
590e6242f39b62491a95718405aa19eff3a9ae658e49744915b6ddac8fd80621
v4 596px APNG:
ecc3790a4c84c138a2575785ea091a9350216e01bc1449e620b6eebecef9bbfc
v4 596px WebP:
d54ff6441ef0cb01698a027d1b29de05d77c8f73391486b46c1e6aa52ce83d83
v4 160px APNG:
d4abf7e110dbd25fcb5010c4255602794b4b7320ab7673233d7ef561d0510db6
v4 160px WebP:
82002de0829ebc39bcf17222061d53a083be274fa586f609953e173b92250c73
Consumer idle current base (NOT v4):
2ae03a533cd5416b1da5b6a9f692bd46ad3c91fd584f32f3c98b9ec347ce0781
Consumer task_2 base:
0251947e0ca94f0ba0fa4b724d37fac242c86ba4de9591bb558c226ad4904cfe
Consumer task_2 runtime animation.json:
607b6760bbd152b698033c8dcfa70a2c069ae67d95b865e4c0c6e9c535ecf6cf
v4 final Consumer preflight plan digest:
sha256:9af2a5d64b5a2c511244bc875467499a51fcd942c536df3d6b2dbc5467f420c3
v4 candidate exact source.json:
7a1bf66f710a8c89b08a3a67868393283675c7eff7cb9ff3a51988171acf1b14
v4 candidate runtime animation.json (NOT production):
80ef8cdf2159dbc75af363e71018e28182086caa9092234574e9a1b65d2335a3
```

### 6. 可执行命令与预览

从 Harness 根目录执行；校验不会发布或重画资源：

```sh
.venv/bin/sprite-harness validate build/reimu-idle-intake-20260905/blink-v2-legs-v4 --json
.venv/bin/sprite-harness validate build/reimu-idle-intake-20260905/blink-loop-v2-legs-v4 --json
.venv/bin/sprite-harness validate build/reimu-idle-consumer-preflight-20260906/final/preflight-a/idle/build --json
.venv/bin/sprite-harness validate build/reimu-idle-consumer-preflight-20260906/final/preflight-b/idle/build --json
.venv/bin/sprite-harness validate build/reimu-task2-eating-keyframes-20260904/runs/chew-v9-asymmetric-cheeks/loop/build --json
.venv/bin/pytest -o addopts='' -q -p no:cacheprovider
.venv/bin/pytest -o addopts='' -q -p no:cacheprovider tests/test_generation.py::test_fast_oversized_adapter_response_has_stable_error
```

预览：[v4 待机 596/160px](http://localhost:8124/build/reimu-idle-intake-20260905/blink-loop-v2-legs-v4/preview.html)，
[当前 Consumer 候选](http://localhost:8124/build/reimu-idle-consumer-preflight-20260906/final/candidate-consumer/app/?tasks=0)
可用 0/2 按钮切换状态，并切换尺寸与 reduced。任务数仍是手动调试输入。
若服务器不存在，在 Harness 根目录运行 `.venv/bin/python -m http.server 8124 --bind 127.0.0.1`；
端口已占用时先检查，勿杀掉未知服务。浏览器打开某张试稿不代表它被采用。

复现构建的入口是 `build/reimu-idle-intake-20260905/blink-loop-v2-legs-v4/build_loop.py`。
**它会重写当前输出和报告，不是只读检查命令**；没有重建需求时用上面的 validate。
复现必须保留 `legs-forward-v4`、`blink-v1` 与 `blink-loop-v1/build_loop.py` 这些依赖。

预检复现过程见 [prepare.py](../build/reimu-idle-consumer-preflight-20260906/prepare.py)，
它在 `final/` 已存在时拒绝覆盖。需要再构建时选择新的独立输出，保留现有证据。
候选源包位于 `final/candidate-consumer/pets/reimu/animations/eating/sources/idle-blink-v4/`，
候选配置位于 `final/candidate-consumer/pets/reimu/animations/eating/animation-set.json`。

### 7. 接手后的下一步，不要越过确认门槛

新增优先项：查看 [task_2 修复预览](http://localhost:8125/build/reimu-task2-ornament-guard-20260906/candidate/preview.html)，
确认装饰接缝与更克制的下颊运动；认可后再做该版本的受保护精确帧导入、两次 Consumer
无发布预检和发布检查。现有 idle 预检不包含这个修复，不能混称已完成其集成。
修复通过固定保守的二维保护区域实现，不是真分层遮挡系统；统计 131/127 是旧版在保护区
（含间隙与相邻脸/发丝）的变化像素数，不是确认被覆盖的装饰像素数。详细证据见候选 REVIEW。

1. 按用户最新决定继续原始 v4，结束本轮鞋型试验。v5–v15 全部保持未采用历史状态；
   不重画、不合入试稿、不删除原始图或历史依赖。
2. 已完成独立 idle 精确帧源包及两次 `--no-publish` 预检，见上述 `final/` 候选。
   两次均 0 errors / 0 warnings；47 个产物字节一致，report.json 仅构建路径不同，规范化后相同。
   浏览器 596/160px、闭眼帧、减弱动态、0↔2 切换已检查；候选 loader 的三种故障回退检查通过。
   眼区之外变化 0，alpha 全程一致，首尾字节相同。生产接入仍未完成。
3. 下一步围绕已有 v4 候选明确生产激活范围与发布决定；保留用户“其他的都OK”和最终选择 v4
   的结论，不重新做鞋型或要求全面审美复审。发布时受保护导入已固定的源包，
   保留旧 idle base，合并 idle 配置后执行原有事务发布及检查。候选配置只含 idle，
   禁止直接覆盖生产六状态配置。本轮未执行生产发布事务。
4. v4 idle 与 task_2 的桌面、人物和榻榻米几何不完全一致，作为激活时需明确接受的已知差异，
   不能靠全图 bbox 缩放宣称已经对齐。推广其他任务档位前先确定共有坐标和克制递增的食物规则。
5. 可独立排查上述核心测试失败；它与本次美术选择是两条工作线。未定位前不得宣称全量测试全绿。
6. 真实任务来源适配器、完整桌宠安装包与完整 Codex atlas 不在本轮完成范围。
   Consumer 旧交接仍描述手动调试任务数；本轮没有验证真实 Codex/Claude 任务接入，不能宣称已实现。

### 8. 工作区与交付限制

现场 Harness 为 `main` / `619d4a7`，包版本 `0.7.0`。现存多处 core/schema/tests/docs 未提交修改
早于本次整理，应保留；同日此前另在忽略的 build/ 下写入预检脚本与试稿，未修复、回退或提交核心修改。
本次“更新交接文档”只修改本文件，另做上述只读核对。Harness 未 fetch，远端状态未验证；
Consumer 在同日预检阶段已 fetch，当时 HEAD 与 origin/main 均为 eeb4223，本次未重新 fetch。
核心 pulse/keyframe 等工作见历史技术记录与当前代码，不要为文档整理改变版本号。

`build/` 被 `.gitignore` 忽略，图像、脚本和 QA 是**此机器本地交付物**；只拿到 Git 仓库不能重现
本轮美术。跨机器交接需显式移交选中资源及上述依赖并校验 SHA，不能声称已随 GitHub 同步。
本轮 Consumer 的 `HANDOFF.md` 未修改。需要同步它时必须单独遵守 Consumer 的写入授权与仓库规则。

## 历史日志 / Historical journal

以下内容完整保留供追溯，所有旧状态以本页顶部“当前交接摘要”为准。

## 2026-09-06 — v15 后再次确定原始 v4

用户最终选择“还是用v4吧”。v11–v15 均未采用；所有源图、试稿、循环及预检保留。
本轮仅同步交接和试稿状态，原始 v4 及 v4 集成候选内容未变，未写入生产 Consumer。

### 本次改鞋过程（已结束，以下待审核措辞是历史状态）

**“不行，还是用v4吧”——采用原始 v4，不继续修改腿、鞋或鞋面。**

**同日最新修订请求**：用户看过集成候选后表示“鞋子还是有点问题，其他的都OK”，
并回复“OK，修一下看看”，授权一张画面右侧鞋子的局部静态试稿。该请求仅对本次鞋型
试验覆盖此前“停止改鞋”决定，尚未选用新版本。内置 imagegen 的
[shoe-v11-subtle 试稿](../build/reimu-idle-intake-20260906/shoe-v11-subtle/REVIEW.md)
鞋面更修长、鞋底面更小，但也重绘其他细节，输出为带烘焙棋盘格的 1254×1254 RGB；
**不是合格局部替换或透明资源，不得整图合入**。原始 v4、预检候选和生产资源均未变。

最新反馈否决 v11 的脚朝向：“应该两个一个方向”。用户同意锁定原始朝向、位置和露底角度
再试，已生成 [v12 方向修正稿](../build/reimu-idle-intake-20260906/shoe-v12-direction-locked/REVIEW.md)。
两只鞋恢复同向前翘，但输出仍为整图重绘、带烘焙棋盘格的 RGB，只供静态鞋型审核；
未采用、未合入动画。v11 标记拒绝，当前运行资源继续保持原始 v4。

随后用户要求“右边的那只脚可以拉的修长一点点，模仿左边那只脚”。已以 v12 试稿为输入
生成 [v13 小幅修长试稿](../build/reimu-idle-intake-20260906/shoe-v13-slender/REVIEW.md)，
保留同向前翘姿态，供比例审核。仍为不透明 RGB 静态试稿，存在鞋外像素变化，未采用；
不得把 v12/v13 当成已经合格的 v4 局部修复或生产透明资源。

用户进一步要求“再拉长一点点”，已以 v13 为输入生成
[v14 再修长试稿](../build/reimu-idle-intake-20260906/shoe-v14-longer/REVIEW.md)。
右鞋沿原方向再小幅延长，仍同向前翘；待审核，未采用。它同样是带烘焙棋盘格、鞋外有变化的
RGB 静态试稿，不能直接合入原始 v4 或动画；当前运行资源保持不变。

最新用户反馈“脚后跟太长了”，以 v14 为输入制作了
[v15 收短后跟试稿](../build/reimu-idle-intake-20260906/shoe-v15-shorter-heel/REVIEW.md)。
右鞋更紧凑，但生成也牵动前掌、使其略显圆短，不能声称只改了后跟。待用户审核，仍未采用；
保留 v14 对比，原始 v4 和运行资源不变。

## 2026-09-06 — v10 declined; original v4 remains selected

Latest decision: “不行，还是用v4吧”. The vamp-only v10 study is now legacy,
not adopted, and must not be composited or propagated. Stop shoe/leg revisions.
Continue with original legs-forward-v4 and blink-loop-v2-legs-v4 unchanged.
All v5–v10 experiments remain preserved as history. This decision supersedes
the v10 integration suggestion below. Handoff and review status updated only;
no artwork/animation replacement, Consumer writes, publication, commit or push.

## 2026-09-06 — new narrow request: slightly longer shoe upper only

After returning to v4, user clarified that the shoe UPPER is too round and
should be slightly elongated. This authorizes a narrow image-right vamp study,
not restarting sole/leg/body redesign. `build/reimu-idle-intake-20260906/shoe-vamp-v10/`
contains exact built-in prompt, candidate-crop.png, static comparison preview
and REVIEW.md. The raw output exposes more black vamp but also shifts outsole
and surrounding geometry; it is NOT a compliant pixel-locked vamp-only edit.
Do not adopt whole generated crop or claim unchanged soles/other pixels.

Current selected base remains v4 with blink-loop-v2-legs-v4. No animation,
Consumer edits, publication, commit or push; no Harness PASS for raw study.
Only an approved small vamp-area change may be locally integrated later.

## 2026-09-06 — final direction: return to v4, stop shoe/leg revisions

Latest maintainer decision: “算了，还是用v4吧”. Use the original
`build/reimu-idle-intake-20260905/legs-forward-v4/candidate-596.png` as the
selected idle artwork, with the existing `blink-v2-legs-v4/` keyframes and
`blink-loop-v2-legs-v4/` loop. No further shoe/leg redraw is requested.
V5, shoe-single-v6/v7/v8-reference, and lower-body-redesign-v9 are legacy,
not adopted; all files retained. Their older pending-review notes are superseded
by this decision. None of their generated pixels entered the v4 loop.

Selection does not publish to Consumer or silently approve a new runtime
integration. No art regeneration or animation rewrite this turn; v4 art and
loop export hashes rechecked and loop Harness validation rerun. Static SHA-256:
590e6242f39b62491a95718405aa19eff3a9ae658e49744915b6ddac8fd80621.
596px APNG SHA-256:
ecc3790a4c84c138a2575785ea091a9350216e01bc1449e620b6eebecef9bbfc.
No Consumer writes, publish, commit or push. Continue future work from v4,
not from any later numbered shoe or lower-body concept.

## 2026-09-06 — whole lower-body redraw concept v9, not selected

User asked what regeneration could look like because shoe proportions and
thick leg roots remained awkward. A full-scene concept jointly redesigning
both legs/shoes is in `build/reimu-idle-intake-20260906/lower-body-redesign-v9/`:
concept.png, exact prompt, preview at CSS596/160 and REVIEW.md. Built-in imagegen
used v4 full figure and the user's shoe reference. Skirt hides leg roots,
ankles are small and shoes thinner/smaller. Actual result shows more downward
feet with less visible sole, not the original raised-sole pose. Explicitly
presented as a direction for review, not a selected replacement.

1254x1254 RGB with baked checkerboard despite requested alpha; not production
transparency. Full-scene upper-body/table/registration drift is also unapproved.
No local composition, normalization, runtime manifest, animation or Harness
PASS. V4/blink loop and Consumer remain untouched; no publish, commit or push.
Next: user evaluates overall proportions/pose before choosing an art direction.

## 2026-09-06 — v8 shoe study uses explicit user reference

User provided a closeup showing the desired thin elongated sole/rounded toe/
small heel and asked to match it. Built-in imagegen now used that exact image
as the second visual reference, with original v4 crop as edit target. New
`build/reimu-idle-intake-20260906/shoe-single-v8-reference/` contains the local
reference (do not commit), exact prompt, candidate-crop.png, preview and review
notes. Candidate retains raised visible sole and small heel division with a
more elongated shape. Proportions/perspective remain pending visual approval.

Raw crop only: no 596px local composition, pixel-lock/alpha guarantee, runtime
manifest or Harness PASS. Incidental other-shoe/background generation changes
must not enter production. Only transfer approved target-shoe pixels after
review. V4/blink loop and Consumer unchanged; all earlier studies preserved.
No publication, commit or push.

## 2026-09-06 — v6 rejected as hoof-like; elongated-shoe raw shape study

User clarified that the target shoe should be slender/long, not shortened.
Marked shoe-single-v6 legacy/do-not-propagate. New built-in imagegen studies
in `build/reimu-idle-intake-20260906/shoe-single-v7/`: two discarded attempts
(thick wedge, then wrong planted-foot pose) and candidate-crop.png, restarted
from v4 with a narrower elongated sole and visible underside. Exact prompts
and provenance recorded in REVIEW.md; preview.html compares original/candidate.

This is RAW generated crop, NOT a pixel-locked 596px candidate. Incidental
other-shoe/ankle/background changes must be discarded in later composition.
No alpha/outside-mask guarantees or Harness PASS claimed for it; no manifest
or animation built this turn. Await shape/perspective approval before local
transfer onto v4 and subsequent validation. V4 and its blink loop remain current.
No Consumer changes, publication, commit or push; previous images preserved.

## 2026-09-06 — single bulky shoe refinement from selected v4

User identified the foreground/image-right shoe as too bulky and authorized
only that shoe's static refinement before any animation update. New candidate:
`build/reimu-idle-intake-20260906/shoe-single-v6/`. Built-in generation followed
by restricted composition changes the target shoe, narrow opening join and
immediately exposed mat. Raw unwanted changes to the other shoe discarded.
Other pixels and all alpha remain exact v4; 2898 changed pixels within bbox
[244,490,311,551). Candidate is visibly slimmer and lacks the transverse sole
crease; final visual acceptance, including shoe/sock join, remains pending.

Includes 596/160 comparisons, closeup, raw generation, prompt, reproducible
script, static frame manifest and QA. Harness validate: 0 errors, 0 warnings.
SHA-256: 267ffd0d2eba446c6b0abc0053d83f3cc111782c2b8f3adbc6cb7fe105bf9287.
No new animation, Consumer writes, publication, commit or push. Selected v4
and its blink loop remain current until this candidate receives approval.
No core changes or full core test suite run in this art-only turn.

## 2026-09-06 — v4 selected; approved blink propagated to fixed forward legs

Maintainer abandoned v5 after left-shoe feedback and explicitly selected v4
as the construction basis. legs-forward-v4/REVIEW.md records static approval;
v5/REVIEW.md marks that candidate legacy/do-not-propagate. All art preserved.

New artifacts under `build/reimu-idle-intake-20260905/`:
- `blink-v2-legs-v4/`: neutral byte-identical to selected v4, half/closed reuse
  exact approved blink-v1 eye-mask pixels; three-frame sheets at 596/160px.
- `blink-loop-v2-legs-v4/`: reproducible builder, frame manifest, 40 full-canvas
  PNG frames, 4-second/10-fps APNG and lossless WebP at 596/160px, preview and QA.

Lower-body difference from the old kneeling neutral: 11771 pixels, bbox
[159,462,363,552). Eye/leg masks are disjoint. Across time all pixels outside
the eye mask, all alpha and all v4 lower-body pixels are fixed; first/last
files byte-identical. APNG disposal=0/blend=0, CRC and decoded RGBA exact;
WebP visible RGBA/alpha/timing exact but invisible transparent RGB discarded.
Both keyframe and loop Harness validate: 0 errors, 0 warnings. No core changes
or full core test suite run. Preview is for playback review, not publication.

Selected neutral SHA-256:
590e6242f39b62491a95718405aa19eff3a9ae658e49744915b6ddac8fd80621
596px APNG SHA-256:
ecc3790a4c84c138a2575785ea091a9350216e01bc1449e620b6eebecef9bbfc
Remaining hashes in loop qa.json. Consumer/task_2 unchanged; no publish,
commit or push. Next: review the propagated loop, then scoped Consumer idle
integration only with authorization. Do not return to v5 or modify approved v4.

## 2026-09-06 — forward-leg v5 shoe-volume refinement candidate

User approved narrowing v4 shoes about 10 percent, reducing toe/sole bulk and
slightly separating feet while retaining raised visible soles and concealed
short legs. `build/reimu-idle-intake-20260905/legs-forward-v5/` contains the
new static candidate, closeup/596/160 comparisons, raw generation/prompt,
reproducible scripts and pixel/hash QA. The percentage is a generation target,
not a measured guarantee. Fine angle/hem/contact details remain reviewable.
Outside-mask pixels and alpha unchanged; 11491 pixels changed within bbox
[159,462,363,552). SHA-256:
3361475e7afd789d87aa523c4c0c378bda7fe2166246a4800cd2a84f1e98c005.
Static review pending; no animation propagation, Consumer writes or publication.
Previous art and approved blink-loop-v1 preserved, no commit/push.

## 2026-09-06 — correction: visible soles are required; v4 from v2

Maintainer explicitly rejected the v3 planted-foot interpretation. V2's visible
soles and concealed short legs are correct; change only direction/stagger.
Do not continue from v3. Its REVIEW now marks it rejected, files preserved.
Online reference research was done on Hobby Japan's pose guide and CLIP STUDIO
TIPS; the user-supplied Reimu illustration remains the main pose reference.

`build/reimu-idle-intake-20260905/legs-forward-v4/` contains a v2-based static
candidate preserving both visible soles, toes angled more toward upper-left,
with a stronger stagger. Includes raw generation/prompt, script, masks/diff,
596/160 comparisons and QA. Outside-mask pixels and alpha unchanged;
11596 modified pixels in bbox [159,462,363,552). SHA-256:
590e6242f39b62491a95718405aa19eff3a9ae658e49744915b6ddac8fd80621.
Await visual review; no blink propagation, Consumer write, publish/commit/push.

## 2026-09-06 — forward-leg v3 oblique shoe angle candidate

Maintainer preferred v2 but asked to correct shoe angle using the sitting
reference. `build/reimu-idle-intake-20260905/legs-forward-v3/` contains a
static generated/local-composited revision, comparison sheets at 596/160,
leg closeup, masks/diff, prompt and reproducible scripts. Shoes show their
uppers/sidewalls instead of broad frontal soles, retaining short concealed
ankles and a slight stagger. Outside-mask pixels and alpha are unchanged;
qa.json stores exact hashes and modified bbox. Fine hem/contact joins remain
subject to visual approval. No blink propagation or Consumer changes, no
publish/commit/push. Prior versions and approved loop remain intact.

## 2026-09-06 — forward-leg v2: larger shoes, shorter concealed legs

Maintainer found v1 awkward and requested larger shoes with thinner, shorter,
more hidden legs. `build/reimu-idle-intake-20260905/legs-forward-v2/` provides
a new static comparison, leg closeup, source crop, generated patch/prompt,
explicit mask, diff and reproducible scripts. Most bare leg is concealed by
the ruffled hem, with only small ankle slivers visible; black shoes are larger.
Changed bbox vs v1 [159,462,363,551), 10855 pixels, outside-mask pixels and all
alpha unchanged. Candidate SHA-256:
6e59480adeea0f3f99e24b2357b48668a28a2a28050c3e7952d74f20dd6488c0.
Static visual approval pending. No propagation to blink frames; v1, approved
neutral/loop, Consumer and originals preserved. No publish, commit or push.

## 2026-09-06 — idle loop approved; forward-leg static alternative requested

The maintainer approved blink-loop-v1 playback, then requested a static
leg-pose comparison with the supplied third-party sitting/eating reference.
`build/reimu-idle-intake-20260905/legs-forward-v1/` now contains one locally
composited static candidate, generated raw output/prompt, 596/160 comparison
sheets, leg closeup, explicit edit mask, diff, reproducible script and SHA QA.
Only a lower-body patch was transferred to the accepted neutral; generated
upper-body/table drift was not adopted. Shoes point forward with slight offset.
Changed bbox [159,462,363,551), 10422 pixels; outside mask and alpha unchanged.
Local hem/mat boundaries still require visual review. This is generated edited
flattened art, not an inferred true source layer.

Candidate SHA-256:
4b9c8c7fcfceecb491a8a5b190005fcbb4b72e098a6f6e97a675a90632992e13.
Await static pose approval before applying to blink variants. Existing approved
loop and all sources preserved; no Consumer write, publish, commit or push.

## 2026-09-06 — idle blink keyframes approved; 4-second loop exported

The maintainer approved blink-v1 keyframes. The new
`build/reimu-idle-intake-20260905/blink-loop-v1/` packages those exact PNGs
into 40 logical frames at 10 fps: 3.4s neutral, 0.1s half, 0.2s closed,
0.1s half, 0.2s neutral. No new generated artwork. Source hashes are asserted;
first/last files match, all alpha and pixels outside the eye masks are fixed.

APNG and lossless WebP exported at 596px and 160px. APNG has 40 full-canvas
frames with disposal=0/blend=0 and exact decoded RGBA. WebP coalesces to five
timed frames; its visible RGBA/alpha and 4000ms timing are exact, but invisible
RGB under alpha zero is discarded. QA includes export SHA-256 values and the
CLI validation result: 0 errors, 0 warnings. This is the supported frame-manifest
workflow. No Harness core changes and no full core test suite run this art turn.

Preview page opened successfully in the in-app browser (loopback port 8124),
showing 596px/160px APNG and a 160px WebP comparison. Playback visual approval
remains pending. 596px APNG SHA-256:
bd5db90aadb0bd0f66d2da87d3019ec1f68c8eae10d6b9e596a772a620c40391.
Consumer and task_2 unchanged; no publish, commit or push. Next: review loop,
then scoped Consumer idle integration/preflight, not an automatic publication.

## 2026-09-06 — scene-repair-v2 accepted for next work; blink keyframe review

The maintainer replied “可以，那就接着做” to the scene-repair candidate. Use
its idle-596.png as the accepted neutral for this review; do not reopen the
missing-art request or claim its geometry exactly matches task_2.
`build/reimu-idle-intake-20260905/blink-v1/` contains neutral/half/closed RGBA
596px keyframes, 596/160 sheets, eye closeup, explicit edit mask, diff PNGs,
source generated closeups, prompts, reproducible scripts and QA hashes.
Generated edits are composed only in two eye polygons; neutral is byte-identical
to the accepted source and pixels outside the polygons plus all alpha are exact.
An extra generated brow in the half pose was locally removed. Human review of
hair-adjacent mask seams remains required; these are not authored source layers.

The non-looping keyframe manifest validates with 0 errors and 0 warnings in
human and JSON CLI modes. No full loop or animation export made. Next gate is
keyframe visual approval, then blink timing and playback review. Consumer,
task_2, legacy sources unchanged; no publish, commit or push.

## 2026-09-06 — missing-art generation authorized; scene repair candidates

The maintainer said they cannot draw and explicitly authorized us to source
or generate missing artwork. Do not repeat the previous demand that they
provide hand-drawn empty-table art. This permission is scoped to this idle
repair, not retrospective changes to published task_2 or automatic publication.

Two built-in imagegen edit attempts and exact prompts are preserved under
`build/reimu-idle-intake-20260905/scene-repair-v2/`. Attempt 2 is the review
candidate. Both outputs were RGB with baked checkerboard; the existing
authorized local alpha extraction produced native RGBA plus 596/160 previews.
Native RGB preservation refers only to extraction versus generated attempt 2,
NOT preservation versus approved originals. No true layers are inferred.

Visual review confirms remaining table/leg/mat registration differences and
upper-character drift. Do not claim completed alignment or start blink on a
supposedly accepted neutral. Candidate SHA-256:
954a2543f21b2873da769eb9d37e95271a5e4567aa34b88086825465b8696050.
Static Harness plan/render/validate: 0 errors, 1 expected ZERO_MOTION warning.
Consumer and original art remain unchanged; no publish, commit or push.

## 2026-09-06 — registration repair requested; blocked on scene artwork

The maintainer requested correcting the scene differences before blink work.
Read-only inspection confirms this needs artwork, not a placement adjustment:
idle and task_2 have different tabletop perspective, leg geometry and tatami
silhouette. The existing shared table has occlusion holes and the shared
tatami has reconstruction marks; neither is a clean master replacement.
Do not fabricate these missing surfaces by stretching or coarse segmentation.

Evidence and reproducible comparison are in
`build/reimu-idle-intake-20260905/registration-review/`. The 596px/160px sheets
show current idle, task_2, a 50-percent overlay, and visible RGB difference on
an explicit common background. The 200691 differing pixels include the
intentional character-pose differences, NOT just scene defects. The highlighted
repair rectangle is a brief, not an authored layer mask. Source hashes are
unchanged. No corrected mother or blink frames were created this turn.

Required next input: a clean empty scene matching task_2, with the approved
idle elbow/table occlusion resolved. Review the repaired neutral before blink.
This supersedes the earlier unconditional next-blink instruction. Static
alpha-v1 validation was rerun: 0 errors, 1 genuine ZERO_MOTION warning; not
an animation-completion claim. Consumer remains unchanged, no publish/commit/push.

## 2026-09-06 — local idle alpha extraction completed

The maintainer delegated the local editing method after the failed generated
background removal. `build/reimu-idle-intake-20260905/alpha-v1/` now contains
the preserved-RGB native RGBA cutout, 596px/160px derived review PNGs,
dark/light/task_2 comparison sheets, reproducible prepare.py, and QA.
Exterior-connected bright neutral checkerboard pixels receive alpha zero;
native RGB changed-pixel count is zero. This is whole-sprite extraction,
not inferred art layers. Visual inspection at both review sizes found no
obvious cutout holes; binary-alpha fringe limitations are documented.

596px mother SHA: 1355abab88314a2394372f3918cbb6bcdf6a778e340a6cdbc36a154f4d357000.
Placement uses uniform 580px sampling plus (8,8) padding. Different table and
tatami shapes remain a cross-state registration limitation, not a solved
pixel-alignment claim. Harness validates the static mother with zero errors
and one expected ZERO_MOTION warning. No fake animation or placeholder event
was introduced. Consumer is unchanged; next art work is the blink keyframes.

## 2026-09-06 — approved idle candidate, background edit failed

The maintainer approved candidate-v1 and requested background cleanup and
alignment work. A built-in ImageGen background-only edit again returned RGB
1254x1254 with a baked checkerboard and visibly altered foreground shapes.
It is preserved as a rejected attempt under
`build/reimu-idle-intake-20260905/background-attempt-v2/`. Candidate-v1 remains
the approved pose reference. No transparent neutral, geometric registration,
596px/160px transparent QA, or blink frames have been completed. Next proposed
route is explicit local background-mask/alpha editing of candidate-v1; awaiting
user selection of that editing method. Consumer and published v9 remain intact.

## 2026-09-06 — idle mother pose candidate (review only, asset gate failed)

The maintainer accepted proceeding with a task_2-style chin-in-hands idle
mother. A built-in ImageGen pose candidate and exact prompt are preserved in
`build/reimu-idle-intake-20260905/candidate-v1/`. This is generated concept
art only: the existing prohibition against ImageGen pixels in finished assets
remains in force. The output is RGB 1254x1254 with a baked checkerboard, and
the table registration differs from the master; it is not a transparent
production mother and has not passed Harness asset validation. The pose is
available for visual review; no blink frames or Consumer edits were made.

## Latest follow-up: eating idle intake and cross-tier review

Continued from the published v9 loop by auditing the six current eating base
images. Review outputs and the reproducible read-only audit are under
`build/reimu-idle-intake-20260905/`: `REVIEW.md`, `inventory.json`,
`states-596.png`, `states-160.png`, and `audit.py`.

The eating idle reference is a chin-in-hands pose with an empty table, SHA-256
`2ae03a533cd5416b1da5b6a9f692bd46ad3c91fd584f32f3c98b9ec347ce0781`.
It differs from the approved Codex idle row's eating-mother source SHA
`0251947e…`; that row must not be silently substituted for food tier zero.
The 160px sheet visibly shows differing character proportions and table
placement between the revised task_2 mother and the other five older states.
Do not normalize them through whole-image bbox scaling.

Proposed next idle art is neutral / half-closed eyes / closed eyes, preserving
the supporting hands and facial contact. Only neutral currently exists;
half-closed/closed poses require authored art. Four state-specific required
layers are absent under the existing generic layer contract, and the existing
shared task_2 layer files have not been validated against idle's composition.
The empty tabletop also differs from older prose suggesting tea-only; preserve
the reference until a deliberate cross-tier art revision is selected.

Read-only Consumer no-publish checks for idle and task_2 are saved under
`baseline-check/`: idle is a valid one-frame fallback with expected
`ZERO_MOTION` (not a completed animation); task_2 validates 16 frames with
zero errors and warnings. All six base hashes remained unchanged. No Consumer
files, new art poses, runtime publication, commit or push occurred in this
follow-up. Resolve the shared visual baseline before expanding final art.

Last updated: 2026-09-05 — task_2 v9 is now the published Consumer runtime.
The maintainer approved the complete loop, authorized legacy cleanup and
publication, and the Consumer completed guarded import, three matching
no-publish builds, transactional publication, full repository checks and a
fresh live task-count-2 load. V7 and v8 remain preserved legacy/comparison
artifacts. The Harness core was not changed. Keyframe tracks remain implemented on top of the
discrete-variant pilot; package remains **0.7.0**, nothing committed or pushed.

The M4/M5 verification records below describe the pre-publication working
tree. Their "no commit/push" statements are historical; publication was
subsequently authorized after the strict review and complete offline
acceptance passed.

## Maintainer-confirmed product priority (2026-09-04)

The product is a reusable layered desktop-pet system, not a collection of
standalone GIFs. The end-to-end target remains:

`task count → clamp to food tier 0–5 → select character state → load and
validate its manifest/layers → compose and play → fall back to the approved
flattened still when required assets are unavailable`.

Repository ownership stays split: Sprite Harness provides provider-neutral
asset validation, composition, deterministic previews/exports and QA; the
`gensokyo-codex-pets` consumer owns task sources, state mapping, playback and
runtime fallback. Codex standard action rows such as `idle`, `running` and
`review` are a separate state space and must not be reported as completion of
the eating `task_2` vertical slice.

The latest maintainer-approved visual direction supersedes the older moving
hand/bite experiment for the current `task_2` iteration: start every frame
from the approved flattened mother/base image; keep the rice ball, hands,
sleeves, body, hair, neck, collar, table, eyes and mouth pixels fixed; keep the
eyes open; and show chewing only through a restrained one-sided jaw/cheek
contour change that follows the existing three-quarter view. No whole-face
scaling, blink, open-mouth chew, generated repainting or global color change is
allowed. Dynamic hand-to-mouth motion remains a future system capability, not
current approved `task_2` artwork.

The current cross-repository milestone is to reuse the completed task_2 v9
vertical slice for the remaining eating tiers, beginning with real reviewed
idle/task_0 or task_1 art. Live task-count input and the partially completed
Codex v2 atlas remain separate workstreams.

## Chew v9 asymmetric-cheek keyframe review (2026-09-05, published in Consumer)

The v8 loop exposed a spatial rather than temporal problem: its near-cheek
puff field began at +3px on one scanline and reached +5px immediately below,
forming a pointed pink wedge at the fixed hair boundary. V9 does not add timing
in-betweens. Instead, it extends that source contour vertically and tapers the
integer row offsets from 0 through +1/+2/+3/+4/+5 and back to 0. The image-left
far cheek adds only −2px puff / +1px compress as a subordinate response, so the
three-quarter face remains asymmetric rather than being scaled symmetrically.

The revised keyframes remain under
`build/reimu-task2-eating-keyframes-20260904/review/chew-v9-asymmetric-cheeks/keyframes/`.
Neutral is still the approved base SHA `0251947e…`; compress is `57bf28a9…` and
puff is `5ba18281…`. Compress changes 729 pixels / 62 at nearest-neighbor 160px;
puff changes 870 / 60. All changed values are transported from the neutral;
protected overlap is zero for eyes/brows, mole, hands, food core, neck/collar,
table and tatami. Harness validates all three external exact frames with zero
errors/warnings; review QA SHA-256 is `3d62acf9…`. The validated v8 loop remains
preserved only as the comparison parent.

After keyframe approval, the formal v9 loop was built at
`runs/chew-v9-asymmetric-cheeks/loop/`, reviewed under
`review/chew-v9-asymmetric-cheeks/loop/`, and exported under
`exports/chew-v9-asymmetric-cheeks/`. It uses 16 frames at 10fps for 1.6
seconds with two neutral → half-compress → exact compress → cross-mid → exact
puff → half-puff → neutral beats. Frames 2/9 and 4/11 match the approved v9
compress/puff hashes; frames 0/15 are the approved neutral pixel-for-pixel.
There are six unique poses, a 1,071-pixel dynamic union with bbox
`[218,255,353,280]`, zero protected overlap and zero new RGBA values.

All 596px/160px APNG frames are full canvas with disposal=0/blend=0 and decode
exactly. Lossless WebP reproduces every visible RGBA pixel and alpha plane.
Harness validation is zero errors/warnings. Review QA SHA-256 is `09a339df…`;
596px APNG/WebP are `ca88e217…` / `ec1ec8d1…`; 160px APNG/WebP are
`b33265bf…` / `8987a517…`. The maintainer approved the full loop and authorized
continuing into the Consumer pre-publication stage.

## Consumer v9 source import, preflight and publication (2026-09-05)

The Consumer now contains a separate pinned
`pets/reimu/animations/eating/sources/task_2-chew-v9/` package. Its guarded
importer accepts only animation id
`reimu_task2_chew_v9_asymmetric_cheeks_loop`, approved Harness plan digest
`sha256:cfe76138…`, neutral SHA `0251947e…`, zero-warning QA and the exact 16
frame digests. Five importer regression tests cover acceptance, frame tamper,
warning rejection, deterministic/idempotent import and checked-in manifest
identity. Source manifest SHA-256 is `81aa07c5…`.

Two independent Consumer builds under
`consumer-preflight/chew-v9-preflight-{a,b}/` used a disposable v9 config and
`--no-publish`. Both validate 16 external frames at 10fps with zero errors and
zero warnings, share Consumer plan digest `sha256:44a06825…`, and reproduce the
pinned source frames byte-for-byte. Their 23 non-location files are identical
with canonical tree SHA `779c7e03…`; the only raw tree difference is each
`report.json` recording its own absolute A/B directory, and normalized reports
are identical. Full facts and production guards are in
`consumer-preflight/chew-v9-preflight-report.json`.

After explicit maintainer authorization, the Consumer verified that the
pre-existing `assets/reimu/eating/task_2/frames/frame_000 2.png` alias was
byte-identical to the named legacy fallback (SHA `d3139f4e…`), recorded the
canonical asset and retired alias in `legacy-assets.json`, and removed only
the redundant runtime-directory copy. A third production-config no-publish
build matched the two preceding builds with canonical non-location tree SHA
`779c7e03…` and zero Harness errors/warnings.

The Consumer then transactionally published all 16 v9 frames. Production
`animation-set.json` and runtime provenance now select
`task_2-chew-v9/source.json`; animation manifest SHA is `607b6760…`, source
manifest SHA is `81aa07c5…`, and every runtime frame matches its pinned source.
Base/frame 0/frame 15 remain neutral SHA `0251947e…`; the canonical legacy
fallback remains `d3139f4e…`. All 104 Python tests, app runtime checks and the
repository check pass. A fresh localhost task-count-2 load reports 16 validated
looping frames in full-motion mode. No commit or push was performed.

## Chew v8 researched loop review (2026-09-05, not published)

The maintainer found the published v7's one-direction 2–3px jaw change too
small and requested comparison with other chibi eating loops. Reference review
was used only to identify motion patterns; no third-party pixels were copied or
stored. The resulting `chew-v8-researched` pilot remains entirely under
`build/reimu-task2-eating-keyframes-20260904/`.

V8 adds an opposing `compress` pose before `puff`: the closed-mouth/rice-ball
contact interface moves at most +1px / −2px, while the existing image-right
lower cheek/jaw interface moves −2px / +5px. This creates roughly 10px of
asymmetric cross-pose width excursion at 596px without opening the mouth or
scaling the face. Eyes, brows, mole, hands, food core, clothes, hair mass,
neck, collar, table and tatami remain fixed. Every changed RGBA value is moved
from the approved neutral.

Harness validates the three external keyframes with zero errors/warnings.
Compress changes 427 pixels at 596px / 34 after 160px nearest reduction; puff
changes 482 / 33. Neutral SHA-256 is `0251947e…`, compress `26803651…`, puff
`01883920…`, and review QA `7dd1c686…`. A diagnostic lossless-WebP toggle is
provided at face-crop 4×, 596px and 160px solely for visual approval; it is not
the final timing.

The maintainer accepted the keyframe direction, so Harness now also contains a
formal loop at `runs/chew-v8-researched/loop/`, with review files under
`review/chew-v8-researched/loop/` and 596px exports under
`exports/chew-v8-researched/`. Its 16 frames run at 10fps for 1.6 seconds and
perform two beats: neutral → half-compress → approved compress → cross-pose
transition → approved puff → half-puff → neutral. Frames 2/9 and 4/11 match the
approved compress and puff SHA-256 values exactly; frames 0/15 match the
approved neutral pixel-for-pixel. There are six unique RGBA poses. The dynamic
union is one connected 603-pixel region with exclusive bbox
`[285,257,348,280]`; maximum per-row offset change between adjacent frames is
4px. Protected-region overlap and new RGBA-value counts are both zero.

APNG exports use sixteen full 596×596 (or full 160×160) frames with
disposal=0/blend=0 and decode exactly. WebP exports are lossless and reproduce
every visible RGBA pixel and alpha plane. Harness validates the external exact
frames with zero errors/warnings. Review QA SHA-256 is `d9540ab5…`; 596px APNG
and WebP are `e398a105…` and `a88c4c37…`; 160px APNG and WebP are `677287dd…`
and `6d7c3821…`. The GIF is Harness compatibility output only. The complete
loop still requires maintainer visual approval before any consumer import or
replacement of v7.

## Consumer exact-frame activation and publication (2026-09-05)

The consumer now holds a pinned 16-frame `task_2` chew-v7 source package and a
new consumer-only `source_mode: exact_frames`. This does not change the Harness
contract or core: the consumer calls `plan` against the approved neutral,
installs its reviewed pixels as external build frames, then calls
`validate --write-qa → preview → contact-sheet → report` through the public
CLI. Harness correctly reports backend `external`, skips `render_manifest`,
and validates source identity, plan consistency and all frame files.

Independent consumer preflight build directories under
`build/reimu-task2-eating-keyframes-20260904/consumer-preflight/` are
byte-identical. Each has 16 frames at 10 fps, zero errors and zero warnings.
Key hashes: exact source manifest
`7bb06b7ee57dcac21288220464fa63b36c4f1f76148f7eef8f83da7b65a50a62`,
frames QA `7f201575cdf74c622691d2a79a5f281a3dd3713891a649df529bdc35c4eaf9dd`,
contact sheet `26f2d0147ee6405f89ad0a7245d017a802197d8de2ca9a9c1cf43d0705ebd959`.

The preflight also recorded why publication could not mix the old runtime
fallback SHA `d3139f4e…` with the approved neutral SHA `0251947e…`; the
layered static reconstruction differs from that neutral in 204,953 visible
RGBA pixels. After explicit maintainer authorization, the consumer preserved
the old fallback as `base-eating-set-v1-legacy.png`, activated the approved
neutral, completed two additional byte-identical production-config preflights,
and transactionally published all 16 frames. Harness reported zero errors and
zero warnings; runtime base, frame 0 and frame 15 are byte-identical. Published
consumer animation manifest SHA-256 is
`2aa4c3b6f4787155802c1d488cfc7bcbeea26c747be783c9a3c7453407f28c28`.
No Harness release, core change, commit or push follows from this consumer
work.

## Keyframe tracks (2026-09-04, uncommitted)

The working tree adds a second, mutually exclusive track kind: **keyframe
tracks** (`keyframes: [{at, value, interpolation}, …]`), designed for natural
multi-phase layered motion (approach → mouth open → bite → retract → chew)
that a single whole-loop curve cannot express. Semantics
(docs/animation-plan.md, "Keyframe tracks"):

- `at` is normalized loop time (FPS-independent): loops sample `i / n` in
  `[0, 1)`; non-loops sample `i / (n − 1)` and reach 1 on the final frame.
- `value` is the direct sampled value in the existing composition semantics
  (px, deg; scale/opacity factor stays `1 + value`), so all effective-value
  safety rules apply unchanged.
- Per-segment `interpolation`: `linear`, `ease_in`, `ease_out`,
  `ease_in_out`, `hold` (exact step on the next keyframe — no cross-fade).
- Loop closure: the final segment interpolates from the last keyframe back to
  the first keyframe's value, reaching it exactly at time 1 ≡ time 0; a
  non-looping tail holds the last value. Keyframe tracks declare no `cycles`.
- Exact keyframe hits, six-decimal rounding, and byte-identical artifacts are
  preserved; the sampler lives in `curves.py` beside the cycle curves, and
  expansion/geometry/validation share one `sample_track` dispatcher.
- New stable codes: `TRACK_MODE_CONFLICT` (exit 2, mixing `keyframes` with
  `amplitude`/`curve`/`cycles`/`phase`/`duty_cycle`),
  `INSUFFICIENT_KEYFRAMES`, `INVALID_KEYFRAME_TIME`,
  `INVALID_KEYFRAME_VALUE`, `UNSUPPORTED_INTERPOLATION`.

Curve tracks are untouched (field order, defaults, digests, and `plan.json`
bytes for existing plans are unchanged); old plans need no migration. The
pilot's `pulse` + `duty_cycle` implementation was reviewed and formalized
as-is — pulse remains the cyclic binary switch, keyframed `hold` opacity is
the aperiodic one. Verification: 669 tests pass (609 baseline), compileall
clean, full CLI plan/render/validate/preview/contact-sheet acceptance in
human and JSON modes, and an offline installed-package CLI acceptance from
outside the repository.

**Version recommendation:** this is a backwards-compatible contract addition;
by the project's precedent (0.4.0 → 0.5.0 for layered input) the next
*publication* should bump the minor version to **0.8.0**. The working tree
deliberately keeps `pyproject.toml` at 0.7.0 because nothing is being
released from this change; bump at publication time.

## Local discrete-variant pilot (2026-09-04, uncommitted)

The current working tree adds a provider-neutral `pulse` track curve with an
optional `duty_cycle` in `(0, 1]`. The curve returns exactly `+1` during the
active fraction and `-1` otherwise. Complementary local opacity tracks can
therefore switch mutually exclusive layered variants without cross-fading or
half-visible composite frames. The schema, parser, normalizer, geometry path,
semantic validator, public docs, and regression tests are updated together.

This capability was exercised in a disposable, no-publish Reimu `task_2`
pilot: one exact closed-eye frame in a 12-frame loop, plus a restrained
layer-motion comparison and an always-open control. That pilot is historical
evidence for the generic track capability, not the current art direction: the
maintainer subsequently locked the first approved `task_2` loop to open eyes
and fixed hands/food/body with jaw/cheek-only motion. Production consumer
configuration and source layers remain protected by before/after inventories.
Do not copy the temporary pilot animation plan into the consumer, bump the
package, commit or push as a consequence of this experiment.

## First consumer integration: gensokyo-codex-pets (2026-09-03)

Sprite Harness 0.7.0 is now consumed in production by
[gensokyo-codex-pets](https://github.com/lyw-ops/gensokyo-codex-pets)
(commit `c9d921b`, `docs/sprite-harness-integration.md` there) for the Reimu
Eating Set: six real 596×596 flattened RGBA sprites, one single-image v1
Animation Plan per state, driven end to end through the public CLI only —
`plan → render → validate --write-qa → preview → contact-sheet → report`, all
in `--json` mode from subprocesses with exit-code checks. **No harness core
change was needed and none was made**; no character-specific logic entered the
harness. This section records what the integration exercised and observed so
future harness work does not re-derive it.

What the consumer run confirmed in practice:

- The identity/static path works as designed: `frame_count: 1` plans with no
  tracks validate with only the expected `ZERO_MOTION` warning, and the
  rendered frame is **byte-identical to the source** through the exact
  integer-copy path — the consumer relies on this for its baseline frames.
- Determinism held at the consumer boundary: repeated full builds (plan through
  publish) produced byte-identical artifacts, letting the consumer treat
  "rebuild is a no-op diff" as a repository check.
- The flattened-vs-layered boundary is confirmed by measurement, not just
  contract: a restrained whole-sprite `translate_y` (±2 px) experiment rendered
  and validated cleanly, and per-frame alpha bounding boxes showed the ground
  line (tatami bottom) moving by the full amplitude with the rest of the scene.
  The consumer therefore shipped an identity baseline instead of fake motion —
  exactly the outcome the `TARGET_TRACKS_SKIPPED` / no-decomposition contract
  is meant to force.
- `--json` outputs were machine-consumed throughout; stable exit codes and the
  `errors`/`warnings` shapes were sufficient to gate publication (validation
  failure or any unexpected warning blocks the consumer's publish step).

Consumer-side observations (working as specified; recorded as API-ergonomics
notes, not bugs):

- Constraint values must be strictly positive (`INVALID_CONSTRAINT` for `0`),
  so a deliberately static plan declares a minimal 1 px budget rather than 0.
- Top-level JSON success flags differ by command: `plan` reports `success`,
  `validate` reports `valid`. Consumers must read the right key per command;
  a future (non-breaking) unification could add a shared field.
- `CONTENT_TOUCHES_EDGE` fires for test fixtures whose opaque pixels reach the
  canvas edge — correct behavior, worth remembering when writing tiny
  generated test images (give them a transparent border).

Next step for this consumer (drives future harness usage, not core changes):

1. Explicit layered Reimu PNGs (body/head/eyes/mouth/hand/food/table/tatami)
   are the consumer's next art milestone; the eating states then move to
   **Animation Plan v2** inline `source.layers` with local tracks (breathing,
   head bob, eating hand, blink, chew) — the M3 contract as shipped, no new
   harness capability required. The consumer's spec/builder already pass
   per-state plan overrides through, so v2 adoption is a data change there.
2. After layered clips exist and Codex standard-row performances are designed,
   the consumer plans to use the **M5 `export`** grid atlas for the Codex v2
   sheet (its 8×11 / 192×208 target matches the generic fixed example). Food
   tiers are not Codex rows; that mapping stays consumer-side.
3. **M4 generation remains unused and unauthorized** in the consumer pipeline;
   its builds are offline and deterministic by policy.

## Current delivery and remaining live step

M1–M5 engineering is implemented. M4 adds optional, explicit source-space PNG
replacement generation through external processes; M5 adds deterministic grid
atlases and complete offline pixel round trips. The real OpenAI adapter is a
separate installable distribution (`sprite-openai-adapter` 0.1.0), with real
request construction/authentication/response handling tested through a local
HTTP service. **Live provider acceptance is NOT completed**: no usable key or
paid-call/source-upload authorization was available. No real model request was
made. The offline geometric adapter is explicitly a test substitute.

## Actual starting state and preservation

Started from `main`, HEAD `b27c6d9de84a6f3a982b9ebd76e742b43f93e68e`,
package 0.5.0, with the complete uncommitted M3 working tree. Baseline execution:
**381 passed in 2.25s**. The render rollback/retained-marker safety, all-source
identity checks, exact RGBA recomputation, strict versions and two-stage M3
geometry were present. No M3 reimplementation, reset, clean, stash, clone,
commit or push was used. Every baseline file is still present; all 12 original
test files, including untracked M3 tests, have unchanged byte hashes. See
[baseline.json](../verification/m4-m5/baseline.json) and
[preservation.json](../verification/m4-m5/strict-review/preservation.json).
The old M3 handoff is preserved below as historical context.

## Contract decisions and versions

| Artifact | Version/compatibility |
| --- | --- |
| Package | 0.5.0 → 0.7.0 directly; no intermediate release |
| Animation Plan / frame plan | v1 single-image and v2 explicit layers unchanged |
| Render | v1 deterministic unchanged; v2 strictly requires generated-input backend and request/accepted digests |
| Generation spec / request / response / accepted inputs | Each starts at strict v1, separate version keys |
| Export spec / normalized config / atlas | Each starts at strict v1 |
| QA | Existing plan/build/frame v1 retained; generation/export v2 binds subjects |
| Frame manifest | v1 unchanged; export accepts existing external frames through validated build inputs |

No mechanical migration of old builds is required. Four actual pre-existing
0.5.0 single/layered full/hold builds were validated by installed 0.7.0.
Canonical integer types are checked at runtime (including rejection of 1.0
and booleans); JSON Schema's mathematical integer convention alone cannot
express the lexical 1 versus 1.0 distinction. All new schemas ship with the
package and parity tests ensure they match schemas/.

One generation spec maps each unique request id to an existing target and an
explicit set of frames; one candidate is explicitly reused across that set.
Request/response identity, coverage, size, alpha and content hashes are checked
before copying accepted PNGs into generation/inputs. Copied source references
and the spec snapshot let adapters resolve all request paths during staging.
The accepted manifest separately binds the original spec path/hash. Request
normalization is recomputed from the original spec and verified plan. Changes
to seed, source, instruction or mapping invalidate old generated artifacts.

`render --generated-input` replaces source pixels before unchanged M2/M3
transforms; ordinary render uses originals. Unmapped frames use originals;
requested-but-missing results fail. Hold always selects actual frame 0 (with
originals for its unmapped targets), then freezes the complete composition and
pose. Offline validation never runs an adapter, but rechecks original and
frozen inputs and recomputes final RGBA/geometry, including hidden RGB.
Global constraints and final nonempty-frame requirements remain active.

The item seed derives from SHA-256 over the documented canonical tuple, never
Python hash/time/temporary paths/arrival order. OpenAI Images does not expose
the requested seed capability: the adapter requires allow_unsupported and
reports false. Frozen input replay is byte deterministic in the same runtime;
new stochastic model invocations are not promised to repeat. Hashes and bbox
checks cannot establish action semantics, aesthetic quality or provider
identity. QA explicitly marks those checks skipped. Local digests are not
cryptographic provider authentication or protection against replacing all
trusted inputs together.

M5 preserves full canvases, uses integer top-left padding and row-major cells,
and never trims/rotates/scales/extrudes/duplicates frames. It reconstructs
layout, timing and pivots from configuration and validated builds, then checks
every source crop and all unused RGBA bytes. Source-frame PNG byte hashes are
observations separate from RGBA requirements, so full-mode re-encoding remains
compatible; held frame sets still require mutual byte identity. Metadata,
input mode/identity and stale export QA are checked offline.

## Safety and failure behavior

Existing render publication remains in place. New generation/export stages
publish complete directories with exclusive markers, previous-output backups
and reversible renames. Generation also holds the existing render lock.
Publication/staging/rollback/cleanup failures, forced exits, concurrent readers
and writers, symlinks/dangling links/hard-link aliases, unknown files and input
changes were exercised. Inputs are checked again before publication; validation
also checks identity stability. These checks do not create an atomic snapshot
across directories, protect against arbitrary hostile filesystem races, provide
power-loss durability, or sandbox a trusted executable's OS permissions.
See [transactions.md](transactions.md) for recovery; never delete a marker to
silence a failed validation. Malformed/invalid/missing/processing exits remain
2/1/3/4, with strict JSON even for CLI argument errors.

Provider process/stdout/stderr, timeout, response/image limits and redacted
error mapping are in [adapters.md](adapters.md). Redirects are disabled.
The core never retries; optional provider retries are limited to one 429.
Unknown-outcome timeouts, interrupted downloads and 5xx are not retried.
No credentials, provider raw errors or credential-bearing headers are logged.

## Final executed verification

Strict review rerun: **594 passed in 14.44s**.
This comprises all 381 baseline tests plus 213 new cases. Original test files
were not edited, removed, skipped or weakened. New independent pixel oracles
check source replacement, local/global ordering, alpha-over rounding, opacity,
frame-0 freezing, full-canvas placement and hand-computed atlas pivots/rects.
The real provider adapter has both a local HTTP service test and injected
transport tests for errors, finite retries, timeouts, bad outputs and redaction.

The subsequent strict review reproduced and fixed input-snapshot gaps in
generation/export normalization and export-config validation. It also fixed
staged copy destinations that could alias and overwrite original sources,
undeclared adapter files being published, and undeclared directories being
ignored by offline bundle validation. Nine regression cases failed before
their respective fixes and now pass. See the detailed
[review report](../verification/m4-m5/strict-review/review.md).

Every final engineering gate exited 0: pytest, compileall, current package
reinstallation, separate adapter installation, pip check, git diff --check,
and installed-CLI acceptance. No dependencies were downloaded for installation.
Package metadata, runtime import and CLI all report 0.7.0. Imports resolve from
`.venv/lib/python3.14/site-packages`, not the repository source tree.

Installed CLI acceptance made **103 subprocess calls**, including **101 harness
CLI calls**, from a temporary cwd outside the repository with PYTHONPATH
removed. Expected and actual exits matched throughout, including 0/1/2/3/4.
Success/failure JSON and all JSON artifacts passed a parser rejecting duplicate
keys and nonfinite tokens. Human modes exercised plan/generate/render/validate/
preview/contact-sheet/export/validate-export/report. All original example input
hashes remained unchanged. Full and held renders and repeated atlas exports
were checked for deterministic bytes; same-bbox corruption failed, full-mode
PNG re-encoding passed, and the installed real adapter refused missing auth
without contacting a provider. Existing 0.5.0 artifacts also validated.

Final logs and artifacts:

- [gates.json](../verification/m4-m5/strict-review/gates.json): exact verification commands, exits and complete stdout/stderr.
- [pytest.log](../verification/m4-m5/strict-review/pytest.log): full-suite output.
- [cli-commands.json](../verification/m4-m5/strict-review/cli-commands.json): every installed CLI invocation and expected/actual exit.
- [cli-summary.json](../verification/m4-m5/strict-review/cli-summary.json): installation identity, pipeline outputs, source hashes and live status.
- [visual-qa.json](../verification/m4-m5/strict-review/visual-qa.json): actual atlas/contact-sheet inspection and file hashes.
- [review.json](../verification/m4-m5/strict-review/review.json): review findings, verification results and final Git state.

`build/m4-m5-strict-review/` contains the latest binary artifacts (ignored
build products, retained locally). The earlier initial/final/release runs
are retained as preceding checkpoints; strict-review/ is the latest gate record.

## Reproduction and pipeline locations

Use fresh output directories. One command performs tests, compile checks,
installation, pip/diff checks and installed outside-repository CLI acceptance:

```bash
.venv/bin/python scripts/verify_m4_m5.py \
  --output verification/m4-m5/review-rerun \
  --acceptance build/m4-m5-review-rerun
```

The fake HTTP service needs permission to bind localhost. No live provider
traffic occurs. To run just the examples after installing both local packages:

```bash
.venv/bin/python scripts/acceptance_m4_m5.py --output build/m4-m5-demo
```

Under the latest `build/m4-m5-strict-review/` directory:

| Pipeline | Outputs |
| --- | --- |
| Old M2 single-image | single/build-full, single/build-hold, single/atlas-full, single/atlas-hold |
| M3 three-layer | layered/build-full, layered/build-hold, layered/atlas-full, layered/atlas-hold |
| M4 offline test adapter | generated/build-full, generated/build-hold, generated/atlas-full, generated/atlas-hold |
| Multi-clip fixed grid | multi-atlas-full, multi-atlas-hold; configs multi-full.json and multi-hold.json |

Every build has frames, preview.gif, contact-sheet.png, render.json and frame
QA. M4 builds additionally contain the complete generation bundle and generation
QA. Every atlas directory has atlas.png, atlas.json, export-config.json,
export-spec.json and export.qa.json. The multi-clip atlas is 1536x2288: 8x11
cells, each 192x208, 8px padding. Explicit order is generated → single → layered,
36 used cells and 52 transparent empty cells. Full and hold exports are separate.
Actual final atlas and generated contact sheet were visually inspected: the
specified candidate-frame changes, clip order, grid gaps and empty rows match
the contract. This is geometric layout QA, not model-semantic acceptance.

For individual commands use the exact installed invocation list in the CLI
log or the command contracts in generation.md / atlas.md. The generic fixed
example also lives at examples/grid-atlas/export.json.

## Changed files for review

New core modules: contracts.py, generation.py, atlas.py, transactions.py and
packaged schemas under src/sprite_harness/contracts/. Integration changes:
build.py, render.py, layers.py, cli.py and qa.py. The new real provider adapter
is entirely under adapters/openai; the core's dependencies remain Pillow and
PyYAML. New tests are test_generation.py, test_atlas.py,
test_generation_export_safety.py, test_provider_adapter.py and
test_new_contracts.py. New scripts create geometric inputs, run the offline
adapter, run optional authorized live smoke, and reproduce all acceptance/gates.
HARNESS, README, roadmap, architecture, animation-plan, renderer, layered-sprites
and handoff are updated. New contract docs are generation.md, adapters.md,
atlas.md and transactions.md. New examples are generated-placeholder/ and
grid-atlas/. pyproject/runtime are 0.7.0; render/QA schemas are versioned unions.
The underlying uncommitted M3 diff remains part of the reviewable worktree.

## Known limits and next step

No known unresolved deterministic pipeline/engineering gate failures remain.
Generation/export have documented memory/file/dimension quotas. Export requires
accessible validated builds; external frames are accepted through the existing
build contract, not raw directory scans or standalone frame manifests. No
trimming, rotation packing, scaling, extrusion, runtime-specific compatibility,
automatic decomposition, interpolation, optical flow, video or GUI is included.
Exact rendering requires the same Pillow/runtime environment.

The only remaining provider acceptance step is an explicitly authorized live
call with a usable OPENAI_API_KEY. It can use the prepared original 1024x1024
geometric smoke workflow:

```bash
.venv/bin/python scripts/live_provider_smoke.py \
  --output build/live-smoke --authorize-paid-call
```

The chosen provider adapter supports only documented native output sizes and
refuses tiny source images. It does not resize, repair alpha or guarantee a
seeded model result. Live success must be recorded from that actual run; package
installation and local transport success do not count as live acceptance.

Final Git HEAD and branch remain `b27c6d9` / `main`. All work is uncommitted and
unpublished for independent review; no commit or push was performed.

---

## Historical M3 handoff (preserved from the starting worktree)

Last updated: 2026-09-03 — milestone 3, package 0.5.0.

## Status and actual baseline

M1, M2 and M3 are implemented. M3 renders explicitly supplied PNG layers;
M4 AI generation and M5 atlas/exporters remain unimplemented. No automatic
sprite decomposition, skeleton, IK, mesh, mask system, video or GUI is claimed.

Work started on `main`, commit `b27c6d9` (`Implement milestone 2 renderer with
safe publication and pixel validation`), package 0.4.0, with a clean working
tree. The existing 229 tests passed before edits. Inspection confirmed all M2
review fixes: source/output aliases, whole-generation publication and rollback,
interrupted-transaction blocking, exact decoded RGBA verification, and strict
render-version types. No M2 fixes had to be recreated from an older baseline.
No commits or pushes were made. The completed implementation remains in the
working tree for independent review; all original test files are unchanged.

## Design and contracts

- One input format: v2 Animation Plan `source.reference_canvas` plus inline
  `source.layers`. No external layer manifest or hidden metadata fields.
  `source.image` and `--source` retain v1 behavior; mixed modes are rejected.
- Every layer supplies a unique target, PNG, named/custom normalized anchor,
  and finite static position. `sprite` is reserved. Array order is the only
  back-to-front order. Unknown layered track/event targets fail; events remain
  annotations. Untracked layers remain visible at their static positions.
- The authoring plan owns relative image paths. Normalization rewrites every
  path relative to the build, pins each PNG's SHA-256/dimensions and includes
  all bindings, order, anchors, positions and canvases in the digest. The
  normalized plan becomes the runtime description; the original authoring
  file is not an additional runtime dependency. Moving a complete parent tree
  retains the same relative paths; moving only the build needs regeneration.
- Local transforms use reference-canvas axes, then clip to the reference
  canvas and alpha-over composite in order. One unchanged M2 `render_pose`
  applies global anchor alignment, transform and opacity to the composite.
  Local translation never enters global offset. Global opacity is applied
  once, after composition. A different output canvas does not imply fitting.
- Rotate sums; scale/opacity factors multiply; opacity clamps only after a
  finite product check. Nonpositive scale, negative opacity and non-finite
  effective geometry fail. Invisible local layers are valid; only the final
  frame must be nonempty. Very large finite local integer translations clip
  without passing overflowing integer coordinates to Pillow. Global budgets
  remain global; there is no independent local displacement budget.
- Both raster stages use the documented integer-copy or bilinear affine path,
  8-bit alpha-over, and `floor(alpha * opacity + 0.5)` opacity rounding. The
  intermediate clip and quantization are intentional.
- `frame-plan.json` v2 includes all layer bindings plus ordered local poses and
  a global pose for every frame. Full frame-plan consistency is recomputed
  from the plan. Failed input verification stops frame consumption. A valid
  built-in manifest requires exact decoded RGBA from **all** trusted sources.
  External frames retain composite geometry validation, which cannot establish
  hidden-layer state or exact artwork identity.
- Full is default; reduced `hold_first_frame` freezes the entire first-frame
  local composition and global pose. All held PNGs are byte-identical.
- M2 publication functions and recovery flow are reused. Source guards now
  include every layer and runtime description, manifest hard-link aliases,
  and plan/QA/preview output aliases. Unknown output files remain protected.

The normative coordinate, path, error and compatibility contract is
[layered-sprites.md](layered-sprites.md); transaction recovery remains in
[renderer.md](renderer.md#recovery-after-an-interrupted-process).

## Schema and version decisions

| Contract | Decision | Compatibility |
| --- | --- | --- |
| Package | 0.4.0 → 0.5.0 | pyproject and runtime version agree; verified installed distribution too |
| Animation Plan | v2 for layers, v1 retained | V1 normalization/source override behavior retained; v2 requires layered source |
| Frame plan | v2 for layered source and ordered local/global poses | V1 structure retained; version must match the plan's input mode and have canonical integer type |
| Render manifest | v1 unchanged | Existing digest + mode fully binds the layered plan; no additional fields needed |
| QA | v1 unchanged | Existing check/issue representation supports layer context |
| Frame manifest | v1 unchanged | Existing external-frame workflow preserved |

Schemas `animation-plan.schema.json` and `frame-plan.schema.json` describe both
versions and reject cross-mode fields. New errors include
`SOURCE_MODE_CONFLICT` (exit 2), `PLAN_SOURCE_VERSION_MISMATCH`, `EMPTY_LAYERS`,
`DUPLICATE_LAYER_TARGET`, `RESERVED_LAYER_TARGET`, `UNKNOWN_LAYER_TARGET`,
`INVALID_REFERENCE_CANVAS`, `INVALID_LAYER_ANCHOR`, `INVALID_LAYER_POSITION`,
`SOURCE_PNG_REQUIRED`, `NONFINITE_EFFECTIVE_TRANSFORM` (exit 1).
Existing source/transform/frame/pixel/transaction errors are reused.

V1 output pixels and normalization were not changed. Invalid non-finite
compositions gain explicit rejection. Historical provenance strings still
produce only `GENERATED_BY_MISMATCH`. No test assertions were migrated,
removed, skipped or weakened to obtain compatibility.

## Verification actually executed

Environment: macOS, Python 3.14.5, Pillow 12.3.0, PyYAML 6.0.3, pytest 9.1.1.

```text
Baseline: .venv/bin/pytest                         229 passed
Final: .venv/bin/pytest -o addopts='' -q            381 passed in 2.61s
.venv/bin/python -m compileall -q src/sprite_harness tests scripts    exit 0
.venv/bin/pip install --no-deps --no-build-isolation .               exit 0, 0.5.0 wheel installed
.venv/bin/pip check                                                exit 0, no broken requirements
git diff --check                                                  exit 0
Installed CLI --version                                           0.5.0
Installed importlib.metadata version                              0.5.0
Installed module location                                         .venv/lib/python3.14/site-packages/sprite_harness
```

381 = 229 unchanged original tests + 123 new layer/contract/pixel/safety tests
+ all 29 original M2 safety scenarios rerun unchanged with two-layer inputs.
Independent oracles hand-compute placement, combined local/global rotation and
translation, bilinear scale support, opacity products, alpha-over order and
post-composite global opacity. Tests cover every-source replacement and resize,
round-trip and relocation, strict shapes/versions, tampering, transparent /
occluded / clipped layers, numeric overflow/underflow, same-bbox corruption,
full/hold modes, source hashes, re-encoding compatibility and external frames.
The shared safety scenarios include every publication rename, staging failure,
rollback/cleanup failure, forced subprocess exit, concurrent readers/writers,
symlinks, hard links and rebuilding damaged outputs.

Final real installed-CLI acceptance: **54 subprocess calls, all expected exits
matched**. Every harness command ran in a temporary cwd outside the repository
with `PYTHONPATH` removed. Both module and distribution identities were checked
before running; no pytest `pythonpath=src` fallback was used. All JSON outputs
and artifacts passed a parser rejecting NaN/Infinity; success and failures
covered process exits 0/1/2/3/4. Plan/render/validate/preview/contact-sheet/report
were exercised in JSON and human modes. Each pipeline produced 12 distinct full
frames, repeated renders matched bytes, and the reduced build held frame 0
across 12 identical PNGs. Same-bbox RGB corruption failed, overwrite repaired
it, the last source layer's resize/replacement failed, and all source hashes
were restored/unchanged after the deliberate probes. The layered contact sheet
was visually inspected; it shows only the intended simple geometric shapes.

Local environment repair: the existing 0.4.0 dist-info directory contained only
orphan duplicate files and no METADATA. It made pip's first success label say
0.4.0 and metadata discovery return None despite loading 0.5.0 code. The directory
was **moved intact**, not deleted, to
`build/m3-install-recovery/sprite_animation_harness-0.4.0.dist-info`. A subsequent
regular reinstall reports 0.5.0 consistently. Pip's cache-permission warning is
benign; installation and `pip check` succeeded without cache or network use.

## Reproduction and artifacts

From the repository root:

```bash
.venv/bin/pip install --no-deps --no-build-isolation .
# Choose a fresh output directory; the acceptance script never replaces one.
.venv/bin/python scripts/acceptance_m3.py --output build/m3-review-acceptance
```

The full recorded final run is under `build/m3-acceptance-final/` (ignored build
output, retained locally):

- `summary.json`: installed identity, 54 calls, checked exits, source hashes and results.
- `commands.json`: full command arguments, outside cwd, expected/actual exits, stdout/stderr.
- `layered/build/`: full three-layer plan, frame plan, render manifest, 12 PNGs,
  `preview.gif`, `contact-sheet.png`, plan/frame QA.
- `layered/build-hold/`: corresponding reduced build and previews/QA.
- `single/build/` and `single/build-hold/`: old M2 example with generated placeholder.
- `layered/build-repeat/` and `single/build-repeat/`: deterministic comparison builds.

A minimal layered demonstration with a fresh directory:

```bash
.venv/bin/python scripts/create_layered_placeholder.py /tmp/sprite-m3-demo
.venv/bin/sprite-harness plan --spec /tmp/sprite-m3-demo/animation.json --output /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness render /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness validate /tmp/sprite-m3-demo/build --write-qa
.venv/bin/sprite-harness preview /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness contact-sheet /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness report /tmp/sprite-m3-demo/build
```

## Changed files for review

- Protocol/docs: `HARNESS.md`, `README.md`, `docs/roadmap.md`,
  `docs/architecture.md`, `docs/animation-plan.md`, `docs/renderer.md`,
  `docs/handoff.md`, new `docs/layered-sprites.md`.
- Version/contracts: `pyproject.toml`, `src/sprite_harness/__init__.py`,
  `schemas/animation-plan.schema.json`, `schemas/frame-plan.schema.json`.
- Core: `src/sprite_harness/plan.py`, `plan_validator.py`, `expand.py`,
  `geometry.py`, new `layers.py`, `build.py`, `render.py`, `processing.py`, `cli.py`.
- Tests: new `tests/test_layers.py`, `tests/test_layered_safety.py`.
- Example/tools: new `examples/layered-placeholder/animation.json`,
  `examples/layered-placeholder/README.md`, `scripts/create_layered_placeholder.py`,
  `scripts/acceptance_m3.py`.

## Limits and next work

No known unresolved M3 functional failures remain after the recorded gates.
Exact pixel validation requires the same Pillow rendering environment;
legitimate cross-version resampling changes require re-rendering. External
flattened frames cannot prove occluded layers. Transactions detect interrupted
processes and recover ordinary publication failures; they do not promise
power-loss durability or protection from hostile filesystem replacement races.
Source files should not be edited concurrently with rendering. Derived preview
and QA files remain snapshots and should be regenerated after changing mode.
There are no independent local motion budgets or resource-size quotas.

The input is explicitly authored layers, not automatically extracted body
parts. Events do not synthesize actions. M4 and M5 remain separate future work.


## 2026-09-16 slouch palette rework 2 (consumer assets only)

Inspected live gensokyo-codex-pets pose_prop: intake READY, geometry failed four
palette checks. Repaired head and three arm/hand palettes plus closed-eye cover
discs, preserving original snapshots, limb alpha, configs and existing timing.
No Harness core edits in this task. Consumer's five PNGs and HANDOFF.md updated.
Public 0.8.0 CLI builds 35 frames with no warnings; exact exclusive-eye composite
comparison passes, reduced-motion holds frame 0. Consumer repository gate passes.
Agent inspected 596/160px side-by-side output; user visual approval remains pending.
Full outputs, scripts, backup and preview: build/slouch-rework-2/REPORT.md.
No app install, runtime publication, commit or push. Existing dirty work preserved.


## 2026-09-17 双手托腮视觉稿已认可，最小眨眼试验完成

用户选择其双手托腮/圆桌/榻榻米概念的左侧方案，接受后续小幅气质调整稿，
并授权试用Harness。旧单手返工2/3/4均不作为新视觉基准。

隔离结果：build/slouch-double-cheek-prototype/README.md。三层仅为完整静态
场景与睁闭眼面板，不是独立头部/手臂骨架。公共0.8.0渲染140帧/20fps/7秒，
闭眼128–132帧共250ms。正常和减弱动态均无错误/警告，逐帧对比确认眼部外RGBA
不变、alpha恒定、减弱动态恒等首帧；已查看160/320px深浅底。

原稿不变，闭眼由ImageGen编辑，限定人工眼部面板内；静态原稿做外部背景透明化
和等比缩放。未改Harness核心或consumer契约，未替换旧共享桌面，未安装/发布。
尚待用户判断眨眼观感；独立身体图层、生产支撑线和App摆放仍未完成。


## 2026-09-17 原生独立托腮预览接入

用户认可最小眨眼后要求“开始做”。已在consumer注册可选double_cheek素材
并增加手动14秒预览入口；仅preview构建能打入新包，未加入自主池。
记录：build/slouch-native-integration/README.md；App双手托腮预览.app已启动。
行为108项/原生31项/consumer仓库检查通过；严格签名通过；源原件和窄补丁保留。
整场景以榻榻米y568/596为支撑、scale0.86、x0.07，修掉膝下对齐造成的裁剪。
用户后续已确认原生效果；正式接入结果见下节。完整独立肢体图层仍未做，正式应用未替换，无commit/push。


## 2026-09-17 双手托腮正式接入完成，安装待用户确认

本条优先于下方历史记录。用户已认可静态稿、眨眼和原生大小/摆放，最后反馈“效果可以”；
原生视觉不再待确认。保持 scale 0.86、xFraction 0.07、supportEdge 568/596，未重新生成脸或调整比例。

- 正式源码允许 `build.py --slouch PACKAGE` 在非 preview 模式打包；版本 1.9 / build 11。
- 自动托腮仅在观测到 idle、连续无互动/其他动作至少180秒、素材验证通过、未暂停/减少动态/睡眠、未拖动或打开菜单时参与调度。
  每次30–45秒调度抽样占5%；原吃饭总权重25%不变，所有动作都可选时70%不动。
  托腮持续14秒（两轮7秒），自然结束/被抢占后单动作冷却900秒，动作池休息180秒；冷却只保存在本次进程。
- 喂食、点击、拖动、失败及离开idle会抢占自动托腮。暂停、减少动态及无效资源会取消自动动作；恢复后重新等待，不补播。
  手动预览与自动episode显式区分，原preview专用手动入口保留；正式版采用自动触发。
- 原始静态全场景+睁闭眼局部面板不变。596×596、140帧/20fps，闭眼128–132；未制作独立头部/手臂/袖子动作。
- 验证：131项行为测试、32项原生自检通过；consumer仓库检查通过；Harness full/reduced均0错误/0警告。
  新包与认可预览的PNG/source.json摘要相同；140帧与Harness逐像素相等；160/596px原生截图与认可预览逐像素相等。
  严格codesign通过。原生运行后Finder元数据曾使签名检查失败，仅清理新构建app的扩展元数据后复验通过。
- 可安装产物：`/Users/lyuyuwei/Documents/ChatGPT/Spirite harness/build/slouch-production-integration/灵梦桌宠.app`。
  同目录 README.md、receipt.json、integration.patch、before/、behavior-tests.txt、repository-check.txt、qa/ 为证据与窄回退资料。
- 已安装 `/Users/lyuyuwei/Applications/灵梦桌宠.app` 仍为1.8/build10，未替换；用户要求替换前再次确认。
  下一步仅在用户确认后备份现安装包并替换，验证安装后的签名/资源/启动；本轮没有正式日常运行观察或安装后验收。
- fetch后consumer HEAD与origin/main同为eeb42236b18e534ac8befd5f71561feed6cd5484。
  两仓库原有混合修改保留；本轮未reset/clean/commit/push。不要重跑旧edit.py或应用旧integration.patch。

## 2026-09-17 sleep_table 眼口间距修订

用户认为静态v1嘴巴与眼睛太近。已生成v2：上移闭眼线，增加眼口间距，保留伏桌方向。
候选位于 `build/sleep-table-static-v2/candidate.png`，等待视觉反馈。首次仅下移嘴巴的生成变化不明显，未采纳。
原图及正式App不变；不声称生成图其他区域逐像素锁定，未接动画。

## 2026-09-17 用户选回睡姿首轮微调版

用户附exec-63c4aa0e-666e-493d-b73c-7fa8bb74a33d.png并说“那还是这一版好一点”。
该图已逐字节保存为Harness `build/sleep-table-selected-v1/selected.png`，选择与摘要见selection.json。
此选择覆盖此前“首轮未采纳”的判断；上移眼睛的sleep-table-static-v2不采用。保留选定图的眼口位置。
静态姿态基准已选定，动画/原生摆放仍未验收，正式App未改，无commit/push。


## 2026-09-20 Tier4 静态底稿准备

已固定现有拉面＋饺子底稿，普通/减少动态模式均通过公共 Harness 流程，
逐像素与原稿相等，160px 可读且无裁切。当前仍为单帧，未制作吃面动态。
产物：`build/reimu-tier4-intake-20260920/`；记录：
`docs/decisions/2026-09-20-reimu-tier4-static-intake.md`。
本轮静态候选待用户反馈，下一步范围待选择；未接原生 Tier4、未安装或发布。
