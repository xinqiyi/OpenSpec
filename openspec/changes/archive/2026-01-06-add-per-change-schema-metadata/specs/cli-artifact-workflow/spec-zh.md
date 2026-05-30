## 新增的需求

### 需求：变更元数据

系统应使用 Zod schema 在 `.openspec.yaml` 文件中存储和验证每个变更的元数据。

#### 场景：创建变更时创建元数据文件

- **WHEN** 用户运行 `openspec new change add-feature --schema tdd`
- **THEN** 系统在变更目录中创建 `.openspec.yaml`
- **AND** 文件包含 `schema: tdd` 和 `created: <YYYY-MM-DD>`

#### 场景：读取时验证元数据

- **WHEN** 系统读取 `.openspec.yaml`
- **AND** `schema` 字段引用了未知的 schema
- **THEN** 系统显示验证错误，列出可用的 schema

#### 场景：元数据 schema 验证

- **WHEN** `.openspec.yaml` 包含无效的 YAML 或缺少必填字段
- **THEN** 系统显示包含详细信息的 Zod 验证错误

#### 场景：缺少元数据文件

- **WHEN** 变更目录没有 `.openspec.yaml` 文件
- **THEN** 系统回退到默认 schema（`spec-driven`）

## 已修改的需求

### 需求：新建变更命令

系统应创建新的变更目录，并进行验证和可选的 schema 元数据。

#### 场景：创建有效变更

- **WHEN** 用户运行 `openspec new change add-feature`
- **THEN** 系统创建 `openspec/changes/add-feature/` 目录
- **AND** 创建包含 `schema: spec-driven`（默认）的 `.openspec.yaml`

#### 场景：带 schema 创建变更

- **WHEN** 用户运行 `openspec new change add-feature --schema tdd`
- **THEN** 系统创建 `openspec/changes/add-feature/` 目录
- **AND** 创建包含 `schema: tdd` 的 `.openspec.yaml`

#### 场景：创建时使用无效 schema

- **WHEN** 用户运行 `openspec new change add-feature --schema unknown`
- **THEN** 系统显示错误，列出可用的 schema
- **AND** 不创建变更目录

#### 场景：无效的变更名称

- **WHEN** 用户运行 `openspec new change "Add Feature"` 使用无效名称
- **THEN** 系统显示验证错误并提供指导

#### 场景：重复的变更名称

- **WHEN** 用户对现有变更运行 `openspec new change existing-change`
- **THEN** 系统显示错误，指示变更已存在

#### 场景：带描述创建

- **WHEN** 用户运行 `openspec new change add-feature --description "添加新功能"`
- **THEN** 系统创建变更目录，并在 README.md 中包含描述

### 需求：schema 选择

系统应支持 workflow 命令的自定义 schema 选择，并从变更元数据自动检测。

#### 场景：从元数据自动检测 schema

- **WHEN** 用户运行 `openspec status --change <id>` 而不带 `--schema`
- **AND** 变更的 `.openspec.yaml` 包含 `schema: tdd`
- **THEN** 系统使用 `tdd` schema

#### 场景：显式 schema 覆盖元数据

- **WHEN** 用户运行 `openspec status --change <id> --schema spec-driven`
- **AND** 变更的 `.openspec.yaml` 包含 `schema: tdd`
- **THEN** 系统使用 `spec-driven`（显式标志优先）

#### 场景：默认 schema 回退

- **WHEN** 用户运行 workflow 命令而不带 `--schema`
- **AND** 变更没有 `.openspec.yaml` 文件
- **THEN** 系统使用 "spec-driven" schema

#### 场景：通过标志使用自定义 schema

- **WHEN** 用户运行 `openspec status --change <id> --schema tdd`
- **THEN** 系统使用指定的 schema 作为 artifact 图谱

#### 场景：未知 schema

- **WHEN** 用户指定了未知 schema
- **THEN** 系统显示错误，列出可用的 schema
