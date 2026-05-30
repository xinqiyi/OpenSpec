## 为什么

目前，用户必须通过指定每个 ID 来单独验证变更和规范。这在以下场景会造成不便：
- 团队希望在发布前验证所有变更/规范
- 开发者需要确保多个相关变更之间的一致性
- 用户运行验证命令时不带参数，收到错误而非有用的指导
- 子命令结构要求用户提前知道他们要验证的是变更还是规范

## 变更内容

- 添加新的顶级 `validate` 命令，带有直观的标志（--all、--changes、--specs）
- 增强现有的 `change validate` 和 `spec validate` 以支持交互式选择（向后兼容）
- 默认在未提供参数时进行交互式选择
- 支持直接项目验证：`openspec validate <item>` 并自动检测类型

## 影响

- 需创建的新规范：cli-validate
- 需增强的规范：cli-change、cli-spec（向后兼容）
- 受影响的代码：src/cli/index.ts、src/commands/validate.ts（新建）、src/commands/spec.ts、src/commands/change.ts
