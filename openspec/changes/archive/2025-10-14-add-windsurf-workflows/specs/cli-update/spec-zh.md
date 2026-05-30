## 修改后的需求
### 需求：斜杠命令更新
更新命令应刷新已配置工具的现有斜杠命令文件，而不创建新文件。

#### 场景：更新 Claude Code 的斜杠命令
- **WHEN** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Cursor 的斜杠命令
- **WHEN** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 OpenCode 的斜杠命令
- **WHEN** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Windsurf 的斜杠命令
- **WHEN** `.windsurf/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用包裹在 OpenSpec 标记中的共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：缺少斜杠命令文件
- **WHEN** 某个工具缺少斜杠命令文件
- **THEN** 在更新期间不创建新文件
