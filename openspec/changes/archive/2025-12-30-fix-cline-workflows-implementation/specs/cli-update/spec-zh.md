# CLI 更新 delta

## 已修改的需求

### 需求：斜杠命令更新

update 命令应为已配置的工具刷新现有斜杠命令文件而不创建新文件，并确保 OpenCode archive 命令接受变更 ID 参数。

#### 场景：更新 Antigravity 的斜杠命令
- **WHEN** `.agent/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 刷新每个文件的 OpenSpec 受管部分，使 workflow 副本与其他工具匹配，同时保留现有的单字段 `description` frontmatter
- **AND** 在更新期间跳过创建任何缺失的 workflow 文件，镜像 Windsurf 和其他 IDE 的行为

#### 场景：更新 Claude Code 的斜杠命令
- **WHEN** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 CodeBuddy Code 的斜杠命令
- **WHEN** `.codebuddy/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Cline 的斜杠命令
- **WHEN** `.clinerules/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 包含 Cline 特定的 Markdown 标题 frontmatter
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Crush 的斜杠命令
- **WHEN** `.crush/commands/` 包含 `openspec/proposal.md`、`openspec/apply.md` 和 `openspec/archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 包含 Crush 特定的 frontmatter，带有 OpenSpec 类别和标签
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Cursor 的斜杠命令
- **WHEN** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Factory Droid 的斜杠命令
- **WHEN** `.factory/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用包含 `description` 和 `argument-hint` 字段的 YAML frontmatter 的共享 Factory template 刷新每个文件
- **AND** 确保 template 主体保留 `$ARGUMENTS` 占位符，以便用户输入继续流入 droid
- **AND** 仅更新 OpenSpec 受管标记内的内容，不触动任何非受管注释
- **AND** 在更新期间跳过创建缺失文件

#### 场景：更新 OpenCode 的斜杠命令
- **WHEN** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令
- **AND** 确保 archive 命令在 frontmatter 中包含 `$ARGUMENTS` 占位符以接受变更 ID 参数

#### 场景：更新 Windsurf 的斜杠命令
- **WHEN** `.windsurf/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用包裹在 OpenSpec 标记中的共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令
- **AND** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Kilo Code 的斜杠命令
- **WHEN** `.kilocode/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用包裹在 OpenSpec 标记中的共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的指令
- **AND** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Codex 的斜杠命令
- **GIVEN** 全局 Codex 提示目录包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **WHEN** 用户运行 `openspec update`
- **THEN** 使用共享斜杠命令 template（包括占位符指导）刷新每个文件
- **AND** 保留 OpenSpec 标记块外的任何非受管内容
- **AND** 当 Codex 提示文件缺失时跳过创建

#### 场景：更新 GitHub Copilot 的斜杠命令
- **WHEN** `.github/prompts/` 包含 `openspec-proposal.prompt.md`、`openspec-apply.prompt.md` 和 `openspec-archive.prompt.md`
- **THEN** 使用共享 template 刷新每个文件，同时保留 YAML frontmatter
- **AND** 仅更新标记之间的 OpenSpec 受管块
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：更新 Gemini CLI 的斜杠命令
- **WHEN** `.gemini/commands/openspec/` 包含 `proposal.toml`、`apply.toml` 和 `archive.toml`
- **THEN** 使用共享的 proposal/apply/archive template 刷新每个文件的主体
- **AND** 仅替换 `prompt = """` 块内 `<!-- OPENSPEC:START -->` 和 `<!-- OPENSPEC:END -->` 标记之间的内容，使 TOML 框架（`description`、`prompt`）保持完整
- **AND** 在更新期间跳过创建任何缺失的 `.toml` 文件；仅刷新已存在的 Gemini 命令

#### 场景：更新 iFlow CLI 的斜杠命令
- **WHEN** `.iflow/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 保留带有 `name`、`id`、`category` 和 `description` 字段的 YAML frontmatter
- **AND** 仅更新标记之间的 OpenSpec 受管块
- **AND** 确保 template 包含相关 workflow 阶段的指令

#### 场景：缺失的斜杠命令文件
- **WHEN** 工具缺少斜杠命令文件时
- **THEN** 在更新期间不创建新文件
