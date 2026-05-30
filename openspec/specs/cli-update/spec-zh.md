# Update 命令 spec

## 目的

作为使用 OpenSpec 的开发者，我希望在新版本发布时更新项目中的 OpenSpec 指令，以便受益于 AI agent 指令的改进。

## 需求
### 需求：更新行为
update 命令应以团队友好的方式将 OpenSpec 指令文件更新为最新 template。

#### 场景：运行 update 命令
- **WHEN** 用户运行 `openspec update` 时
- **THEN** 用最新 template 替换 `openspec/AGENTS.md`
- **AND** 如果根级别的存根文件（`AGENTS.md`/`CLAUDE.md`）存在，刷新它以使其指向 `@/openspec/AGENTS.md`

### 需求：前置条件

该命令需要在允许更新前存在现有的 OpenSpec 结构。

#### 场景：检查前置条件

- **GIVEN** 该命令需要现有的 `openspec` 目录（由 `openspec init` 创建）
- **WHEN** `openspec` 目录不存在时
- **THEN** 显示错误："未找到 OpenSpec 目录。请先运行 'openspec init'。"
- **AND** 以代码 1 退出

### 需求：文件处理
update 命令应以可预测和安全的方式处理文件更新。

#### 场景：更新文件
- **WHEN** 更新文件时
- **THEN** 用最新 template 完全替换 `openspec/AGENTS.md`
- **AND** 如果根级别的存根存在，更新托管块内容，使其继续将团队成员指向 `@/openspec/AGENTS.md`

### 需求：工具无关的更新
update 命令应以可预测的方式刷新 OpenSpec 管理的文件，同时尊重每个团队选择的工具。

#### 场景：更新文件
- **WHEN** 更新文件时
- **THEN** 用最新 template 完全替换 `openspec/AGENTS.md`
- **AND** 使用托管标记块创建或刷新根级别的 `AGENTS.md` 存根，即使该文件之前不存在
- **AND** 仅更新现有 AI 工具文件中 OpenSpec 管理的部分，保留用户编写的内容不变
- **AND** 避免创建新的原生工具配置文件（斜杠命令、CLAUDE.md 等），除非它们已存在

### 需求：始终更新核心文件
update 命令应始终更新核心 OpenSpec 文件并显示 ASCII 安全成功消息。

#### 场景：成功更新
- **WHEN** 更新成功完成时
- **THEN** 用最新 template 替换 `openspec/AGENTS.md`
- **AND** 如果根级别的存根存在，刷新它使其仍将贡献者指向 `@/openspec/AGENTS.md`

### 需求：斜杠命令更新

update 命令应刷新已配置工具的现有斜杠命令文件，而不创建新文件，并确保 OpenCode archive 命令接受变更 ID 参数。

