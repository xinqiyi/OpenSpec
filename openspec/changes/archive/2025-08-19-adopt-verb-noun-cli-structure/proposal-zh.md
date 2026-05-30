# 变更：采用动词-名词 CLI 结构（弃用基于名词的命令）

## 为什么

大多数广泛使用的 CLI（git、docker、kubectl）以动作（动词）开头，后跟对象（名词）。这与用户的思维方式一致："对 Y 做 X"。使用动词作为顶级命令可以提高清晰度、可发现性和可扩展性。

## 变更内容

- 将顶级动词命令提升为主要入口点：`list`、`show`、`validate`、`diff`、`archive`。
- 弃用基于名词的顶级命令：`openspec spec ...` 和 `openspec change ...`。
- 在适用时通过标志引入一致的名词范围（例如 `--changes`、`--specs`），并保持智能默认值。
- 明确名称冲突时 `show` 和 `validate` 的消歧。

### 映射（从 → 到）

- **列出**
 - 从：`openspec change list`
 - 到：`openspec list --changes`（默认），或 `openspec list --specs`

- **查看**
 - 从：`openspec spec show <spec-id>` / `openspec change show <change-id>`
 - 到：`openspec show <item-id>` 自动检测，如有歧义使用 `--type spec|change`

- **验证**
 - 从：`openspec spec validate <spec-id>` / `openspec change validate <change-id>`
 - 到：`openspec validate <item-id> --type spec|change`，或批量：`openspec validate --specs` / `--changes` / `--all`

### 向后兼容性

- 保留 `openspec spec` 和 `openspec change` 可用，附带一个发布周期的弃用警告。
- 更新帮助文本，引导用户使用动词-名词替代方案。

## 影响

- **受影响的 spec**：
 - `cli-list`：添加对 `--specs` 和显式 `--changes` 的支持（默认保持为变更）
 - `openspec-conventions`：添加显式需求，建立动词-名词 CLI 设计和弃用指南
- **受影响的代码**：
 - `src/cli/index.ts`：取消弃用顶级 `list`；将 `change list` 标记为已弃用；确保帮助文本和警告一致
 - `src/core/list.ts`：支持通过 `--specs` 列出 spec，默认列出变更；共享输出结构
 - 可选的后续工作：收紧 `show`/`validate` 的帮助和歧义处理

## 显式变更

**CLI 设计**
- 从：混合 schema，有名词（`spec`、`change`）和部分顶级动词；`openspec list` 当前已弃用
- 到：动词作为主要形式：`openspec list|show|validate|diff|archive`；名词通过标志或项目 ID 限定范围；名词命令已弃用
- 原因：与常见 CLI 对齐；改善用户体验；更简单的心理模型
- 影响：在弃用期内非破坏性；用户逐步迁移

**列出行为**
- 从：`openspec change list`（主要），`openspec list`（已弃用）
- 到：`openspec list` 作为主要形式，默认使用 `--changes`；添加 `--specs` 以列出 spec
- 原因：一致的动词-名词风格；更好的可发现性
- 影响：新增选项；通过默认值保持现有行为

## 推广和弃用策略

- 在一个发布周期内对基于名词的命令显示弃用警告。
- 在 `openspec/README.md` 和 CLI 帮助中记录新用法。
- 一个发布周期后，考虑移除基于名词的命令，或作为薄别名保留但不显示警告。

## 未解决的问题

- `show` 是否也应接受 `--changes`/`--specs` 以进行无需 ID 的发现？（此范围外；当前的自动检测和 `--type` 保持有效。）
