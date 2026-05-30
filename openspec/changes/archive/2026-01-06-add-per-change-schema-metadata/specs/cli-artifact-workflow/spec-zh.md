## 新增的需求

### 需求：变更元数据

系统应使用 Zod 模式在 `.openspec.yaml` 文件中存储和验证每个变更的元数据。

#### 场景：创建变更时创建元数据文件

- **当** 用户运行 `openspec new change add-feature --schema tdd`
- **则** 系统在变更目录中创建 `.openspec.yaml`
- **并且** 文件包含 `schema: tdd` 和 `created: <YYYY-MM-DD>`

#### 场景：读取时验证元数据

- **当** 系统读取 `.openspec.yaml`
- **并且** `schema` 字段引用了未知的模式
- **则** 系统显示验证错误，列出可用的模式

#### 场景：元数据模式验证

- **当** `.openspec.yaml` 包含无效的 YAML 或缺少必填字段
- **则** 系统显示包含详细信息的 Zod 验证错误

#### 场景：缺少元数据文件

- **当** 变更目录没有 `.openspec.yaml` 文件
- **则** 系统回退到默认模式（`spec-driven`）

## 已修改的需求

### 需求：新建变更命令

系统应创建新的变更目录，并进行验证和可选的模式元数据。

#### 场景：创建有效变更

- **当** 用户运行 `openspec new change add-feature`
- **则** 系统创建 `openspec/changes/add-feature/` 目录
- **并且** 创建包含 `schema: spec-driven`（默认）的 `.openspec.yaml`

#### 场景：带模式创建变更

- **当** 用户运行 `openspec new change add-feature --schema tdd`
- **则** 系统创建 `openspec/changes/add-feature/` 目录
- **并且** 创建包含 `schema: tdd` 的 `.openspec.yaml`

#### 场景：创建时使用无效模式

- **当** 用户运行 `openspec new change add-feature --schema unknown`
- **则** 系统显示错误，列出可用的模式
- **并且** 不创建变更目录

#### 场景：无效的变更名称

- **当** 用户运行 `openspec new change "Add Feature"` 使用无效名称
- **则** 系统显示验证错误并提供指导

#### 场景：重复的变更名称

- **当** 用户对现有变更运行 `openspec new change existing-change`
- **则** 系统显示错误，指示变更已存在

#### 场景：带描述创建

- **当** 用户运行 `openspec new change add-feature --description "添加新功能"`
- **则** 系统创建变更目录，并在 README.md 中包含描述

### 需求：模式选择

系统应支持工作流命令的自定义模式选择，并从变更元数据自动检测。

#### 场景：从元数据自动检测模式

- **当** 用户运行 `openspec status --change <id>` 而不带 `--schema`
- **并且** 变更的 `.openspec.yaml` 包含 `schema: tdd`
- **则** 系统使用 `tdd` 模式

#### 场景：显式模式覆盖元数据

- **当** 用户运行 `openspec status --change <id> --schema spec-driven`
- **并且** 变更的 `.openspec.yaml` 包含 `schema: tdd`
- **则** 系统使用 `spec-driven`（显式标志优先）

#### 场景：默认模式回退

- **当** 用户运行工作流命令而不带 `--schema`
- **并且** 变更没有 `.openspec.yaml` 文件
- **则** 系统使用 "spec-driven" 模式

#### 场景：通过标志使用自定义模式

- **当** 用户运行 `openspec status --change <id> --schema tdd`
- **则** 系统使用指定的模式作为工件图谱

#### 场景：未知模式

- **当** 用户指定了未知模式
- **则** 系统显示错误，列出可用的模式
