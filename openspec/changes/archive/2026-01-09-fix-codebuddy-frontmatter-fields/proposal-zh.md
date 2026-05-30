## 原因

CodeBuddy 斜杠命令配置器目前使用与其他工具不一致的 frontmatter 字段。它使用 `category` 和 `tags` 字段（与 Crush 一样），但应使用 `argument-hint` 字段（与 Factory、Auggie 和 Codex 一样）以保持更好的一致性。此外，`proposal` 命令完全缺少 frontmatter 字段。在查阅 CodeBuddy 官方文档后，正确的格式应使用 `description` 和 `argument-hint` 字段，并采用方括号参数格式。

## 变更内容

- 将 CodeBuddy frontmatter 中的 `category` 和 `tags` 字段替换为 `argument-hint` 字段
- 为 `proposal` 命令添加缺失的 frontmatter 字段
- 使用正确的方括号格式作为 `argument-hint` 参数（例如 `[change-id]`）
- 确保与 CodeBuddy 官方文档保持一致

## 影响范围

- 受影响的规格文件：cli-init, cli-update
- 受影响的代码：`src/core/configurators/slash/codebuddy.ts`
- CodeBuddy 用户将在斜杠命令中获得正确格式的适当参数提示
