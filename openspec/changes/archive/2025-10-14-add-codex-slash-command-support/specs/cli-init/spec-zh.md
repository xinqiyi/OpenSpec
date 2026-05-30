## 修改后的需求
### 需求：AI 工具配置
命令应使用标记系统使用 OpenSpec 指令配置 AI 编码助手。
#### 场景：提示 AI 工具选择
- **WHEN** 交互式运行时
- **THEN** 使用多选菜单提示用户"您使用哪些 AI 工具？"
- **AND** 使用复选框列出每个可用的工具：
 - Claude Code（创建或刷新 CLAUDE.md 和斜杠命令）
 - Cursor（创建或刷新 `.cursor/commands/*` 斜杠命令）
 - OpenCode（创建或刷新 `.opencode/command/openspec-*.md` 斜杠命令）
 - Windsurf（创建或刷新 `.windsurf/workflows/openspec-*.md` workflow）
 - Kilo Code（创建或刷新 `.kilocode/workflows/openspec-*.md` workflow）
 - Codex（创建或刷新 `~/.codex/prompts/openspec-*.md` 全局提示）
 - AGENTS.md 标准（使用 OpenSpec 标记创建或刷新 AGENTS.md）
- **AND** 在已配置工具旁边显示"（已配置）"，使用户了解选择将刷新内容
- **AND** 将禁用的工具视为"即将推出"并保持不可选状态
- **AND** 允许在选择一个或多个工具后按 Enter 确认

### 需求：斜杠命令配置
init 命令应使用共享 template 为支持的编辑器生成斜杠命令文件。

#### 场景：为 Claude Code 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Claude Code
- **THEN** 创建 `.claude/commands/openspec/proposal.md`、`.claude/commands/openspec/apply.md` 和 `.claude/commands/openspec/archive.md`
- **AND** 从共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Cursor 生成斜杠命令
- **WHEN** 用户在初始化期间选择 Cursor
- **THEN** 创建 `.cursor/commands/openspec-proposal.md`、`.cursor/commands/openspec-apply.md` 和 `.cursor/commands/openspec-archive.md`
- **AND** 从共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 OpenCode 生成斜杠命令
- **WHEN** 用户在初始化期间选择 OpenCode
- **THEN** 创建 `.opencode/command/openspec-proposal.md`、`.opencode/command/openspec-apply.md` 和 `.opencode/command/openspec-archive.md`
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
