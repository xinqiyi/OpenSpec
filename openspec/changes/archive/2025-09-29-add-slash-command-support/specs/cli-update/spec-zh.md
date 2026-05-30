## 新增需求
### 需求：斜杠命令更新
update 命令应刷新已配置工具的现有斜杠命令文件，而不创建新文件。

#### 场景：更新 Claude Code 的斜杠命令
- **当** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **则** 使用共享模板刷新每个文件
- **且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 Cursor 的斜杠命令
- **当** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **则** 使用共享模板刷新每个文件
- **且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 OpenCode 的斜杠命令
- **当** `.opencode/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **则** 使用共享模板刷新每个文件
- **且** 确保模板包含相关工作流阶段的说明

#### 场景：缺少斜杠命令文件
- **当** 工具缺少斜杠命令文件时
- **则** 在更新期间不创建新文件
