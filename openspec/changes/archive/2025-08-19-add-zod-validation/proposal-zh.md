# 变更：添加 Zod 运行时验证

## 为什么

虽然 spec 和 change 命令可以输出 JSON，但它们目前不执行超出基本结构检查的严格运行时验证。这可能导致无效的规范或变更被处理、必需字段缺失时的静默失败以及糟糕的错误消息。

## 变更内容

- 使用严格的 Zod 验证增强现有的 `spec validate` 和 `change validate` 命令
- 为 archive 命令添加验证，确保变更在应用前有效
- 为 diff 命令添加验证，确保变更格式正确
- 提供 JSON 格式的详细验证报告
- 添加在警告上失败的 `--strict` 模式

## 影响

- **受影响的规范**：cli-spec、cli-change、cli-archive、cli-diff
- **受影响的代码**：
  - src/commands/spec.ts（增强 validate 子命令）
  - src/commands/change.ts（增强 validate 子命令）
  - src/core/archive.ts（添加上档前验证）
  - src/core/diff.ts（添加验证检查）
