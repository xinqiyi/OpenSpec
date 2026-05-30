# 为 Init/Update 添加 AGENTS.md Standard 支持

## 摘要
- 让 `openspec init` 使用与 `CLAUDE.md` 相同的标记系统管理根级别的 `AGENTS.md` 文件。
- 允许 `openspec update` 刷新或搭建根 `AGENTS.md`，使 AGENTS 兼容工具始终接收当前指令。
- 保持现有的 `openspec/AGENTS.md` template 作为 spec 来源，同时确保读取 `AGENTS.md` 选择加入指令的助手自动获取最新指导。

## 动机
README 现在将团队指向 AGENTS.md 兼容的助手，但 CLI 只管理 `CLAUDE.md`。项目必须手动创建根 `AGENTS.md` 文件才能受益于该标准，如果维护者不记得手动复制内容，更新将会漂移。扩展 `init` 和 `update` 弥补了这一差距，使 OpenSpec 真正实现一流的 AGENTS 支持承诺。

## 方案
1. 在 `openspec init` 选择流程中扩展一个"AGENTS.md standard"选项，创建或刷新包裹在 OpenSpec 标记中的根 `AGENTS.md` 文件，镜像现有的 CLAUDE 集成。
2. 生成文件时，从与 `openspec/AGENTS.md` 相同的 template 中提取受管内容，确保两个位置保持同步。
3. 更新 `openspec update`，使其始终刷新根 `AGENTS.md`（如果缺失则创建），与 `openspec/AGENTS.md` 和其他已配置的助手一起。
4. 在 CLI spec 中记录新行为，并用两个命令的测试验证标记处理（无重复，保留块外用户内容）。

## 范围外
- 添加超出共享指令块的额外 AGENTS 特定提示或 workflow。
- 一次运行中为多个标准添加非交互式标志或批量配置。
- 更广泛地重构 template 的存储或加载方式。

## 风险与缓解措施
- **风险：** 意外覆盖用户在受管块周围编辑的内容。
 - **缓解措施：** 重用与 `CLAUDE.md` 共享的现有标记更新辅助函数，并添加覆盖在块前后包含自定义文本的文件的测试。
- **风险：** `openspec/AGENTS.md` 和根文件之间的分歧。
 - **缓解措施：** 从 spec template 中提取根文件内容，而不是内联复制字符串。
- **风险：** 对文件创建时间的混淆。
 - **缓解措施：** 记录创建与更新，并确保帮助文本在 `init` 期间引用 AGENTS 选项。
