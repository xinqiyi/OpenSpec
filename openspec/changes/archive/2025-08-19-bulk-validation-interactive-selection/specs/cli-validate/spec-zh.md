# CLI Validate 命令规范

## 新增需求

### 需求：顶级 validate 命令

CLI 应提供一个顶级的 `validate` 命令，用于验证变更和规范，并提供灵活的选择选项。

#### 场景：交互式验证选择

- **当** 执行 `openspec validate` 不带参数
- **那么** 提示用户选择要验证的内容（全部、变更、规范或特定项）
- **并且** 根据选择执行验证
- **并且** 使用适当的格式显示结果

#### 场景：非交互式环境不提示

- **鉴于** stdin 不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **当** 执行 `openspec validate` 不带参数
- **那么** 不进行交互式提示
- **并且** 打印有用的提示，列出可用的命令/标志，并以退出码 1 退出

#### 场景：直接项验证

- **当** 执行 `openspec validate <item-name>`
- **那么** 自动检测该项是变更还是规范
- **并且** 验证指定的项
- **并且** 显示验证结果

### 需求：批量验证和过滤验证

validate 命令应支持批量验证的标志（--all）和按类型过滤验证（--changes、--specs）。

#### 场景：验证所有内容

- **当** 执行 `openspec validate --all`
- **那么** 验证 openspec/changes/ 中的所有变更（排除 archive）
- **并且** 验证 openspec/specs/ 中的所有规范
- **并且** 显示通过/失败项的摘要
- **并且** 如果任何验证失败，以退出码 1 退出

#### 场景：批量验证的范围

- **当** 使用 `--all` 或 `--changes` 验证时
- **那么** 包含 `openspec/changes/` 下的所有变更提案
- **并且** 排除 `openspec/changes/archive/` 目录

- **当** 使用 `--specs` 验证时
- **那么** 包含所有在 `openspec/specs/<id>/spec.md` 下有 spec.md 的规范

#### 场景：验证所有变更

- **当** 执行 `openspec validate --changes`
- **那么** 验证 openspec/changes/ 中的所有变更（排除 archive）
- **并且** 显示每个变更的结果
- **并且** 显示摘要统计信息

#### 场景：验证所有规范

- **当** 执行 `openspec validate --specs`
- **那么** 验证 openspec/specs/ 中的所有规范
- **并且** 显示每个规范的结果
- **并且** 显示摘要统计信息

### 需求：验证选项和进度指示

validate 命令应支持标准验证选项（--strict、--json），并在批量操作期间显示进度。

#### 场景：严格验证

- **当** 执行 `openspec validate --all --strict`
- **那么** 对所有项应用严格验证
- **并且** 将警告视为错误
- **并且** 如果任何项有警告或错误则失败

#### 场景：JSON 输出

- **当** 执行 `openspec validate --all --json`
- **那么** 以 JSON 格式输出验证结果
- **并且** 包含每个项的详细问题
- **并且** 包含摘要统计信息

#### 场景：批量验证的 JSON 输出模式

- **当** 执行 `openspec validate --all --json`（或 `--changes` / `--specs`）
- **那么** 输出一个 JSON 对象，结构如下：
  - `items`：对象数组，包含字段 `{ id: string, type: "change"|"spec", valid: boolean, issues: Issue[], durationMs: number }`
  - `summary`：对象 `{ totals: { items: number, passed: number, failed: number }, byType: { change?: { items: number, passed: number, failed: number }, spec?: { items: number, passed: number, failed: number } } }`
  - `version`：模式的字符串标识符（例如 `"1.0"`）
- **并且** 如果任何 `items[].valid === false`，以退出码 1 退出

其中 `Issue` 遵循现有的逐项验证报告结构 `{ level: "ERROR"|"WARNING"|"INFO", path: string, message: string }`。

#### 场景：显示验证进度

- **当** 验证多个项时（--all、--changes 或 --specs）
- **那么** 显示进度指示器或状态更新
- **并且** 指示当前正在验证哪一项
- **并且** 显示通过/失败项的实时计数

#### 场景：并发限制以提升性能

- **当** 验证多个项时
- **那么** 以有限的并发度运行验证（例如 4-8 个并行）
- **并且** 确保进度指示器保持响应

### 需求：项类型检测和歧义处理

validate 命令应处理歧义名称和显式类型覆盖，以确保清晰、确定性的行为。

#### 场景：直接项验证与自动类型检测

- **当** 执行 `openspec validate <item-name>`
- **那么** 如果 `<item-name>` 唯一匹配一个变更或规范，验证该项

#### 场景：变更和规范名称之间的歧义

- **鉴于** `<item-name>` 同时作为变更和规范存在
- **当** 执行 `openspec validate <item-name>`
- **那么** 打印歧义错误，解释两个匹配项
- **并且** 建议传递 `--type change` 或 `--type spec`，或使用 `openspec change validate` / `openspec spec validate`
- **并且** 以退出码 1 退出，不执行验证

#### 场景：未知项名称

- **当** `<item-name>` 既不匹配变更也不匹配规范
- **那么** 打印未找到错误
- **并且** 在可能时显示最接近的匹配建议
- **并且** 以退出码 1 退出

#### 场景：显式类型覆盖

- **当** 执行 `openspec validate --type change <item>`
- **那么** 将 `<item>` 视为变更 ID 并验证（跳过自动检测）

- **当** 执行 `openspec validate --type spec <item>`
- **那么** 将 `<item>` 视为规范 ID 并验证（跳过自动检测）

### 需求：交互性控制

- CLI 应遵循 `--no-interactive` 以禁用提示。
- CLI 应遵循 `OPEN_SPEC_INTERACTIVE=0` 以全局禁用提示。
- 交互式提示仅应在 stdin 为 TTY 且交互性未被禁用时显示。

#### 场景：通过标志或环境变量禁用提示

- **当** 使用 `--no-interactive` 或环境变量 `OPEN_SPEC_INTERACTIVE=0` 执行 `openspec validate`
- **那么** CLI 应不显示交互式提示
- **并且** 应根据情况打印非交互式提示或选择的输出
