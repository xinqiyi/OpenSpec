# CLI Init 增量

## 已修改需求
### 需求：斜杠命令配置
init 命令应使用共享模板为受支持的编辑器生成斜杠命令文件。

#### 场景：为 Antigravity 生成斜杠命令
- **当** 用户在初始化期间选择 Antigravity
- **则** 创建 `.agent/workflows/openspec-proposal.md`、`.agent/workflows/openspec-apply.md` 和 `.agent/workflows/openspec-archive.md`
- **并且** 确保每个文件以仅包含 `description: <stage summary>` 字段的 YAML frontmatter 开头，后跟包裹在托管标记中的共享 OpenSpec 工作流指令
- **并且** 使用与其他工具相同的提案/应用/归档指南填充工作流正文，使 Antigravity 的行为类似于 Windsurf，同时指向 `.agent/workflows/` 目录

#### 场景：为 Claude Code 生成斜杠命令
- **当** 用户在初始化期间选择 Claude Code
- **则** 创建 `.claude/commands/openspec/proposal.md`、`.claude/commands/openspec/apply.md` 和 `.claude/commands/openspec/archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 CodeBuddy Code 生成斜杠命令
- **当** 用户在初始化期间选择 CodeBuddy Code
- **则** 创建 `.codebuddy/commands/openspec/proposal.md`、`.codebuddy/commands/openspec/apply.md` 和 `.codebuddy/commands/openspec/archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Cline 生成斜杠命令
- **当** 用户在初始化期间选择 Cline
- **则** 创建 `.clinerules/workflows/openspec-proposal.md`、`.clinerules/workflows/openspec-apply.md` 和 `.clinerules/workflows/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 包含 Cline 特定的 Markdown 标题 frontmatter
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Crush 生成斜杠命令
- **当** 用户在初始化期间选择 Crush
- **则** 创建 `.crush/commands/openspec/proposal.md`、`.crush/commands/openspec/apply.md` 和 `.crush/commands/openspec/archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 包含 Crush 特定的 frontmatter，包含 OpenSpec 类别和标签
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Cursor 生成斜杠命令
- **当** 用户在初始化期间选择 Cursor
- **则** 创建 `.cursor/commands/openspec-proposal.md`、`.cursor/commands/openspec-apply.md` 和 `.cursor/commands/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Factory Droid 生成斜杠命令
- **当** 用户在初始化期间选择 Factory Droid
- **则** 创建 `.factory/commands/openspec-proposal.md`、`.factory/commands/openspec-apply.md` 和 `.factory/commands/openspec-archive.md`
- **并且** 从包含 Factory 兼容的 YAML frontmatter（包含 `description` 和 `argument-hint` 字段）的共享模板填充每个文件
- **并且** 在模板正文中包含 `$ARGUMENTS` 占位符，以便 droid 接收任何用户提供的输入
- **并且** 将生成的内容包裹在 OpenSpec 托管标记中，以便 `openspec update` 可以安全地刷新命令

#### 场景：为 OpenCode 生成斜杠命令
- **当** 用户在初始化期间选择 OpenCode
- **则** 创建 `.opencode/commands/openspec-proposal.md`、`.opencode/commands/openspec-apply.md` 和 `.opencode/commands/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Windsurf 生成斜杠命令
- **当** 用户在初始化期间选择 Windsurf
- **则** 创建 `.windsurf/workflows/openspec-proposal.md`、`.windsurf/workflows/openspec-apply.md` 和 `.windsurf/workflows/openspec-archive.md`
- **并且** 从共享模板（包裹在 OpenSpec 标记中）填充每个文件，使工作流文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Kilo Code 生成斜杠命令
- **当** 用户在初始化期间选择 Kilo Code
- **则** 创建 `.kilocode/workflows/openspec-proposal.md`、`.kilocode/workflows/openspec-apply.md` 和 `.kilocode/workflows/openspec-archive.md`
- **并且** 从共享模板（包裹在 OpenSpec 标记中）填充每个文件，使工作流文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Codex 生成斜杠命令
- **当** 用户在初始化期间选择 Codex
- **则** 在 `~/.codex/prompts/openspec-proposal.md`、`~/.codex/prompts/openspec-apply.md` 和 `~/.codex/prompts/openspec-archive.md`（或设置了 `$CODEX_HOME/prompts` 时在其下）创建全局提示文件
- **并且** 从将第一个编号占位符（`$1`）映射到主要用户输入（例如变更标识符或问题文本）的共享模板填充每个文件
- **并且** 将生成的内容包裹在 OpenSpec 标记中，以便 `openspec update` 可以刷新提示而不影响周围的自定义注释

#### 场景：为 GitHub Copilot 生成斜杠命令
- **当** 用户在初始化期间选择 GitHub Copilot
- **则** 创建 `.github/prompts/openspec-proposal.prompt.md`、`.github/prompts/openspec-apply.prompt.md` 和 `.github/prompts/openspec-archive.prompt.md`
- **并且** 使用包含 `description` 字段的 YAML frontmatter 填充每个文件，该字段概述工作流阶段
- **并且** 包含 `$ARGUMENTS` 占位符以捕获用户输入
- **并且** 将共享模板正文包裹在 OpenSpec 标记中，以便 `openspec update` 可以刷新内容
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Gemini CLI 生成斜杠命令
- **当** 用户在初始化期间选择 Gemini CLI
- **则** 创建 `.gemini/commands/openspec/proposal.toml`、`.gemini/commands/openspec/apply.toml` 和 `.gemini/commands/openspec/archive.toml`
- **并且** 每个文件填充为 TOML，设置阶段特定的 `description = "<summary>"` 和包含共享 OpenSpec 模板的多行 `prompt = """` 块
- **并且** 在 `prompt` 值内部包裹 OpenSpec 托管标记（`<!-- OPENSPEC:START -->` / `<!-- OPENSPEC:END -->`），以便 `openspec update` 可以安全地刷新标记之间的正文而不影响 TOML 框架
- **并且** 确保斜杠命令副本与现有其他工具使用的提案/应用/归档模板匹配

#### 场景：为 iFlow CLI 生成斜杠命令
- **当** 用户在初始化期间选择 iFlow CLI
- **则** 创建 `.iflow/commands/openspec-proposal.md`、`.iflow/commands/openspec-apply.md` 和 `.iflow/commands/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 为每个命令包含带有 `name`、`id`、`category` 和 `description` 字段的 YAML frontmatter
- **并且** 将生成的内容包裹在 OpenSpec 托管标记中，以便 `openspec update` 可以安全地刷新命令
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 RooCode 生成斜杠命令
- **当** 用户在初始化期间选择 RooCode
- **则** 创建 `.roo/commands/openspec-proposal.md`、`.roo/commands/openspec-apply.md` 和 `.roo/commands/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 包含简单的 Markdown 标题（例如 `# OpenSpec: Proposal`），不包含 YAML frontmatter
- **并且** 在适用时将生成的内容包裹在 OpenSpec 托管标记中，以便 `openspec update` 可以安全地刷新命令
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令
