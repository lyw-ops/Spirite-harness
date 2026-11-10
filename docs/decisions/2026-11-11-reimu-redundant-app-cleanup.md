# 2026-11-11 · 清理多余的灵梦应用

用户说「然后我们可以清除多余的博丽灵梦app」，随后把后续操作交给我决定。

盘点（Spotlight 加目录搜索）找到 8 项：正式安装的 `~/Applications/灵梦桌宠.app`、指向它的符号链接 `~/Desktop/灵梦/灵梦桌宠.app`，
以及 Harness build 目录里 6 个旧的 `灵梦桌宠预览.app`（1.9、1.10、1.11、1.12 各一个，1.13 两个）。

处理：6 个预览包**移到废纸篓，没有永久删除**；清单与还原方法在 `build/reimu-app-cleanup-20261111/`（`moved.tsv` 记录原路径、废纸篓路径、内容摘要、版本、大小）。
正式安装的应用和桌面上的符号链接保留。清理后 Spotlight 只剩正式安装的一个。

预览包里的批准静帧被几份研究脚本直接读取，所以先把 1.13 批准包的 `Contents/Resources` 复制为普通文件夹
`build/reimu-preview-resources-1.13/`（逐文件相同），并把 6 个脚本里的路径改到这里。两个 1.13 预览包的资源只在
`WorkEatingTier1/README.md` 和 `WorkEatingTier1/source.json`（Tier1 的批准记录）上不同，图片完全相同；我一开始以为两者完全相同，核对后更正了快照说明。

边界：旧记录和报告里写的 `…/灵梦桌宠预览.app` 路径现在已不存在，记录本身没有改动。偏好域 `local.reimu.onigiri.preview` 没有清理。
清空废纸篓之后这 6 个包就无法从本机恢复；安装链的回退包（`build/reimu-1.NN-install-*/rollback-*.zip`）不受影响。
