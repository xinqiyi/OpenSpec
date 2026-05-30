## 新增需求
### 需求：斜杠命令更新
update 命令应刷新已配置工具的现有斜杠命令文件，而不创建新文件。

#### 场景：更新 Claude Code 的斜杠命令
- **WHEN** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Cursor 的斜杠命令
- **WHEN** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 OpenCode 的斜杠命令
- **WHEN** `.opencode/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：缺少斜杠命令文件
- **WHEN** 工具缺少斜杠命令文件时
- **THEN** 在更新期间不创建新文件
