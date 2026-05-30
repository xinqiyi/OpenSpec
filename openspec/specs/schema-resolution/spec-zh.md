# schema-resolution 规范

## 目的
定义项目本地 schema 解析行为，包括优先级顺序（项目本地优先，然后是用户覆盖，最后是包内置）以及在未提供 `projectRoot` 时的向后兼容回退。

## 需求
### 需求：项目本地 schema 解析

当提供了 `projectRoot` 时，系统应从项目本地目录（`./openspec/schemas/<name>/`）以最高优先级解析 schema。

#### 场景：项目本地 schema 优先于用户覆盖
- **WHEN** 名为 "my-workflow" 的 schema 存在于 `./openspec/schemas/my-workflow/schema.yaml`
- **AND** 名为 "my-workflow" 的 schema 存在于 `~/.local/share/openspec/schemas/my-workflow/schema.yaml`
- **AND** 调用 `getSchemaDir("my-workflow", projectRoot)`
- **THEN** 系统应返回项目本地路径

#### 场景：项目本地 schema 优先于包内置
- **WHEN** 名为 "spec-driven" 的 schema 存在于 `./openspec/schemas/spec-driven/schema.yaml`
- **AND** "spec-driven" 是包内置 schema
- **AND** 调用 `getSchemaDir("spec-driven", projectRoot)`
- **THEN** 系统应返回项目本地路径

#### 场景：无项目本地 schema 时回退到用户覆盖
- **WHEN** 在 `./openspec/schemas/my-workflow/` 中没有名为 "my-workflow" 的 schema
- **AND** 名为 "my-workflow" 的 schema 存在于 `~/.local/share/openspec/schemas/my-workflow/schema.yaml`
- **AND** 调用 `getSchemaDir("my-workflow", projectRoot)`
- **THEN** 系统应返回用户覆盖路径

#### 场景：无项目本地或用户 schema 时回退到包内置
- **WHEN** 在 `./openspec/schemas/spec-driven/` 中没有名为 "spec-driven" 的 schema
- **AND** 在 `~/.local/share/openspec/schemas/spec-driven/` 中没有名为 "spec-driven" 的 schema
- **AND** "spec-driven" 是包内置 schema
- **AND** 调用 `getSchemaDir("spec-driven", projectRoot)`
- **THEN** 系统应返回包内置路径

#### 场景：未提供 projectRoot 时的向后兼容
- **WHEN** 调用 `getSchemaDir("my-workflow")` 而不带 `projectRoot` 参数
- **THEN** 系统应仅检查用户覆盖和包内置位置
- **AND** 系统不应检查项目本地位置

### 需求：项目 schemas 目录辅助函数

系统应提供 `getProjectSchemasDir(projectRoot)` 函数，返回项目本地 schemas 目录路径。

#### 场景：返回正确的路径
- **WHEN** 调用 `getProjectSchemasDir("/path/to/project")`
- **THEN** 系统应返回 `/path/to/project/openspec/schemas`

### 需求：列出 schemas 时包含项目本地

如果提供了 `projectRoot`，系统应在列出可用 schemas 时包含项目本地 schemas。

#### 场景：项目本地 schemas 出现在列表中
- **WHEN** 名为 "team-flow" 的 schema 存在于 `./openspec/schemas/team-flow/schema.yaml`
- **AND** 调用 `listSchemas(projectRoot)`
- **THEN** 返回的列表应包含 "team-flow"

#### 场景：项目本地 schema 在列表中覆盖同名用户 schema
- **WHEN** 名为 "custom" 的 schema 同时存在于项目本地和用户覆盖位置
- **AND** 调用 `listSchemas(projectRoot)`
- **THEN** 返回的列表应仅包含 "custom" 一次

#### 场景：listSchemas 的向后兼容
- **WHEN** 调用 `listSchemas()` 而不带 `projectRoot` 参数
- **THEN** 系统应仅包含用户覆盖和包内置 schema

### 需求：Schema 信息包含项目来源

系统应在 `listSchemasWithInfo()` 结果中为项目本地 schema 指示 `source: 'project'`。

#### 场景：项目本地 schema 显示项目来源
- **WHEN** 名为 "team-flow" 的 schema 存在于 `./openspec/schemas/team-flow/schema.yaml`
- **AND** 调用 `listSchemasWithInfo(projectRoot)`
- **THEN** "team-flow" 的 schema 信息应具有 `source: 'project'`

#### 场景：用户覆盖 schema 显示用户来源
- **WHEN** 名为 "my-custom" 的 schema 仅存在于 `~/.local/share/openspec/schemas/my-custom/`
- **AND** 调用 `listSchemasWithInfo(projectRoot)`
- **THEN** "my-custom" 的 schema 信息应具有 `source: 'user'`

#### 场景：包内置 schema 显示包来源
- **WHEN** "spec-driven" 仅作为包内置存在
- **AND** 调用 `listSchemasWithInfo(projectRoot)`
- **THEN** "spec-driven" 的 schema 信息应具有 `source: 'package'`

### 需求：Schemas 命令显示来源

`openspec schemas` 命令应显示每个 schema 的来源。

#### 场景：显示格式包含来源
- **WHEN** 用户运行 `openspec schemas`
- **THEN** 输出应显示每个 schema 及其来源标签（project、user 或 package）

### 需求：使用配置 schema 作为新变更的默认值

当创建新变更时，如果没有指定 `--schema` 标志且没有规划中心默认值适用，系统应使用 `openspec/config.yaml` 中的 schema 字段作为默认值。

