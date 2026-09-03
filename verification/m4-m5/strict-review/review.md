# M4 / M5 严格复查与重跑

2026-09-03。检查当前未提交工作树，未 commit / push。

复查发现并修复三类问题，新增 9 项回归测试，均先复现失败再修复。
此次故障注入只使用 pytest 临时目录，没有改动用户原始素材或已有验收产物。

| 优先级 | 已复现的问题 | 修复与回归证据 |
| --- | --- | --- |
| P1 | adapter 在固化目标位置预放指向原素材的软链接或硬链接，core 复制候选时会覆盖原素材；最终快照报错发生得太晚。 | 复制前检查完整暂存目录、拒绝预占的 harness 输出，输入文件以独占模式创建。两个别名测试检查原素材及原生成目录字节未变。 |
| P2 | generation/export 规范化期间的 spec 变化未被初始快照捕获；validate-export 首次读取配置后被修改也可能返回 valid。 | 初始身份捕获提前到首次读取之前，新增输入不得覆盖已有快照。三个故障注入案例均返回 INPUT_CHANGED，发布案例保留旧产物。 |
| P2 | adapter 多写的文件/目录可能随生成包发布；离线检查会忽略未知空目录或目录软链接。 | 暂存及离线读取均检查整个目录结构。四个回归案例拒绝异常内容，禁止发布。 |

修复位于 `src/sprite_harness/generation.py` 和 `src/sprite_harness/atlas.py`；
回归用例为 `tests/test_review_regressions.py`。

完整重跑命令：

```bash
.venv/bin/python scripts/verify_m4_m5.py \
  --output verification/m4-m5/strict-review \
  --acceptance build/m4-m5-strict-review
```

本目录已存在；复跑时将两个输出目录改为新的名称。

- pytest：594 passed in 14.44s，包含全部 381 项 M3 基线测试；12 个原测试文件保持原字节。
- compileall、core/adapter 独立安装、pip check、git diff --check 全部成功。
- 仓库外 103 次执行，其中 101 次 harness CLI，移除 PYTHONPATH；导入来自 site-packages。
- 所有预期/实际退出码匹配，覆盖 0/1/2/3/4；成功与失败 JSON 严格解析。
- 单图、三层、M4 测试 adapter 各跑 full/hold，共 6 条管线：plan → generate（仅 M4）→ render → validate → preview/contact-sheet → export → validate-export/report。
- full 各有 12 个不同帧；hold 各有 12 个字节一致帧，等于该动画 full 的 frame 0。
- 多 clip atlas 按 generated、single、layered 顺序，8×11 网格，192×208 cell；36 个使用，52 个 RGBA 零值空 cell。
- 重复离线渲染、重复导出字节一致；同 bbox 改色被拒绝；full PNG 等像素重编码仍合法。
- 四个实际 0.5.0 旧 build 再次通过验证。

已实际打开本次生成的 contact sheet 与 atlas 检查排布。蓝色头部替换出现在
0-based 帧 2、3、4、8、9，手部替换出现在 0、6；其余帧使用原始素材。
GIF、帧 PNG、contact sheet 与 atlas 在 `build/m4-m5-strict-review/`。

工程复查及离线演示通过。真实 provider 的本地 HTTP 传输测试通过，但 live
provider 验收仍未完成：没有进行付费请求或素材上传。本次预览使用程序绘制
的几何素材及测试 adapter，不代表真实 AI 画面质量验收。跨目录原子快照、
任意恶意进程的 OS 沙箱、断电持久性仍不在保证范围内。

完整命令/输出见 [gates.json](gates.json)、[cli-commands.json](cli-commands.json)，
视觉检查及原文件保留记录见 [visual-qa.json](visual-qa.json)、[preservation.json](preservation.json)。
