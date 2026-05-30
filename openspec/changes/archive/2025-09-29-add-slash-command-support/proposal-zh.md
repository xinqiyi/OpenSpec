# 为编码 Agent 添加斜杠命令支持

## 摘要
- 使 OpenSpec 能够为受支持的编码 Agent（Claude Code 和 Cursor）生成和更新自定义斜杠命令。
- 提供与 OpenSpec workflow 对齐的三个斜杠命令：proposal（启动变更 proposal）、apply（实施）和 archive（archive）。
- 在 Agent 之间共享斜杠命令 template，使未来扩展更简单。

## 动机
开发者使用不同的编码 Agent 和编辑器。在工具之间为 OpenSpec workflow 提供一致的斜杠命令可减少摩擦，并确保触发 workflow 的标准方式。现在同时支持 Claude Code 和 Cursor，为未来引入斜杠命令功能的 Agent 奠定基础。

## proposal
1. 在 `openspec init` 期间，当用户选择支持的工具时，为三个 OpenSpec workflow 阶段生成斜杠命令配置：
 - Claude（命名空间化）：`/openspec/proposal`、`/openspec/apply`、`/openspec/archive`。
 - Cursor（扁平化，带前缀）：`/openspec-proposal`、`/openspec-apply`、`/openspec-archive`。
 - 语义：
 - Create – 搭建变更框架（ID、`proposal.md`、`tasks.md`、delta spec）；严格验证。
 - Apply – 实施已批准的变更；完成任务；严格验证。
 - Archive – 部署后 archive；必要时更新 spec。
 - 每个命令文件必须嵌入来自 `openspec/README.md` 的简洁、逐步说明（参见 template 内容部分）。
2. 按工具存储斜杠命令文件：
 - Claude Code：`.claude/commands/openspec/{proposal,apply,archive}.md`
 - Cursor：`.cursor/commands/{openspec-proposal,openspec-apply,openspec-archive}.md`
 - 确保创建嵌套目录。
3. 命令文件格式和元数据：
 - 使用 Markdown，可选 YAML frontmatter 用于工具元数据（name/title、description、category/tags），当工具支持时。
 - OpenSpec 标记仅包裹正文，从不放在 frontmatter 内部。
 - 保持可见的斜杠名称、文件名和任何 frontmatter `name`/`id` 一致对齐（例如 `proposal`、`openspec-proposal`）。
 - 命名空间：将这些归类在"OpenSpec"下，优先使用唯一 ID（例如 `openspec-proposal`）以避免冲突。
4. 集中 template：定义命令正文一次并在工具间重用；应用最小的工具特定包装器（frontmatter、类别、文件名）。
5. 在 `openspec update` 期间，仅刷新标记内的现有斜杠命令文件（按文件处理）；不创建缺失的文件或新工具。

## 设计思路
- 引入 `SlashCommandConfigurator` 来管理每个工具的多个文件。
 - 暴露多个目标而不是单个 `configFileName`（例如 `getTargets(): Array<{ path: string; kind: 'slash'; id: string }>`）。
 - 为 init 提供 `generateAll(projectPath, openspecDir)`，为 update 提供 `updateExisting(projectPath, openspecDir)`。
- 每个工具的适配器仅添加 frontmatter 和路径；正文来自共享 template。
- template 存在于 `TemplateManager` 中，带有从 `openspec/README.md` 提取简洁、权威片段的助手。
- 更新流程记录每个文件的结果，使用户确切看到哪些斜杠文件被刷新。

### 标记放置
- 标记必须仅包裹 Markdown 正文内容：
 - Frontmatter（如果存在）放在首位。
 - 然后是 `<!-- OPENSPEC:START -->` … 正文 … `<!-- OPENSPEC:END -->`。
 - 避免将标记插入 YAML 块以防止解析错误。

