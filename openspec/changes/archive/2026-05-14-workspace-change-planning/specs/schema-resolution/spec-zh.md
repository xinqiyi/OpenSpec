## 新增需求

### 需求：workspace planning schema 解析
schema 解析应支持内置的 workspace planning schema。

#### 场景：列出 workspace planning schema
- **WHEN** 用户运行 `openspec schemas` 时
- **THEN** 输出应包含 `workspace-planning`
- **AND** 除非被更高优先级的 schema 覆盖，否则应将其标识为包提供的 schema

#### 场景：按名称解析 workspace planning schema
- **WHEN** workflow 命令请求 `workspace-planning` schema 时
- **THEN** schema 解析应按照正常的项目、用户再到包的优先级顺序进行解析

#### 场景：新变更的默认 workspace schema
- **GIVEN** 命令在 workspace planning 中心创建变更
- **AND** 用户未传递显式的 `--schema`
- **WHEN** OpenSpec 为新变更解析 schema 时
- **THEN** 应使用 `workspace-planning` 作为默认 schema

#### 场景：workspace 变更的显式 schema 覆盖
- **GIVEN** 命令在 workspace planning 中心创建变更
- **WHEN** 用户传递显式的 `--schema <名称>` 时
- **THEN** OpenSpec 应使用显式请求的 schema
- **AND** 应使用正常的 schema 解析来验证该 schema
