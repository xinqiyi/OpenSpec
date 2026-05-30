# 实施任务

## 1. 扩展 Init 工作流
- [x] 1.1 在 `openspec init` 工具选择提示中添加"AGENTS.md standard"选项，遵循现有 UI 约定。
- [x] 1.2 选中该选项时，使用 OpenSpec 标记生成或刷新根级别的 `AGENTS.md` 文件，内容来自规范模板。

## 2. 增强 Update 命令
- [x] 2.1 确保 `openspec update` 从最新模板写入根 `AGENTS.md`（如果缺失则创建），与 `openspec/AGENTS.md` 一起。
- [x] 2.2 更新成功消息和日志，以反映 AGENTS standard 文件的创建与刷新。

## 3. 共享模板处理
- [x] 3.1 如有必要，重构模板工具，使两个命令重用相同的内容而不重复。
- [x] 3.2 为有和没有现有 `AGENTS.md` 的项目添加自动化测试，覆盖 init/update 流程，确保标记行为正确。

## 4. 文档
- [x] 4.1 更新 CLI 规范和面向用户的文档，描述 AGENTS standard 支持。
- [x] 4.2 运行 `openspec validate add-agents-md-config --strict` 并记录任何显著的行为变化。
