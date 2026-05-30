## 为什么
archive 命令目前强制用户要么接受 spec 更新，要么取消整个 archive 操作。用户需要灵活性来 archive 变更而不更新 spec，可以通过显式标志或拒绝确认提示来实现。这对于不修改 spec 的变更（如工具、文档或基础设施更新）尤其重要。

## 变更内容
- 为 archive 命令添加新的 `--skip-specs` 标志，绕过所有 spec 更新操作
- 修复确认行为：当用户交互式拒绝 spec 更新时，继续 archive 而非取消整个操作
- 使用 `--skip-specs` 标志时，完全跳过 spec 发现和更新确认步骤
- 当跳过 spec 时（通过标志或用户选择），显示清晰的消息
- 该标志可与现有的 `--yes` 标志组合使用，实现无需 spec 更新的全自动 archive

## 影响
- 受影响的 spec：cli-archive
- 受影响的代码：src/core/archive.ts、src/cli/index.ts
