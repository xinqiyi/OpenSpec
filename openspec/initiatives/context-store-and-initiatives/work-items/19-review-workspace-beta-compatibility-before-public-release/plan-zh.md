# 在公共发布前审查 workspace Beta 兼容性

## 目标

在 workspace 变为公共/稳定之前，决定哪些 Beta workspace 兼容性行为真正值得继承。

这是故意放在后期的工作。workspace 尚未公开发布，因此未发布的 Beta 内部实现不应自动成为永久兼容性契约。

## 背景

Beta 版本目前包含一些兼容性路径：

- 用于 `.openspec-workspace/workspace.yaml` 和 `.openspec-workspace/local.yaml` 的旧分裂 workspace 状态读取器。
- 受管 workspace 注册表回退行为。
- `codex` 到 `codex-cli` 开启器 spec 化。
- 针对旧 workspace `.code-workspace` 忽略规则的生成 `.gitignore` 清理。
- 仅因之前的 workspace 切片在内部暴露而存在的空或已弃用的辅助垫片。

其中一些可能对本地 Beta 测试人员有用。其他的在公共发布前删除可能更安全。

## 范围

仅审查 workspace 兼容性。不要使用此项目重新打开无关的遗留迁移系统，如旧的斜杠命令清理、遥测配置迁移或已弃用的 `change`/`spec` 命令别名。

## 需要做出的决策

- 哪些 workspace 兼容性路径是公共契约的一部分？
- 哪些路径是仅 Beta 的迁移辅助工具，可以在一次发布说明或清理后移除？
- 哪些路径仅用于测试兼容性，可以在发布前删除？
- Beta workspace 根路径应自动迁移、保持可读，还是有意不支持？
- 鉴于 workspace 是受管本地文件夹而非 repository，旧的生成 `.gitignore` 清理是否应该存在？

## 实施说明

- 优先选择删除而非为未发布的中间 Beta 状态保留兼容性。
- 如果保留兼容性路径，记录其存在的原因以及后续允许移除的条件。
- 保护用户拥有的文件安全。不要清理或重写模糊的本地文件，除非 OpenSpec 可以证明其拥有它们。
- 更新测试，使其描述所选的公共契约，而非偶然的 Beta 历史。

## 完成条件

- workspace 兼容性代码已盘点并分类。
- 低价值的仅 Beta 垫片已移除。
- 剩余的兼容性行为有重点测试和发布说明措辞。
- 公共文档和生成的 agent 指导不提及不支持的 Beta 内部实现。
