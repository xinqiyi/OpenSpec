# 添加归档命令参数

## 为什么
`/openspec:archive` 斜杠命令目前缺乏参数支持，迫使 AI 从对话上下文中推断要归档哪个变更，或者列出所有变更。如果上下文存在歧义或存在多个变更，这会造成安全风险，可能归档错误的提案。用户期望能够明确指定变更 ID，与 CLI 命令 `openspec archive <id>` 的行为保持一致。

## 变更内容
- 在 OpenCode 归档斜杠命令的前置元数据中添加 `$ARGUMENTS` 占位符（与提案命令的现有模式匹配）
- 更新归档命令模板步骤，以在提供时验证特定的变更 ID 参数
- 注意：Codex、GitHub Copilot 和 Amazon Q 的归档命令已支持 `$ARGUMENTS`；Claude/Cursor/Windsurf/Kilocode 不支持参数

## 影响范围
- 受影响的规范：`cli-update`（斜杠命令生成逻辑）
- 受影响的代码：
  - `src/core/configurators/slash/opencode.ts`（向归档前置元数据添加 `$ARGUMENTS`）
  - `src/core/templates/slash-command-templates.ts`（归档模板步骤，用于参数验证）
- 破坏性变更：否——这是增强安全性的附加功能
- 用户可见：是——OpenCode 用户将能够传递变更 ID 作为参数：`/openspec:archive <change-id>`
