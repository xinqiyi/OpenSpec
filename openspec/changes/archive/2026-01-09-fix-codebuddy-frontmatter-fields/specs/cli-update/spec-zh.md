## 修改后的需求

### 需求：斜杠命令更新

update 命令应刷新已配置工具的现有斜杠命令文件而不创建新文件，并确保 OpenCode 归档命令接受变更 ID 参数。

#### 场景：更新 Antigravity 的斜杠命令
- **当** `.agent/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **那么** 刷新每个文件中 OpenSpec 管理的部分，使工作流副本与其他工具一致，同时保留现有的单字段 `description` frontmatter
- **并且** 在更新期间跳过创建任何缺失的工作流文件，模仿 Windsurf 和其他 IDE 的行为

#### 场景：更新 Claude Code 的斜杠命令
- **当** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **那么** 使用共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 CodeBuddy Code 的斜杠命令
- **当** `.codebuddy/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **那么** 使用包含 `description` 和 `argument-hint` 字段的 YAML frontmatter 的共享 CodeBuddy 模板刷新每个文件
- **并且** 对 `argument-hint` 参数使用方括号格式（例如 `[change-id]`）
- **并且** 保留 OpenSpec 管理标记之外的任何用户自定义

#### 场景：更新 Cline 的斜杠命令
- **当** `.clinerules/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **那么** 使用共享模板刷新每个文件
- **并且** 包含 Cline 特定的 Markdown 标题 frontmatter
- **并且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 Crush 的斜杠命令
- **当** `.crush/commands/` 包含 `openspec/proposal.md`、`openspec/apply.md` 和 `openspec/archive.md`
- **那么** 使用共享模板刷新每个文件
- **并且** 包含 Crush 特定的 frontmatter，包含 OpenSpec 类别和标签
- **并且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 Cursor 的斜杠命令
- **当** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **那么** 使用共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 Factory Droid 的斜杠命令
- **当** `.factory/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **那么** 使用包含 `description` 和 `argument-hint` 字段的 YAML frontmatter 的共享 Factory 模板刷新每个文件
- **并且** 确保模板主体保留 `$ARGUMENTS` 占位符，以便用户输入继续流入 droid
- **并且** 仅更新 OpenSpec 管理标记内的内容，保持任何非管理注释不变
- **并且** 在更新期间跳过创建缺失文件

#### 场景：更新 OpenCode 的斜杠命令
- **当** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **那么** 使用共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明
- **并且** 确保归档命令在前置元数据中包含 `$ARGUMENTS` 占位符以接受变更 ID 参数

#### 场景：更新 Windsurf 的斜杠命令
- **当** `.windsurf/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **那么** 使用共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明
