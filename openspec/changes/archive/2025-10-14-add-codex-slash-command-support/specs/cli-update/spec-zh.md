## 修改后的需求
### 需求：斜杠命令更新
update 命令应刷新已配置工具的现有斜杠命令文件，而不创建新文件。

#### 场景：更新 Claude Code 的斜杠命令
- **当** `.claude/commands/openspec/` 包含 `proposal.md`、`apply.md` 和 `archive.md`
- **则** 使用共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 Cursor 的斜杠命令
- **当** `.cursor/commands/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **则** 使用共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 OpenCode 的斜杠命令
- **当** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **则** 使用共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明

#### 场景：更新 Windsurf 的斜杠命令
- **当** `.windsurf/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **则** 使用包裹在 OpenSpec 标记中的共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明
- **并且** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Kilo Code 的斜杠命令
- **当** `.kilocode/workflows/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **则** 使用包裹在 OpenSpec 标记中的共享模板刷新每个文件
- **并且** 确保模板包含相关工作流阶段的说明
- **并且** 跳过创建缺失文件（update 命令仅刷新已存在的文件）

#### 场景：更新 Codex 的斜杠命令
- **给定** 全局 Codex 提示目录包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`
- **当** 用户运行 `openspec update`
- **则** 使用共享斜杠命令模板（包含占位符指导）刷新每个文件
- **并且** 保留 OpenSpec 标记块外部的任何非管理内容
- **并且** 当 Codex 提示文件缺失时跳过创建

#### 场景：缺少斜杠命令文件
- **当** 某个工具缺少斜杠命令文件
- **则** 在更新过程中不创建新文件
