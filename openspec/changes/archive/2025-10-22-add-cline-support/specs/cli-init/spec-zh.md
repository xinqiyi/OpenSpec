## 已修改的需求

### 需求：AI 工具配置详情

命令应使用标记系统，使用 OpenSpec 特定指令正确配置所选 AI 工具。

#### 场景：配置 Claude Code

- **当** 选择了 Claude Code
- **则** 在项目根目录（不在 openspec/ 内）创建或更新 `CLAUDE.md`
- **并且** 使用指向 `@/openspec/AGENTS.md` 的简短桩代码填充受管块

#### 场景：配置 CodeBuddy Code

- **当** 选择了 CodeBuddy Code
- **则** 在项目根目录（不在 openspec/ 内）创建或更新 `CODEBUDDY.md`
- **并且** 使用指向 `@/openspec/AGENTS.md` 的简短桩代码填充受管块

#### 场景：配置 Cline

- **当** 选择了 Cline
- **则** 在项目根目录（不在 openspec/ 内）创建或更新 `CLINE.md`
- **并且** 使用指向 `@/openspec/AGENTS.md` 的简短桩代码填充受管块

#### 场景：创建新的 CLAUDE.md

- **当** CLAUDE.md 不存在时
- **则** 创建新文件，包含包裹在标记中的桩代码指令，使完整工作流保持在 `openspec/AGENTS.md` 中：
```markdown
<!-- OPENSPEC:START -->
# OpenSpec 指令

本项目使用 OpenSpec 管理 AI 助手工作流。

- 完整指南位于 '@/openspec/AGENTS.md'。
- 保留此受管块，以便 'openspec update' 可以刷新指令。
<!-- OPENSPEC:END -->
```

### 需求：斜杠命令配置

init 命令应使用共享模板为支持的编辑器生成斜杠命令文件。

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
- **则** 创建 `.clinerules/openspec-proposal.md`、`.clinerules/openspec-apply.md` 和 `.clinerules/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 包含 Cline 特定的 Markdown 标题 frontmatter
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Cursor 生成斜杠命令
- **当** 用户在初始化期间选择 Cursor
- **则** 创建 `.cursor/commands/openspec-proposal.md`、`.cursor/commands/openspec-apply.md` 和 `.cursor/commands/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 OpenCode 生成斜杠命令
- **当** 用户在初始化期间选择 OpenCode
- **则** 创建 `.opencode/commands/openspec-proposal.md`、`.opencode/commands/openspec-apply.md` 和 `.opencode/commands/openspec-archive.md`
- **并且** 从共享模板填充每个文件，使命令文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Windsurf 生成斜杠命令
- **当** 用户在初始化期间选择 Windsurf
- **则** 创建 `.windsurf/workflows/openspec-proposal.md`、`.windsurf/workflows/openspec-apply.md` 和 `.windsurf/workflows/openspec-archive.md`
- **并且** 从共享模板填充每个文件（包裹在 OpenSpec 标记中），使工作流文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Kilo Code 生成斜杠命令
- **当** 用户在初始化期间选择 Kilo Code
- **则** 创建 `.kilocode/workflows/openspec-proposal.md`、`.kilocode/workflows/openspec-apply.md` 和 `.kilocode/workflows/openspec-archive.md`
- **并且** 从共享模板填充每个文件（包裹在 OpenSpec 标记中），使工作流文本与其他工具匹配
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令

#### 场景：为 Codex 生成斜杠命令
- **当** 用户在初始化期间选择 Codex
- **则** 在 `~/.codex/prompts/openspec-proposal.md`、`~/.codex/prompts/openspec-apply.md` 和 `~/.codex/prompts/openspec-archive.md` 创建全局提示文件（如果设置了 `$CODEX_HOME/prompts` 则在其下）
- **并且** 从共享模板填充每个文件，将第一个编号占位符（`$1`）映射到主要用户输入（例如变更标识符或问题文本）
- **并且** 将生成的内容包裹在 OpenSpec 标记中，以便 `openspec update` 可以刷新提示而不影响周围的用户自定义注释

#### 场景：为 GitHub Copilot 生成斜杠命令
- **当** 用户在初始化期间选择 GitHub Copilot
- **则** 创建 `.github/prompts/openspec-proposal.prompt.md`、`.github/prompts/openspec-apply.prompt.md` 和 `.github/prompts/openspec-archive.prompt.md`
- **并且** 使用包含 `description` 字段（总结工作流阶段）的 YAML frontmatter 填充每个文件
- **并且** 包含 `$ARGUMENTS` 占位符以捕获用户输入
- **并且** 将共享模板主体包裹在 OpenSpec 标记中，以便 `openspec update` 可以刷新内容
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的指令
