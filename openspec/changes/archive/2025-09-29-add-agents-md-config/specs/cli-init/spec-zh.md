## 修改后的需求
### 需求：AI 工具配置
命令应根据用户选择使用 OpenSpec 指令配置 AI 编码助手。

#### 场景：提示 AI 工具选择

- **当** 运行时
- **那么** 提示用户选择要配置的 AI 工具：
  - Claude Code（✅ 可使用 OpenSpec 自定义斜杠命令）
  - Cursor（✅ 可使用 OpenSpec 自定义斜杠命令）
  - AGENTS.md（可与 Codex、Amp、Copilot 等配合使用）

### 需求：AI 工具配置详情
命令应使用标记系统为选定的 AI 工具正确配置 OpenSpec 特定指令。

#### 场景：配置 Claude Code

- **当** 选择了 Claude Code
- **那么** 在项目根目录（不在 openspec/ 内部）创建或更新 `CLAUDE.md`

#### 场景：配置 AGENTS 标准

- **当** 选择了 AGENTS.md 标准
- **那么** 在项目根目录（不在 openspec/ 内部）创建或更新 `AGENTS.md`

#### 场景：创建新的 CLAUDE.md

- **当** CLAUDE.md 不存在时
- **那么** 创建包含包裹在标记中的 OpenSpec 内容的新文件：
```markdown
<!-- OPENSPEC:START -->
# OpenSpec 项目

本文档为 AI 编码助手提供有关如何使用 OpenSpec 规范进行规范驱动开发的说明。在 OpenSpec 启用的项目上工作时，请严格遵守这些规则。

本项目使用 OpenSpec 进行规范驱动开发。规范是事实的源头。

有关详细的约定和指南，请参阅 @openspec/AGENTS.md。
<!-- OPENSPEC:END -->
```

#### 场景：创建新的 AGENTS.md

- **当** 项目根目录中不存在 AGENTS.md
- **那么** 使用与 CLAUDE.md 相同的模板创建包含包裹在标记中的 OpenSpec 内容的新文件

#### 场景：更新现有的 CLAUDE.md

- **当** CLAUDE.md 已存在
- **那么** 保留所有现有内容
- **并且** 使用标记在文件开头插入 OpenSpec 内容
- **并且** 确保标记不会重复（如果已存在）

#### 场景：更新现有的 AGENTS.md

- **当** AGENTS.md 已存在于项目根目录中
- **那么** 保留所有现有内容
- **并且** 确保文件开头的 OpenSpec 管理块被刷新而不重复标记

#### 场景：使用标记管理内容

- **当** 使用标记系统时
- **那么** 使用 `<!-- OPENSPEC:START -->` 标记管理内容的开始
- **并且** 使用 `<!-- OPENSPEC:END -->` 标记管理内容的结束
- **并且** 允许 OpenSpec 更新其内容而不影响用户自定义
- **并且** 完整保留标记外的所有内容

为何使用标记：
- 用户可能希望保留现有的 CLAUDE.md 或 AGENTS.md 指令
- OpenSpec 可以在未来版本中更新其指令
- OpenSpec 管理和用户管理内容之间有清晰的边界
