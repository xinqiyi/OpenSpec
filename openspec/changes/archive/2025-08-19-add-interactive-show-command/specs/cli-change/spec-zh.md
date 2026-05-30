# CLI Change 命令规范

## 新增需求

### 需求：交互式 show 选择

change show 命令在未提供变更名称时应支持交互式选择。

#### 场景：用于 show 的交互式变更选择

- **当** 执行 `openspec change show` 且不带参数时
- **则** 显示可用变更的交互式列表
- **且** 允许用户选择要显示的变更
- **且** 显示所选变更内容
- **且** 保持所有现有 show 选项（--json、--deltas-only）

#### 场景：非交互式回退保持当前行为

- **给定** stdin 不是 TTY，或者提供了 `--no-interactive`，或者环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **当** 执行 `openspec change show` 且不带变更名称时
- **则** 不进行交互式提示
- **且** 打印包含可用变更 ID 的现有提示
- **且** 设置 `process.exitCode = 1`
