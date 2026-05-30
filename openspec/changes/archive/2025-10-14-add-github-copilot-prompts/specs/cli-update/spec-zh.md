## 修改后的需求

### 需求：斜杠命令更新
update 命令应刷新已配置工具的现有斜杠命令文件，而不创建新文件。

#### 场景：更新 Claude Code 的斜杠命令
- **WHEN** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Cursor 的斜杠命令
- **WHEN** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 OpenCode 的斜杠命令
- **WHEN** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：更新 Windsurf 的斜杠命令
- **WHEN** `.windsurf/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用包裹在 OpenSpec 标记中的共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明
- **AND** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Kilo Code 的斜杠命令
- **WHEN** `.kilocode/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **THEN** 使用包裹在 OpenSpec 标记中的共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明
- **AND** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Codex 的斜杠命令
- **GIVEN** 全局 Codex 提示目录包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **WHEN** 用户运行 `openspec update`
- **THEN** 使用共享斜杠命令 template（包含占位符指导）刷新每个文件
- **AND** 保留 OpenSpec 标记块外部的任何非管理内容
- **AND** 当 Codex 提示文件缺失时跳过创建

#### 场景：更新 GitHub Copilot 的斜杠命令
- **WHEN** `.github/prompts/` 包含 `openspec-proposal.prompt.md`、`openspec-apply.prompt.md` 和 `openspec-archive.prompt.md`
- **THEN** 在使用共享 template 刷新每个文件的同时保留 YAML frontmatter
- **AND** 仅更新标记之间的 OpenSpec 管理块
- **AND** 确保 template 包含相关 workflow 阶段的说明

#### 场景：缺少斜杠命令文件
- **WHEN** 某个工具缺少斜杠命令文件
- **THEN** 在更新过程中不创建新文件