#### 场景：更新 Antigravity 的斜杠命令
- **WHEN** `.agent/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 刷新每个文件的 OpenSpec 管理部分，使 workflow 副本与其他工具匹配，同时保留现有的单字段 `description` frontmatter
- **AND** 在更新期间跳过创建任何缺失的 workflow 文件，与 Windsurf 和其他 IDE 的行为一致

#### 场景：更新 Claude Code 的斜杠命令
- **WHEN** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 CodeBuddy Code 的斜杠命令
- **WHEN** `.codebuddy/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md` 时
- **THEN** 使用共享的 CodeBuddy template 刷新每个文件，这些 template 包含 `description` 和 `argument-hint` 字段的 YAML frontmatter
- **AND** 对 `argument-hint` 参数使用方括号格式（例如 `[change-id]`）
- **AND** 保留 OpenSpec 管理的标记外部的用户自定义内容

#### 场景：更新 Cline 的斜杠命令
- **WHEN** `.clinerules/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 包含 Cline 特定的 Markdown 标题 frontmatter
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Continue 的斜杠命令
- **WHEN** `.continue/prompts/` 包含 `openspec-proposal.prompt`、`openspec-apply.prompt` 和 `openspec-archive.prompt` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Crush 的斜杠命令
- **WHEN** `.crush/commands/` 包含 `openspec/proposal.md`、`openspec/apply.md` 和 `openspec/archive.md` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 包含 Crush 特定的 frontmatter，带有 OpenSpec 分类和标签
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Cursor 的斜杠命令
- **WHEN** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Factory Droid 的斜杠命令
- **WHEN** `.factory/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用共享的 Factory template 刷新每个文件，这些 template 包含 `description` 和 `argument-hint` 字段的 YAML frontmatter
- **AND** 确保 template 主体保留 `$ARGUMENTS` 占位符，以便用户输入继续流入 droid
- **AND** 仅更新 OpenSpec 管理的标记内的内容，保留任何非管理性质的注释不变
- **AND** 在更新期间跳过创建缺失文件

#### 场景：更新 OpenCode 的斜杠命令
- **WHEN** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令
- **AND** 确保 archive 命令在 frontmatter 中包含 `$ARGUMENTS` 占位符，用于接受变更 ID 参数

#### 场景：更新 Windsurf 的斜杠命令
- **WHEN** `.windsurf/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用包装在 OpenSpec 标记中的共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令
- **AND** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Kilo Code 的斜杠命令
- **WHEN** `.kilocode/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用包装在 OpenSpec 标记中的共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令
- **AND** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Codex 的斜杠命令
- **GIVEN** 全局 Codex 提示目录包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **WHEN** 用户运行 `openspec update` 时
- **THEN** 使用共享的斜杠命令 template 刷新每个文件（包括占位符指南）
- **AND** 保留 OpenSpec 标记块外部的任何非托管内容
- **AND** 当 Codex 提示文件缺失时跳过创建

#### 场景：更新 GitHub Copilot 的斜杠命令
- **WHEN** `.github/prompts/` 包含 `openspec-proposal.prompt.md`、`openspec-apply.prompt.md` 和 `openspec-archive.prompt.md` 时
- **THEN** 使用共享 template 刷新每个文件，同时保留 YAML frontmatter
- **AND** 仅更新标记之间的 OpenSpec 管理块
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Gemini CLI 的斜杠命令
- **WHEN** `.gemini/commands/openspec/` 包含 `proposal.toml`、`apply.toml` 和 `archive.toml` 时
- **THEN** 使用共享的 proposal/apply/archive template 刷新每个文件的主体
- **AND** 仅替换 `prompt = """` 块中 `<!-- OPENSPEC:START -->` 和 `<!-- OPENSPEC:END -->` 标记之间的内容，以便 TOML 框架（`description`、`prompt`）保持不变
- **AND** 在更新期间跳过创建任何缺失的 `.toml` 文件；仅刷新已存在的 Gemini 命令

#### 场景：更新 iFlow CLI 的斜杠命令
- **WHEN** `.iflow/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 保留带有 `name`、`id`、`category` 和 `description` 字段的 YAML frontmatter
- **AND** 仅更新标记之间的 OpenSpec 管理块
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：缺少斜杠命令文件
- **WHEN** 工具缺少斜杠命令文件时
- **THEN** 在更新期间不创建新文件

### 需求：archive 命令参数支持
archive 斜杠命令 template 应支持对于支持 `$ARGUMENTS` 占位符的工具的可选变更 ID 参数。

#### 场景：带变更 ID 参数的 archive 命令
- **WHEN** 用户使用变更 ID 调用 `/openspec:archive <change-id>` 时
- **THEN**template 应指示 AI 针对 `openspec list` 验证提供的变更 ID
- **AND** 如果验证通过，使用提供的变更 ID 进行 archive
- **AND** 如果提供的变更 ID 不匹配可 archive 的变更，则快速失败

#### 场景：不带参数的 archive 命令（向后兼容）
- **WHEN** 用户调用 `/openspec:archive` 而未提供变更 ID 时
- **THEN**template 应指示 AI 从上下文或通过运行 `openspec list` 识别变更 ID
- **AND** 继续现有行为（保持向后兼容性）

#### 场景：OpenCode archive template 生成
- **WHEN** 生成 OpenCode archive 斜杠命令文件时
- **THEN** 在 frontmatter 中包含 `$ARGUMENTS` 占位符
- **AND** 将其包装在清晰的结构中，如 `<ChangeId>\n $ARGUMENTS\n</ChangeId>` 以指示预期的参数
- **AND** 在 template 主体中包含验证步骤，以检查变更 ID 是否有效

### 需求：从 workspace planning 主页重定向 repository 更新
repository 本地的 `openspec update` 命令不应将 workspace planning 主页静默视为 repository 本地的 OpenSpec 项目。

#### 场景：从 workspace 根目录运行更新
- **GIVEN** 命令从 OpenSpec workspace 根目录运行
- **WHEN** 用户运行 `openspec update` 时
- **THEN**OpenSpec 不应在 workspace 根目录生成 repository 本地项目文件
- **AND** 应告诉用户运行 `openspec workspace update`

#### 场景：从 workspace planning 目录内部运行更新
- **GIVEN** 命令从 OpenSpec workspace planning 主页的子目录运行
- **WHEN** 用户运行 `openspec update` 时
- **THEN**OpenSpec 不应运行 repository 本地更新行为
- **AND** 应告诉用户运行 `openspec workspace update`

#### 场景：从 repository 本地项目运行更新
- **GIVEN** 命令从 repository 本地的 OpenSpec 项目内部运行
- **WHEN** 用户运行 `openspec update` 时
- **THEN**OpenSpec 应保留现有的 repository 本地更新行为

## 边界情况

### 错误处理

该命令应优雅地处理边界情况。

#### 场景：文件权限错误

- **WHEN** 文件写入失败时
- **THEN** 让错误自然冒泡，附带文件路径

#### 场景：缺少 AI 工具文件

- **WHEN**AI 工具配置文件不存在时
- **THEN** 跳过更新该文件
- **AND** 不创建它

#### 场景：自定义目录名称

- **WHEN** 考虑自定义目录名称时
- **THEN** 此变更不支持
- **AND** 应使用默认目录名称 `openspec`

## 成功标准

用户应能够：
- 通过单个命令更新 OpenSpec 指令
- 获取最新的 AI agent 指令
- 看到清晰的更新确认

更新过程应：
- 简单快速（无需版本检查）
- 可预测（每次结果相同）
- 自包含（无需网络）
