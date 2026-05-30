# CLI Validate 命令 spec

## 新增需求

### 需求：顶级 validate 命令

CLI 应提供一个顶级的 `validate` 命令，用于验证变更和 spec，并提供灵活的选择选项。

#### 场景：交互式验证选择

- **WHEN** 执行 `openspec validate` 不带参数
- **THEN** 提示用户选择要验证的内容（全部、变更、spec 或特定项）
- **AND** 根据选择执行验证
- **AND** 使用适当的格式显示结果

#### 场景：非交互式环境不提示

- **鉴于** stdin 不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **WHEN** 执行 `openspec validate` 不带参数
- **THEN** 不进行交互式提示
- **AND** 打印有用的提示，列出可用的命令/标志，并以退出码 1 退出

#### 场景：直接项验证

- **WHEN** 执行 `openspec validate <item-name>`
- **THEN** 自动检测该项是变更还是 spec
- **AND** 验证指定的项
- **AND** 显示验证结果

### 需求：批量验证和过滤验证

validate 命令应支持批量验证的标志（--all）和按类型过滤验证（--changes、--specs）。

#### 场景：验证所有内容

- **WHEN** 执行 `openspec validate --all`
- **THEN** 验证 openspec/changes/ 中的所有变更（排除 archive）
- **AND** 验证 openspec/specs/ 中的所有 spec
- **AND** 显示通过/失败项的摘要
- **AND** 如果任何验证失败，以退出码 1 退出

#### 场景：批量验证的范围

- **WHEN** 使用 `--all` 或 `--changes` 验证时
- **THEN** 包含 `openspec/changes/` 下的所有变更 proposal
- **AND** 排除 `openspec/changes/archive/` 目录

- **WHEN** 使用 `--specs` 验证时
- **THEN** 包含所有在 `openspec/specs/<id>/spec.md` 下有 spec.md 的 spec

#### 场景：验证所有变更

- **WHEN** 执行 `openspec validate --changes`
- **THEN** 验证 openspec/changes/ 中的所有变更（排除 archive）
- **AND** 显示每个变更的结果
- **AND** 显示摘要统计信息

#### 场景：验证所有 spec

- **WHEN** 执行 `openspec validate --specs`
- **THEN** 验证 openspec/specs/ 中的所有 spec
- **AND** 显示每个 spec 的结果
- **AND** 显示摘要统计信息

### 需求：验证选项和进度指示

validate 命令应支持标准验证选项（--strict、--json），并在批量操作期间显示进度。

#### 场景：严格验证

- **WHEN** 执行 `openspec validate --all --strict`
- **THEN** 对所有项应用严格验证
- **AND** 将警告视为错误
- **AND** 如果任何项有警告或错误则失败

#### 场景：JSON 输出

- **WHEN** 执行 `openspec validate --all --json`
- **THEN** 以 JSON 格式输出验证结果
- **AND** 包含每个项的详细问题
- **AND** 包含摘要统计信息

#### 场景：批量验证的 JSON 输出 schema

- **WHEN** 执行 `openspec validate --all --json`（或 `--changes` / `--specs`）
- **THEN** 输出一个 JSON 对象，结构如下：
 - `items`：对象数组，包含字段 `{ id: string, type: "change"|"spec", valid: boolean, issues: Issue[], durationMs: number }`
 - `summary`：对象 `{ totals: { items: number, passed: number, failed: number }, byType: { change?: { items: number, passed: number, failed: number }, spec?: { items: number, passed: number, failed: number } } }`
 - `version`：schema 的字符串标识符（例如 `"1.0"`）
- **AND** 如果任何 `items[].valid === false`，以退出码 1 退出

其中 `Issue` 遵循现有的逐项验证报告结构 `{ level: "ERROR"|"WARNING"|"INFO", path: string, message: string }`。

#### 场景：显示验证进度

- **WHEN** 验证多个项时（--all、--changes 或 --specs）
- **THEN** 显示进度指示器或状态更新
- **AND** 指示当前正在验证哪一项
- **AND** 显示通过/失败项的实时计数

#### 场景：并发限制以提升性能

- **WHEN** 验证多个项时
- **THEN** 以有限的并发度运行验证（例如 4-8 个并行）
- **AND** 确保进度指示器保持响应

### 需求：项类型检测和歧义处理

validate 命令应处理歧义名称和显式类型覆盖，以确保清晰、确定性的行为。

#### 场景：直接项验证与自动类型检测

- **WHEN** 执行 `openspec validate <item-name>`
- **THEN** 如果 `<item-name>` 唯一匹配一个变更或 spec，验证该项

#### 场景：变更和 spec 名称之间的歧义

- **鉴于** `<item-name>` 同时作为变更和 spec 存在
- **WHEN** 执行 `openspec validate <item-name>`
- **THEN** 打印歧义错误，解释两个匹配项
- **AND** 建议传递 `--type change` 或 `--type spec`，或使用 `openspec change validate` / `openspec spec validate`
- **AND** 以退出码 1 退出，不执行验证

#### 场景：未知项名称

- **WHEN** `<item-name>` 既不匹配变更也不匹配 spec
- **THEN** 打印未找到错误
- **AND** 在可能时显示最接近的匹配建议
- **AND** 以退出码 1 退出

#### 场景：显式类型覆盖

- **WHEN** 执行 `openspec validate --type change <item>`
- **THEN** 将 `<item>` 视为变更 ID 并验证（跳过自动检测）

- **WHEN** 执行 `openspec validate --type spec <item>`
- **THEN** 将 `<item>` 视为 spec ID 并验证（跳过自动检测）

### 需求：交互性控制

- CLI 应遵循 `--no-interactive` 以禁用提示。
- CLI 应遵循 `OPEN_SPEC_INTERACTIVE=0` 以全局禁用提示。
- 交互式提示仅应在 stdin 为 TTY 且交互性未被禁用时显示。

#### 场景：通过标志或环境变量禁用提示

- **WHEN** 使用 `--no-interactive` 或环境变量 `OPEN_SPEC_INTERACTIVE=0` 执行 `openspec validate`
- **THEN** CLI 应不显示交互式提示
- **AND** 应根据情况打印非交互式提示或选择的输出
