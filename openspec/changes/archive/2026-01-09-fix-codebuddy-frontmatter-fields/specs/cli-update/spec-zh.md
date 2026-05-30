## 修改后的需求

### 需求：斜杠命令更新

update 命令应刷新已配置工具的现有斜杠命令文件而不创建新文件，并确保 OpenCode archive 命令接受变更 ID 参数。

#### 场景：更新 Antigravity 的斜杠命令
- **WHEN** `.agent/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 刷新每个文件中 OpenSpec 管理的部分，使 workflow 副本与其他工具一致，同时保留现有的单字段 `description` frontmatter
- **AND** 在更新期间跳过创建任何缺失的 workflow 文件，模仿 Windsurf 和其他 IDE 的行为

#### 场景：更新 Claude Code 的斜杠命令
- **WHEN** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 CodeBuddy Code 的斜杠命令
- **WHEN** `.codebuddy/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **THEN** 使用包含 `description` 和 `argument-hint` 字段的 YAML frontmatter 的共享 CodeBuddy template 刷新每个文件
- **AND** 对 `argument-hint` 参数使用方括号格式（例如 `[change-id]`）
- **AND** 保留 OpenSpec 管理标记之外的任何用户自定义

#### 场景：更新 Cline 的斜杠命令
- **WHEN** `.clinerules/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 包含 Cline 特定的 Markdown 标题 frontmatter
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Crush 的斜杠命令
- **WHEN** `.crush/commands/` 包含 `openspec/proposal.md`、`openspec/apply.md` 和 `openspec/archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 包含 Crush 特定的 frontmatter，包含 OpenSpec 类别和标签
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Cursor 的斜杠命令
- **WHEN** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Factory Droid 的斜杠命令
- **WHEN** `.factory/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用包含 `description` 和 `argument-hint` 字段的 YAML frontmatter 的共享 Factory template 刷新每个文件
- **AND** 确保 template 主体保留 `$ARGUMENTS` 占位符，以便用户输入继续流入 droid
- **AND** 仅更新 OpenSpec 管理标记内的内容，保持任何非管理注释不变
- **AND** 在更新期间跳过创建缺失文件

#### 场景：更新 OpenCode 的斜杠命令
- **WHEN** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明
- **AND** 确保 archive 命令在前置元数据中包含 `$ARGUMENTS` 占位符以接受变更 ID 参数

#### 场景：更新 Windsurf 的斜杠命令
- **WHEN** `.windsurf/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明
