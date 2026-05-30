## 修改后的需求

### 需求：斜杠命令配置

init 命令应使用共享 template 为支持的编辑器生成斜杠命令文件。

#### 场景：为 Antigravity 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Antigravity
- **THEN** 创建 `.agent/workflows/openspec-proposal.md`、`.agent/workflows/openspec-apply.md` 和 `.agent/workflows/openspec-archive.md`
- **AND** 确保每个文件以 YAML frontmatter 开头，其中仅包含 `description: <阶段摘要>` 字段，后跟包裹在管理标记中的共享 OpenSpec workflow 指令
- **AND** 使用与其他工具相同的 proposal/apply/archive 指导填充 workflow 主体，使 Antigravity 的行为与 Windsurf 一致，同时指向 `.agent/workflows/` 目录

#### 场景：为 Claude Code 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Claude Code
- **THEN** 创建 `.claude/commands/openspec/proposal.md`、`.claude/commands/openspec/apply.md` 和 `.claude/commands/openspec/archive.md`
- **AND** 从共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 CodeBuddy Code 生成斜杠命令
- **WHEN** 用户在初始化期间选择 CodeBuddy Code
- **THEN** 创建 `.codebuddy/commands/openspec/proposal.md`、`.codebuddy/commands/openspec/apply.md` 和 `.codebuddy/commands/openspec/archive.md`
- **AND** 从共享 template 填充每个文件，其中包含 CodeBuddy 兼容的 YAML frontmatter，包含 `description` 和 `argument-hint` 字段
- **AND** 对 `argument-hint` 参数使用方括号格式（例如 `[change-id]`）
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Cline 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Cline
- **THEN** 创建 `.clinerules/workflows/openspec-proposal.md`、`.clinerules/workflows/openspec-apply.md` 和 `.clinerules/workflows/openspec-archive.md`
- **AND** 从共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 包含 Cline 特定的 Markdown 标题 frontmatter
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Crush 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Crush
- **THEN** 创建 `.crush/commands/openspec/proposal.md`、`.crush/commands/openspec/apply.md` 和 `.crush/commands/openspec/archive.md`
- **AND** 从共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 包含 Crush 特定的 frontmatter，包含 OpenSpec 类别和标签
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Cursor 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Cursor
- **THEN** 创建 `.cursor/commands/openspec-proposal.md`、`.cursor/commands/openspec-apply.md` 和 `.cursor/commands/openspec-archive.md`
- **AND** 从共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Factory Droid 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Factory Droid
- **THEN** 创建 `.factory/commands/openspec-proposal.md`、`.factory/commands/openspec-apply.md` 和 `.factory/commands/openspec-archive.md`
- **AND** 从共享 template 填充每个文件，其中包含 Factory 兼容的 YAML frontmatter，包含 `description` 和 `argument-hint` 字段
- **AND** 在 template 主体中包含 `$ARGUMENTS` 占位符，以便 droid 接收用户提供的输入
- **AND** 将生成的内容包装在 OpenSpec 管理标记中，以便 `openspec update` 可以安全地刷新命令

#### 场景：为 OpenCode 生成斜杠命令
- **WHEN** 用户在初始化期间选择 OpenCode
- **THEN** 创建 `.opencode/commands/openspec-proposal.md`、`.opencode/commands/openspec-apply.md` 和 `.opencode/commands/openspec-archive.md`
- **AND** 从共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Windsurf 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Windsurf
- **THEN** 创建 `.windsurf/workflows/openspec-proposal.md`、`.windsurf/workflows/openspec-apply.md` 和 `.windsurf/workflows/openspec-archive.md`
- **AND** 从共享 template（包裹在 OpenSpec 标记中）填充每个文件，使 workflow 文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Kilo Code 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Kilo Code
- **THEN** 创建 `.kilocode/workflows/openspec-proposal.md`、`.kilocode/workflows/openspec-apply.md` 和 `.kilocode/workflows/openspec-archive.md`
- **AND** 从共享 template（包裹在 OpenSpec 标记中）填充每个文件，使 workflow 文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Codex 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Codex
- **THEN** 在 `~/.codex/prompts/openspec-proposal.md`、`~/.codex/prompts/openspec-apply.md` 和 `~/.codex/prompts/openspec-archive.md`（或如果设置了 `$CODEX_HOME/prompts` 则在其下）创建全局提示文件
- **AND** 从共享 template 填充每个文件，将第一个编号占位符（`$1`）映射到主要用户输入（例如变更标识符或问题文本）
- **AND** 将生成的内容包装在 OpenSpec 标记中，以便 `openspec update` 可以刷新提示而不触及周围的自定义注释
