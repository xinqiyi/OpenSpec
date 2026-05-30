## 新增的需求

### 需求：项目本地 schema 解析

系统应从项目本地目录（`./openspec/schemas/<name>/`）解析 schema，当提供 `projectRoot` 时具有最高优先级。

#### 场景：项目本地 schema 优先于用户覆盖
- **WHEN** 名为 "my-workflow" 的 schema 存在于 `./openspec/schemas/my-workflow/schema.yaml`
- **AND** 名为 "my-workflow" 的 schema 存在于 `~/.local/share/openspec/schemas/my-workflow/schema.yaml`
- **AND** 调用 `getSchemaDir("my-workflow", projectRoot)`
- **THEN** 系统应返回项目本地路径

#### 场景：项目本地 schema 优先于包内置 schema
- **WHEN** 名为 "spec-driven" 的 schema 存在于 `./openspec/schemas/spec-driven/schema.yaml`
- **AND** "spec-driven" 是包内置 schema
- **AND** 调用 `getSchemaDir("spec-driven", projectRoot)`
- **THEN** 系统应返回项目本地路径

#### 场景：无项目本地 schema 时回退到用户覆盖
- **WHEN** 名为 "my-workflow" 的 schema 在 `./openspec/schemas/my-workflow/` 不存在
- **AND** 名为 "my-workflow" 的 schema 存在于 `~/.local/share/openspec/schemas/my-workflow/schema.yaml`
- **AND** 调用 `getSchemaDir("my-workflow", projectRoot)`
- **THEN** 系统应返回用户覆盖路径

#### 场景：无项目本地或用户 schema 时回退到包内置 schema
- **WHEN** 名为 "spec-driven" 的 schema 在 `./openspec/schemas/spec-driven/` 不存在
- **AND** 名为 "spec-driven" 的 schema 在 `~/.local/share/openspec/schemas/spec-driven/` 不存在
- **AND** "spec-driven" 是包内置 schema
- **AND** 调用 `getSchemaDir("spec-driven", projectRoot)`
- **THEN** 系统应返回包内置路径

#### 场景：未提供 projectRoot 时的向后兼容性
- **WHEN** 调用 `getSchemaDir("my-workflow")` 时不带 `projectRoot` 参数
- **THEN** 系统仅检查用户覆盖和包内置位置
- **AND** 系统不应检查项目本地位置

### 需求：项目 schema 目录辅助函数

系统应提供一个 `getProjectSchemasDir(projectRoot)` 函数，返回项目本地 schema 目录路径。

#### 场景：返回正确的路径
- **WHEN** 调用 `getProjectSchemasDir("/path/to/project")`
- **THEN** 系统应返回 `/path/to/project/openspec/schemas`

### 需求：列出 schema 时包含项目本地 schema

系统应在提供 `projectRoot` 时在列出可用 schema 中包含项目本地 schema。

#### 场景：项目本地 schema 出现在列表中
- **WHEN** 名为 "team-flow" 的 schema 存在于 `./openspec/schemas/team-flow/schema.yaml`
- **AND** 调用 `listSchemas(projectRoot)`
- **THEN** 返回的列表应包含 "team-flow"

#### 场景：项目本地 schema 在列表中覆盖同名用户 schema
- **WHEN** 名为 "custom" 的 schema 同时存在于项目本地和用户覆盖位置
- **AND** 调用 `listSchemas(projectRoot)`
- **THEN** 返回的列表应仅包含一次 "custom"

#### 场景：listSchemas 的向后兼容性
- **WHEN** 调用 `listSchemas()` 时不带 `projectRoot` 参数
- **THEN** 系统应仅包含用户覆盖和包内置 schema

### 需求：schema 信息包含项目来源

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
- **WHEN** "spec-driven" 仅作为包内置 schema 存在
- **AND** 调用 `listSchemasWithInfo(projectRoot)`
- **THEN** "spec-driven" 的 schema 信息应具有 `source: 'package'`

### 需求：schemas 命令显示来源

`openspec schemas` 命令应显示每个 schema 的来源。

#### 场景：显示格式包含来源
- **WHEN** 用户运行 `openspec schemas`
- **THEN** 输出应显示每个 schema 及其来源标签（项目、用户或包）
