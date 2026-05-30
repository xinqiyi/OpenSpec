## 为什么

当 `openspec status` 在不带 `--change` 且不存在变更的情况下被调用时（例如，在新初始化项目的上手期间），CLI 抛出致命错误：`未找到变更。使用以下命令创建一个：openspec new change <name>`。这破坏了上手流程，因为 AI 代理可能在创建任何变更之前调用 `openspec status`，导致代理停止或报告失败。修复 [#714](https://github.com/Fission-AI/OpenSpec/issues/714)。

## 变更内容

- `openspec status` 在不存在变更时将优雅退出（退出码 0）并显示友好消息，而非抛出致命错误
- `openspec status --json` 在不存在变更时将返回包含空变更数组的有效 JSON 对象
- 其他命令（`apply`、`show` 等）保留其当前的严格验证行为

## 能力

### 新能力

- `graceful-status-empty`：当不存在变更时对 `openspec status` 的优雅处理，涵盖文本和 JSON 输出模式

### 修改的能力

_无——`validateChangeExists` 在内部进行了重构，委托给新导出的 `getAvailableChanges`，但其行为和公共契约不变。其他消费者不受影响。_

## 影响

- `src/commands/workflow/shared.ts` — 提取 `getAvailableChanges` 作为公共函数（验证行为不变）
- `src/commands/workflow/status.ts` — 在验证前检查可用变更，优雅处理空情况
- 需要对 status 命令的测试进行更新，以覆盖新的优雅行为