### 幂等性和创建规则
- `init`：为所选工具一次性创建所有三个文件；后续 `init` 运行对现有文件是无操作的。
- `update`：仅刷新存在的文件；跳过缺失的文件而不创建新文件。
- 目录创建（`.claude/commands/openspec/` 和 `.cursor/commands/`）是配置器的责任。

### 命令命名和用户体验
- Claude Code：在斜杠本身中使用命名空间以提高可读性和分组：`/openspec/proposal`、`/openspec/apply`、`/openspec/archive`。
- Cursor：使用带有 `openspec-` 前缀的扁平名称：`/openspec-proposal`、`/openspec-apply`、`/openspec-archive`。支持时通过 `category: OpenSpec` 分组。
- 一致性：对齐文件名、可见斜杠名称和任何 frontmatter `id`（例如 `id: openspec-apply`）。
- 迁移：在 `update` 期间不重命名现有命令；仅在 `init` 时应用新命名（或通过显式迁移步骤）。

## 开放问题
- 验证每个工具版本支持的确切元数据/frontmatter；如果不支持，省略 frontmatter 并仅提供 Markdown 正文。
- 确认目标版本的最终 Cursor 命令文件位置；如果 Cursor 不解析 frontmatter，回退到仅 Markdown。
- 根据用户需求评估初始三个命令之外的额外命令（例如 `/show-change`、`/validate-all`）。

## 替代方案
- 按工具硬编码斜杠命令文本（被拒绝：内容重复；增加维护负担）。
- 推迟 Cursor 支持直到其配置稳定（部分接受）：在实际环境验证之前，将 Cursor 放在功能标志后面。

## 风险
- 工具配置格式可能变化，需要更新包装器/frontmatter。
- 不正确的路径或类别可能隐藏命令；添加路径存在性检查和清晰的日志记录。
- 标记误用（在 frontmatter 内部）可能破坏解析；在测试中强制执行放置规则。

## 未来工作
- 支持暴露斜杠命令 API 的其他编辑器/Agent。
- 允许用户在 `openspec init` 期间自定义命令名称和类别。
- 提供专用命令以重新生成斜杠命令，而无需运行完整的 `update`。

## 文件格式示例
以下示例说明预期结构。如果工具不支持 frontmatter，省略 YAML 块并仅保留标记 + 正文。

### Claude Code：`.claude/commands/openspec/proposal.md`
```markdown
---
name: OpenSpec: Proposal
description: 搭建新的 OpenSpec 变更并严格验证。
category: OpenSpec
tags: [openspec, change]
---
<!-- OPENSPEC:START -->
...来自共享 template 的命令正文...
<!-- OPENSPEC:END -->
```

斜杠调用：`/openspec/proposal`（命名空间化）

### Cursor：`.cursor/commands/openspec-proposal.md`
```markdown
---
name: /openspec-proposal
id: openspec-proposal
category: OpenSpec
description: 搭建新的 OpenSpec 变更并严格验证。
---
<!-- OPENSPEC:START -->
...来自共享 template 的命令正文...
<!-- OPENSPEC:END -->
```

斜杠调用：`/openspec-proposal`（扁平化，带前缀）

## template 内容
template 应简洁、可操作，并源自 `openspec/README.md` 以避免重复。每个命令正文包括：
- 护栏：如果需要，提出 1-2 个澄清问题；遵循最小复杂性规则；对 Node 项目使用 `pnpm`。
- 针对 workflow 阶段（proposal、apply、archive）定制的步骤列表，包括严格验证命令。
- 指向 `openspec show`、`openspec list` 的指针，以及验证失败时的故障排除提示。

## 测试策略
- 每个工具生成文件的黄金快照（frontmatter + 标记 + 正文）。
- 部分存在测试：如果 1-2 个文件存在，`update` 仅刷新这些文件，不创建缺失的文件。
- 标记放置测试：确保标记从不出现在 frontmatter 内部；覆盖缺失/重复标记的恢复行为。
- 日志测试：`update` 报告斜杠命令的每个文件更新。
