## 修改后的需求
### 需求：AI 工具配置
命令应使用标记系统为 AI 编码助手配置 OpenSpec 指令。
#### 场景：提示 AI 工具选择
- **WHEN** 以交互方式运行时
- **THEN** 使用多选菜单提示用户"您使用哪些 AI 工具？"
- **AND** 列出每个可用工具并带有复选框：
 - Claude Code（创建或刷新 CLAUDE.md 和斜杠命令）
 - Cursor（创建或刷新 `.cursor/commands/*` 斜杠命令）
 - OpenCode（创建或刷新 `.opencode/command/openspec-*.md` 斜杠命令）
 - Windsurf（创建或刷新 `.windsurf/workflows/openspec-*.md` workflow）
 - AGENTS.md standard（使用 OpenSpec 标记创建或刷新 AGENTS.md）
- **AND** 在受管文件已存在的工具旁边显示"（已配置）"，让用户了解选择将刷新内容
- **AND** 将禁用的工具视为"即将推出"并保持不可选择
- **AND** 允许在选择一个或多个工具后按 Enter 确认

### 需求：斜杠命令配置
init 命令应使用共享 template 为支持的编辑器生成斜杠命令文件。

#### 场景：为 Claude Code 生成斜杠命令
- **WHEN** 用户在初始化过程中选择 Claude Code
- **THEN** 创建 `.claude/commands/openspec/proposal.md`、`.claude/commands/openspec/apply.md` 和 `.claude/commands/openspec/archive.md`
- **AND** 使用共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Cursor 生成斜杠命令
- **WHEN** 用户在初始化过程中选择 Cursor
- **THEN** 创建 `.cursor/commands/openspec-proposal.md`、`.cursor/commands/openspec-apply.md` 和 `.cursor/commands/openspec-archive.md`
- **AND** 使用共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 OpenCode 生成斜杠命令
- **WHEN** 用户在初始化过程中选择 OpenCode
- **THEN** 创建 `.opencode/commands/openspec-proposal.md`、`.opencode/commands/openspec-apply.md` 和 `.opencode/commands/openspec-archive.md`
- **AND** 使用共享 template 填充每个文件，使命令文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明

#### 场景：为 Windsurf 生成斜杠命令
- **WHEN** 用户在初始化过程中选择 Windsurf
- **THEN** 创建 `.windsurf/workflows/openspec-proposal.md`、`.windsurf/workflows/openspec-apply.md` 和 `.windsurf/workflows/openspec-archive.md`
- **AND** 使用共享 template（包裹在 OpenSpec 标记中）填充每个文件，使 workflow 文本与其他工具一致
- **AND** 每个 template 包含相关 OpenSpec workflow 阶段的说明
