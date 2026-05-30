# spec：带配置的 schema 解析

## 新增的需求

### 需求：使用配置 schema 作为新变更的默认值

系统应在创建新变更时且在未提供显式 `--schema` 标志的情况下，使用 `openspec/config.yaml` 中的 schema 字段作为默认值。

#### 场景：不带 --schema 标志创建变更且配置存在
- **WHEN** 用户运行 `openspec new change foo` 且配置包含 `schema: "tdd"`
- **THEN** 系统使用 schema "tdd" 创建变更

#### 场景：不带 --schema 标志创建变更且无配置
- **WHEN** 用户运行 `openspec new change foo` 且不存在配置文件
- **THEN** 系统使用默认 schema "spec-driven" 创建变更

#### 场景：带显式 --schema 标志创建变更
- **WHEN** 用户运行 `openspec new change foo --schema custom` 且配置包含 `schema: "tdd"`
- **THEN** 系统使用 schema "custom" 创建变更（CLI 标志覆盖配置）

### 需求：使用更新的优先级顺序解析 schema

系统应按照以下优先级顺序解析变更的 schema：CLI 标志、变更元数据、项目配置、硬编码默认值。

#### 场景：提供了 CLI 标志
- **WHEN** 用户使用 `--schema custom` 运行命令
- **THEN** 系统使用 "custom"，无论变更元数据或配置如何

#### 场景：变更元数据指定 schema
- **WHEN** 变更的 `.openspec.yaml` 包含 `schema: bound` 且配置包含 `schema: tdd`
- **THEN** 系统使用来自变更元数据的 "bound"

#### 场景：仅项目配置指定 schema
- **WHEN** 没有 CLI 标志或变更元数据，但配置包含 `schema: tdd`
- **THEN** 系统使用来自项目配置的 "tdd"

#### 场景：任何地方都未指定 schema
- **WHEN** 没有 CLI 标志、变更元数据或项目配置
- **THEN** 系统使用硬编码默认值 "spec-driven"

### 需求：支持配置中的项目本地 schema 名称

系统应允许配置中的 schema 字段引用 `openspec/schemas/` 中定义的项目本地 schema。

#### 场景：配置引用项目本地 schema
- **WHEN** 配置包含 `schema: "my-workflow"` 且 `openspec/schemas/my-workflow/` 存在
- **THEN** 系统解析为项目本地 schema

#### 场景：配置引用不存在的 schema
- **WHEN** 配置包含 `schema: "nonexistent"` 且该 schema 不存在
- **THEN** 系统在尝试加载 schema 时显示错误，带有模糊匹配建议和所有有效 schema 列表

### 需求：为无效 schema 提供有帮助的错误消息

系统应显示带有模糊匹配建议、可用 schema 列表和修复说明的 schema 错误。

#### 场景：schema 名称有拼写错误（接近匹配）
- **WHEN** 配置包含 `schema: "spce-driven"`（拼写错误）
- **THEN** 错误消息包含 "您是不是想找：spec-driven (built-in)" 作为建议

#### 场景：schema 名称无接近匹配
- **WHEN** 配置包含 `schema: "completely-wrong"`
- **THEN** 错误消息显示所有可用的内置和项目本地 schema 列表

#### 场景：错误消息包含修复说明
- **WHEN** 配置引用无效 schema
- **THEN** 错误消息包含 "修复：编辑 openspec/config.yaml 并将 'schema: X' 改为有效的 schema 名称"

#### 场景：错误区分内置与项目本地 schema
- **WHEN** 错误列出可用 schema
- **THEN** 输出清晰地将每个标记为 "built-in" 或 "project-local"

### 需求：保持现有变更的向后兼容性

系统应继续适用于没有项目配置的现有变更。

#### 场景：无配置的现有变更
- **WHEN** 变更是在配置功能之前创建的，且不存在配置文件
- **THEN** 系统使用现有逻辑解析 schema（变更元数据或硬编码默认值）

#### 场景：稍后添加配置的现有变更
- **WHEN** 在项目已存在变更的情况下添加配置文件
- **THEN** 现有变更继续使用其来自 `.openspec.yaml` 的绑定 schema
