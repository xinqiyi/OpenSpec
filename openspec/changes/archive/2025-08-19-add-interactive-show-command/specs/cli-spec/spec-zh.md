# CLI Spec 命令 spec

## 新增需求

### 需求：交互式 spec show

spec show 命令在未提供 spec-id 时应支持交互式选择。

#### 场景：用于 show 的交互式 spec 选择

- **WHEN** 执行 `openspec spec show` 且不带参数时
- **THEN** 显示可用 spec 的交互式列表
- **AND** 允许用户选择要显示的 spec
- **AND** 显示所选 spec 内容
- **AND** 保持所有现有 show 选项（--json、--requirements、--no-scenarios、-r）

#### 场景：非交互式回退保持当前行为

- **GIVEN** stdin 不是 TTY，或者提供了 `--no-interactive`，或者环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **WHEN** 执行 `openspec spec show` 且不带 spec-id 时
- **THEN** 不进行交互式提示
- **AND** 打印缺少 spec-id 的现有错误消息
- **AND** 设置非零退出码
