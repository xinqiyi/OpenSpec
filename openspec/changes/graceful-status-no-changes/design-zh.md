## 上下文

`src/commands/workflow/status.ts` 中的 `statusCommand` 将调用 `shared.ts` 中的 `validateChangeExists()` 作为其第一个操作。当未提供 `--change` 选项且不存在变更目录时，`validateChangeExists` 抛出：`未找到变更。使用以下命令创建一个：openspec new change <name>`。此错误作为致命 CLI 错误（非零退出码）向上传播。

这对需要操作变更的 `apply` 和 `show` 等命令是正确的行为。然而，`status` 是一个信息性命令——它应报告当前状态，即使该状态是"不存在变更"。

该错误在上手期间（问题 #714）出现，当 AI agent 在创建任何变更之前调用 `openspec status` 时。

## 目标 / 非目标

**目标：**
- 使 `openspec status` 在不存在变更时以退出码 0 和友好消息退出
- 支持无变更情况下的文本和 JSON 输出 schema
- 保持所有其他命令的验证行为不变

**非目标：**
- 更改 `validateChangeExists` 的行为（对所有消费者保持严格；仅提取其内部辅助函数）
- 更改上手 template 或 skill 说明
- 处理提供了 `--change` 但特定变更不存在的情况（应保持为错误）

## 决策

### 提取 `getAvailableChanges` 并在验证前检查

**理由**：将 `validateChangeExists` 中的私有 `getAvailableChanges` 闭包提取为 `shared.ts` 中公开导出的函数。然后，在 `statusCommand` 中，在 `validateChangeExists` 之前调用 `getAvailableChanges`，以早期检测无变更情况并优雅处理。这避免了使用 try/catch 进行控制流，并消除了对错误消息字符串的任何耦合。

**考虑的替代方案**：通过匹配 `error.message.startsWith('No changes found')` 捕获来自 `validateChangeExists` 的错误。由于字符串耦合很脆弱——如果错误消息发生变化，捕获会静默失效，因此被拒绝。

**考虑的替代方案**：向 `validateChangeExists` 添加 `throwOnEmpty` 参数。由于它为单个消费者的需求向共享函数增加了复杂性，并将用户体验问题混入验证工具中，因此被拒绝。

### 保持 `validateChangeExists` 严格

**理由**：`validateChangeExists` 在行为上保持不变——它仍然为所有错误情况抛出异常。优雅处理完全存在于 `statusCommand` 中，这是用户体验决策的适当层。其他命令（`apply`、`show`、`instructions`）不受影响。

## 风险 / 权衡

- **[风险]** 当未提供 `--change` 且变更确实存在时，额外的文件系统读取（先调用 `getAvailableChanges`，然后 `validateChangeExists` 执行自己的读取）-- 缓解措施：当不存在变更时，`statusCommand` 在到达 `validateChangeExists` 之前提前返回，因此双重读取仅在存在变更时发生——开销极小。
- **[风险]** 未来其他命令也可能受益于优雅的无变更处理 -- 缓解措施：`getAvailableChanges` 现在是公开且可复用的，使得在其他地方应用相同 schema 变得容易。