#### 场景：不带 --schema 标志且配置存在时创建变更
- **WHEN** 用户运行 `openspec new change foo`，没有规划中心默认值适用，且配置包含 `schema: "tdd"`
- **THEN** 系统使用 schema "tdd" 创建变更

#### 场景：不带 --schema 标志且无配置时创建变更
- **WHEN** 用户运行 `openspec new change foo`，没有规划中心默认值适用，且没有配置文件存在
- **THEN** 系统使用默认 schema "spec-driven" 创建变更

#### 场景：带显式 --schema 标志创建变更
- **WHEN** 用户运行 `openspec new change foo --schema custom` 且配置包含 `schema: "tdd"`
- **THEN** 系统使用 schema "custom" 创建变更（CLI 标志覆盖配置）

### 需求：按更新后的优先级顺序解析 schema

系统应使用以下优先级顺序解析变更的 schema：CLI 标志、变更元数据、规划中心默认值、项目配置、硬编码默认值。

#### 场景：提供了 CLI 标志
- **WHEN** 用户运行命令时使用 `--schema custom`
- **THEN** 系统使用 "custom"，无论变更元数据或配置如何

#### 场景：变更元数据指定了 schema
- **WHEN** 变更的 `.openspec.yaml` 包含 `schema: bound` 且配置包含 `schema: tdd`
- **THEN** 系统使用变更元数据中的 "bound"

#### 场景：规划中心默认值覆盖项目配置
- **WHEN** 没有 CLI 标志或变更元数据，规划中心提供默认 schema `workspace-planning`，且配置包含 `schema: tdd`
- **THEN** 系统使用规划中心默认值中的 "workspace-planning"

#### 场景：仅项目配置指定了 schema
- **WHEN** 没有 CLI 标志、变更元数据或规划中心默认值，但配置包含 `schema: tdd`
- **THEN** 系统使用项目配置中的 "tdd"

#### 场景：任何地方都未指定 schema
- **WHEN** 没有 CLI 标志、变更元数据、规划中心默认值或项目配置
- **THEN** 系统使用硬编码默认值 "spec-driven"

### 需求：支持配置中的项目本地 schema 名称

系统应允许配置的 schema 字段引用在 `openspec/schemas/` 中定义的项目本地 schema。

#### 场景：配置引用项目本地 schema
- **WHEN** 配置包含 `schema: "my-workflow"` 且 `openspec/schemas/my-workflow/` 存在
- **THEN** 系统解析到项目本地 schema

#### 场景：配置引用不存在的 schema
- **WHEN** 配置包含 `schema: "nonexistent"` 且该 schema 不存在
- **THEN** 系统在尝试加载 schema 时显示错误，包含模糊匹配建议和所有有效 schema 的列表

### 需求：为无效 schema 提供有帮助的错误消息

系统应显示 schema 错误，包含模糊匹配建议、可用 schema 列表和修复说明。

#### 场景：Schema 名称拼写错误（接近匹配）
- **WHEN** 配置包含 `schema: "spce-driven"`（拼写错误）
- **THEN** 错误消息包含 "Did you mean: spec-driven (built-in)" 作为建议

#### 场景：Schema 名称没有接近匹配
- **WHEN** 配置包含 `schema: "completely-wrong"`
- **THEN** 错误消息显示所有可用内置和项目本地 schema 的列表

#### 场景：错误消息包含修复说明
- **WHEN** 配置引用了无效 schema
- **THEN** 错误消息包含 "Fix: Edit openspec/config.yaml and change 'schema: X' to a valid schema name"

#### 场景：错误区分内置与项目本地 schema
- **WHEN** 错误列出可用 schema
- **THEN** 输出清晰地标记每个为 "built-in" 或 "project-local"

### 需求：维护现有变更的向后兼容性

系统应继续与没有项目配置的现有变更一起工作。

#### 场景：没有配置的现有变更
- **WHEN** 变更在配置功能之前创建，且没有配置文件存在
- **THEN** 系统使用现有逻辑（变更元数据或硬编码默认值）解析 schema

#### 场景：之后添加配置的现有变更
- **WHEN** 配置文件被添加到包含现有变更的项目中
- **THEN** 现有变更继续使用其来自 `.openspec.yaml` 的绑定 schema

### 需求：工作区规划 schema 解析

Schema 解析应支持内置的工作区规划 schema。

#### 场景：列出工作区规划 schema
- **WHEN** 用户运行 `openspec schemas`
- **THEN** 输出应包含 `workspace-planning`
- **AND** 除非被更高优先级的 schema 覆盖，否则应将其标识为包提供的 schema

#### 场景：按名称解析工作区规划 schema
- **WHEN** 工作流命令请求 schema `workspace-planning`
- **THEN** schema 解析应使用正常的项目、用户、然后包的优先级顺序进行解析

#### 场景：新变更的工作区默认 schema
- **GIVEN** 命令在工作区规划中心创建一个变更
- **AND** 用户未传递显式的 `--schema`
- **AND** 没有变更元数据 schema 适用于新变更
- **WHEN** OpenSpec 为新变更解析 schema
- **THEN** 它应使用规划中心默认 schema `workspace-planning`
- **AND** 它应在任何项目或全局配置 schema 值之前使用该规划中心默认值

#### 场景：工作区变更的显式 schema 覆盖
- **GIVEN** 命令在工作区规划中心创建一个变更
- **WHEN** 用户传递显式的 `--schema <name>`
- **THEN** OpenSpec 应使用显式请求的 schema
- **AND** 它应使用正常的 schema 解析验证该 schema
