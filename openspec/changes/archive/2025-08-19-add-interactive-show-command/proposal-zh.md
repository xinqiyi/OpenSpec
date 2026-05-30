## 为什么

用户经常需要查看变更和 spec，但必须事先知道他们要看的是变更还是 spec。当前的子命令结构（`change show`、`spec show`）在以下情况下造成摩擦：
- 用户想要快速查看某个条目而不记住其类型
- 探索代码库需要在不同的 show 命令之间切换
- 不带参数的 show 命令返回错误而非帮助性指导

## 变更内容

- 添加新的顶层 `show` 命令，用于显示变更或 spec，具有智能选择功能
- 支持直接条目显示：`openspec show <item>`，自动检测类型
- 未提供参数时进行交互式选择
- 增强现有的 `change show` 和 `spec show` 以支持交互式选择（向后兼容）
- 保留所有现有格式选项（--json、--deltas-only、--requirements 等）

## 影响

- 需要创建的新 spec：cli-show
- 需要增强的 spec：cli-change、cli-spec（为向后兼容）
- 受影响的代码：src/cli/index.ts、src/commands/show.ts（新建）、src/commands/spec.ts、src/commands/change.ts
