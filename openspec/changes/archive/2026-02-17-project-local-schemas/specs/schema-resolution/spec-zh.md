## 新增的需求

### 需求：项目本地模式解析

系统应从项目本地目录（`./openspec/schemas/<name>/`）解析模式，当提供 `projectRoot` 时具有最高优先级。

#### 场景：项目本地模式优先于用户覆盖
- **当** 名为 "my-workflow" 的模式存在于 `./openspec/schemas/my-workflow/schema.yaml`
- **并且** 名为 "my-workflow" 的模式存在于 `~/.local/share/openspec/schemas/my-workflow/schema.yaml`
- **并且** 调用 `getSchemaDir("my-workflow", projectRoot)`
- **则** 系统应返回项目本地路径

#### 场景：项目本地模式优先于包内置模式
- **当** 名为 "spec-driven" 的模式存在于 `./openspec/schemas/spec-driven/schema.yaml`
- **并且** "spec-driven" 是包内置模式
- **并且** 调用 `getSchemaDir("spec-driven", projectRoot)`
- **则** 系统应返回项目本地路径

#### 场景：无项目本地模式时回退到用户覆盖
- **当** 名为 "my-workflow" 的模式在 `./openspec/schemas/my-workflow/` 不存在
- **并且** 名为 "my-workflow" 的模式存在于 `~/.local/share/openspec/schemas/my-workflow/schema.yaml`
- **并且** 调用 `getSchemaDir("my-workflow", projectRoot)`
- **则** 系统应返回用户覆盖路径

#### 场景：无项目本地或用户模式时回退到包内置模式
- **当** 名为 "spec-driven" 的模式在 `./openspec/schemas/spec-driven/` 不存在
- **并且** 名为 "spec-driven" 的模式在 `~/.local/share/openspec/schemas/spec-driven/` 不存在
- **并且** "spec-driven" 是包内置模式
- **并且** 调用 `getSchemaDir("spec-driven", projectRoot)`
- **则** 系统应返回包内置路径

#### 场景：未提供 projectRoot 时的向后兼容性
- **当** 调用 `getSchemaDir("my-workflow")` 时不带 `projectRoot` 参数
- **则** 系统仅检查用户覆盖和包内置位置
- **并且** 系统不应检查项目本地位置

### 需求：项目模式目录辅助函数

系统应提供一个 `getProjectSchemasDir(projectRoot)` 函数，返回项目本地模式目录路径。

#### 场景：返回正确的路径
- **当** 调用 `getProjectSchemasDir("/path/to/project")`
- **则** 系统应返回 `/path/to/project/openspec/schemas`

### 需求：列出模式时包含项目本地模式

系统应在提供 `projectRoot` 时在列出可用模式中包含项目本地模式。

#### 场景：项目本地模式出现在列表中
- **当** 名为 "team-flow" 的模式存在于 `./openspec/schemas/team-flow/schema.yaml`
- **并且** 调用 `listSchemas(projectRoot)`
- **则** 返回的列表应包含 "team-flow"

#### 场景：项目本地模式在列表中覆盖同名用户模式
- **当** 名为 "custom" 的模式同时存在于项目本地和用户覆盖位置
- **并且** 调用 `listSchemas(projectRoot)`
- **则** 返回的列表应仅包含一次 "custom"

#### 场景：listSchemas 的向后兼容性
- **当** 调用 `listSchemas()` 时不带 `projectRoot` 参数
- **则** 系统应仅包含用户覆盖和包内置模式

### 需求：模式信息包含项目来源

系统应在 `listSchemasWithInfo()` 结果中为项目本地模式指示 `source: 'project'`。

#### 场景：项目本地模式显示项目来源
- **当** 名为 "team-flow" 的模式存在于 `./openspec/schemas/team-flow/schema.yaml`
- **并且** 调用 `listSchemasWithInfo(projectRoot)`
- **则** "team-flow" 的模式信息应具有 `source: 'project'`

#### 场景：用户覆盖模式显示用户来源
- **当** 名为 "my-custom" 的模式仅存在于 `~/.local/share/openspec/schemas/my-custom/`
- **并且** 调用 `listSchemasWithInfo(projectRoot)`
- **则** "my-custom" 的模式信息应具有 `source: 'user'`

#### 场景：包内置模式显示包来源
- **当** "spec-driven" 仅作为包内置模式存在
- **并且** 调用 `listSchemasWithInfo(projectRoot)`
- **则** "spec-driven" 的模式信息应具有 `source: 'package'`

### 需求：schemas 命令显示来源

`openspec schemas` 命令应显示每个模式的来源。

#### 场景：显示格式包含来源
- **当** 用户运行 `openspec schemas`
- **则** 输出应显示每个模式及其来源标签（项目、用户或包）
