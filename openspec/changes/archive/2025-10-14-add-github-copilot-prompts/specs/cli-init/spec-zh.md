## 修改后的需求

### 需求：斜杠命令配置
init 命令应使用共享模板为支持的编辑器生成斜杠命令文件。

#### 场景：为 Claude Code 生成斜杠命令
- **当** 用户在初始化过程中选择 Claude Code
- **则** 创建 `.claude/commands/openspec/proposal.md`、`.claude/commands/openspec/apply.md` 和 `.claude/commands/openspec/archive.md`
- **并且** 使用共享模板填充每个文件，使命令文本与其他工具一致
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的说明

#### 场景：为 Cursor 生成斜杠命令
- **当** 用户在初始化过程中选择 Cursor
- **则** 创建 `.cursor/commands/openspec-proposal.md`、`.cursor/commands/openspec-apply.md` 和 `.cursor/commands/openspec-archive.md`
- **并且** 使用共享模板填充每个文件，使命令文本与其他工具一致
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的说明

#### 场景：为 OpenCode 生成斜杠命令
- **当** 用户在初始化过程中选择 OpenCode
- **则** 创建 `.opencode/commands/openspec-proposal.md`、`.opencode/commands/openspec-apply.md` 和 `.opencode/commands/openspec-archive.md`
- **并且** 使用共享模板填充每个文件，使命令文本与其他工具一致
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的说明

#### 场景：为 Windsurf 生成斜杠命令
- **当** 用户在初始化过程中选择 Windsurf
- **则** 创建 `.windsurf/workflows/openspec-proposal.md`、`.windsurf/workflows/openspec-apply.md` 和 `.windsurf/workflows/openspec-archive.md`
- **并且** 使用共享模板（包裹在 OpenSpec 标记中）填充每个文件，使工作流文本与其他工具一致
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的说明

#### 场景：为 Kilo Code 生成斜杠命令
- **当** 用户在初始化过程中选择 Kilo Code
- **则** 创建 `.kilocode/workflows/openspec-proposal.md`、`.kilocode/workflows/openspec-apply.md` 和 `.kilocode/workflows/openspec-archive.md`
- **并且** 使用共享模板（包裹在 OpenSpec 标记中）填充每个文件，使工作流文本与其他工具一致
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的说明

#### 场景：为 Codex 生成斜杠命令
- **当** 用户在初始化过程中选择 Codex
- **则** 在 `~/.codex/prompts/openspec-proposal.md`、`~/.codex/prompts/openspec-apply.md` 和 `~/.codex/prompts/openspec-archive.md` 创建全局提示文件（如果设置了 `$CODEX_HOME/prompts`，则在该目录下）
- **并且** 使用将第一个编号占位符（`$1`）映射到主要用户输入（例如，变更标识符或问题文本）的共享模板填充每个文件
- **并且** 将生成的内容包裹在 OpenSpec 标记中，以便 `openspec update` 可以刷新提示而不影响周围的自定义注释

#### 场景：为 GitHub Copilot 生成斜杠命令
- **当** 用户在初始化过程中选择 GitHub Copilot
- **则** 创建 `.github/prompts/openspec-proposal.prompt.md`、`.github/prompts/openspec-apply.prompt.md` 和 `.github/prompts/openspec-archive.prompt.md`
- **并且** 使用包含 `description` 字段（总结工作流阶段）的 YAML frontmatter 填充每个文件
- **并且** 包含 `$ARGUMENTS` 占位符以捕获用户输入
- **并且** 将共享模板主体包裹在 OpenSpec 标记中，以便 `openspec update` 可以刷新内容
- **并且** 每个模板包含相关 OpenSpec 工作流阶段的说明
