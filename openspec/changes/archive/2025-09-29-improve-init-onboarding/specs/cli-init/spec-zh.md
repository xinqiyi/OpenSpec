## 已修改的需求

### 需求：AI 工具配置

命令应根据用户选择，使用 OpenSpec 指令配置 AI 编码助手。

#### 场景：提示选择 AI 工具

- **WHEN** 以交互方式运行时
- **THEN** 使用多选菜单提示用户"您使用哪些 AI 工具？"
- **AND** 使用复选框列出每个可用工具：
 - Claude Code（创建或刷新 CLAUDE.md 和斜杠命令）
 - Cursor（创建或刷新 `.cursor/commands/*` 斜杠命令）
 - AGENTS.md 标准（创建或刷新带 OpenSpec 标记的 AGENTS.md）
- **AND** 在受管文件已存在的工具旁显示"（已配置）"，让用户了解选择将刷新内容
- **AND** 将禁用的工具视为"即将推出"并保持不可选
- **AND** 在选择一个或多个工具后允许按 Enter 确认

### 需求：AI 工具配置详情

命令应使用标记系统，使用 OpenSpec 特定指令正确配置所选 AI 工具。

#### 场景：配置 Claude Code

- **WHEN** 选择了 Claude Code
- **THEN** 在项目根目录（不在 openspec/ 内）创建或更新 `CLAUDE.md`

#### 场景：创建新的 CLAUDE.md

- **WHEN** CLAUDE.md 不存在时
- **THEN** 创建新文件，包含包裹在标记中的 OpenSpec 内容：
```markdown
<!-- OPENSPEC:START -->
# OpenSpec 指令

面向使用 OpenSpec 进行 spec 驱动开发的 AI 编码助手的说明。

## TL;DR 快速检查清单
- 搜索现有工作：`openspec spec list --long`、`openspec list`
- 确定范围：新能力 vs 修改现有能力
- 选择唯一的 `change-id`：动词主导的 kebab-case（`add-`、`update-`、`remove-`、`refactor-`）
- 搭建结构：`proposal.md`、`tasks.md`、可选的 `design.md` 和 spec delta
- 使用 `openspec validate [change-id] --strict` 验证
- 在实施前请求批准
<!-- OPENSPEC:END -->
```

#### 场景：更新现有的 CLAUDE.md

- **WHEN** CLAUDE.md 已存在
- **THEN** 保留所有现有内容
- **AND** 在文件开头使用标记插入 OpenSpec 内容
- **AND** 如果标记已存在，确保不重复

#### 场景：使用标记管理内容

- **WHEN** 使用标记系统时
- **THEN** 使用 `<!-- OPENSPEC:START -->` 标记受管内容的开始
- **AND** 使用 `<!-- OPENSPEC:END -->` 标记受管内容的结束
- **AND** 允许 OpenSpec 更新其内容而不影响用户自定义内容
- **AND** 完整保留标记外的所有内容

### 需求：交互 schema

命令应提供带有清晰导航说明的 AI 工具选择交互菜单。

#### 场景：显示交互菜单

- **WHEN** 运行时
- **THEN** 提示用户："您使用哪些 AI 工具？"
- **AND** 显示基于复选框的多选菜单，包含可用工具（Claude Code、Cursor、AGENTS.md 标准）
- **AND** 将禁用选项显示为"即将推出"（不可选）
- **AND** 显示内联帮助，指示空格键切换选择，Enter 键确认

#### 场景：导航菜单

- **WHEN** 用户在菜单中时
- **THEN** 允许使用箭头键在选项之间移动
- **AND** 允许使用空格键切换高亮选项
- **AND** 允许使用 Enter 键确认所有当前选择

### 需求：成功输出

命令应在成功初始化时提供清晰、可操作的后续步骤。

#### 场景：显示成功消息

- **WHEN** 初始化成功完成
- **THEN** 显示成功横幅，后跟针对所选工具的个性化可操作提示
- **AND** 总结哪些助手文件是创建的与刷新的（例如 `CLAUDE.md (created)`、`.cursor/commands/openspec-apply.md (refreshed)`）
- **AND** 为每个配置的助手包含可复制粘贴的上手提示，将占位文本（[您在此处的功能]）替换为自定义的实际指导
- **AND** 当没有工具特定的文件时（例如仅选择了 AGENTS.md 标准），引用兼容 AGENTS.md 的助手
