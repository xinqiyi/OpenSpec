# CLI 显示命令 spec

## 新增的需求

### 需求：顶级 show 命令

CLI 应提供一个顶级 `show` 命令，用于显示变更和 spec，并具有智能选择功能。

#### 场景：交互式显示选择

- **WHEN** 执行 `openspec show` 不带参数
- **THEN** 提示用户选择类型（变更或 spec）
- **AND** 显示所选类型的可用项目列表
- **AND** 显示所选项目的内容

#### 场景：非交互式环境不提示

- **GIVEN** 标准输入不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **WHEN** 执行 `openspec show` 不带参数
- **THEN** 不进行提示
- **AND** 打印带有 `openspec show <item>` 或 `openspec change/spec show` 示例的有用提示
- **AND** 以退出码 1 退出

#### 场景：直接项目显示

- **WHEN** 执行 `openspec show <item-name>`
- **THEN** 自动检测项目是变更还是 spec
- **AND** 显示项目的内容
- **AND** 根据项目类型使用适当的格式

#### 场景：类型检测和歧义处理

- **WHEN** 执行 `openspec show <item-name>`
- **THEN** 如果 `<item-name>` 唯一匹配变更或 spec，显示该项目
- **AND** 如果同时匹配两者，打印歧义错误并建议 `--type change|spec` 或使用 `openspec change show`/`openspec spec show`
- **AND** 如果都不匹配，打印未找到信息并给出最接近匹配的建议

#### 场景：显式类型覆盖

- **WHEN** 执行 `openspec show --type change <item>`
- **THEN** 将 `<item>` 视为变更 ID 并显示（跳过自动检测）

- **WHEN** 执行 `openspec show --type spec <item>`
- **THEN** 将 `<item>` 视为 spec ID 并显示（跳过自动检测）

### 需求：输出格式选项

show 命令应支持与现有命令一致的各种输出格式。

#### 场景：JSON 输出

- **WHEN** 执行 `openspec show <item> --json`
- **THEN** 以 JSON 格式输出项目
- **AND** 包含解析后的元数据和结构
- **AND** 与现有变更/spec show 命令保持格式一致

#### 场景：标志作用域和委托

- **WHEN** 通过顶级命令显示变更或 spec 时
- **THEN** 接受诸如 `--json` 等通用标志
- **AND** 将类型特定的标志传递给相应的实现
 - 仅变更标志：`--deltas-only`（`--requirements-only` 已弃用）
 - 仅 spec 标志：`--requirements`、`--no-scenarios`、`-r/--requirement`
- **AND** 对检测到的类型忽略无关标志并发出警告

### 需求：交互性控制

- CLI 应遵循 `--no-interactive` 来禁用提示。
- CLI 应遵循 `OPEN_SPEC_INTERACTIVE=0` 来全局禁用提示。
- 交互式提示仅在标准输入是 TTY 且交互性未被禁用时显示。

#### 场景：变更特定选项

- **WHEN** 使用 `openspec show <change-name> --deltas-only` 显示变更时
- **THEN** 仅以 JSON 格式显示 delta
- **AND** 与现有变更 show 选项保持兼容

#### 场景：spec 特定选项

- **WHEN** 使用 `openspec show <spec-id> --requirements` 显示 spec 时
- **THEN** 仅以 JSON 格式显示需求
- **AND** 支持其他 spec 选项（--no-scenarios、-r）
- **AND** 与现有 spec show 选项保持兼容
