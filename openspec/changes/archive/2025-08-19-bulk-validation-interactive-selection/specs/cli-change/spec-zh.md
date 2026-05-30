# CLI Change 命令 spec

## 新增需求

### 需求：交互式验证选择

change validate 命令在未提供变更名称时应支持交互式选择。

#### 场景：用于验证的交互式变更选择

- **WHEN** 执行 `openspec change validate` 且不带参数时
- **THEN** 显示可用变更的交互式列表
- **AND** 允许用户选择要验证的变更
- **AND** 验证所选变更

#### 场景：非交互式回退保持当前行为

- **GIVEN** stdin 不是 TTY，或者提供了 `--no-interactive`，或者环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **WHEN** 执行 `openspec change validate` 且不带变更名称时
- **THEN** 不进行交互式提示
- **AND** 打印包含可用变更 ID 的现有提示
- **AND** 设置 `process.exitCode = 1`
