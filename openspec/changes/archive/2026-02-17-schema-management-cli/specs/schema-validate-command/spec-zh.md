## 新增的需求

### 需求：schema 验证检查 schema 结构

CLI 应提供 `openspec schema validate [name]` 命令，用于验证 schema 配置并报告错误。

#### 场景：验证特定 schema
- **WHEN** 用户运行 `openspec schema validate my-workflow`
- **THEN** 系统按解析顺序定位 schema
- **AND** 根据 schema Zod 类型验证 `schema.yaml`
- **AND** 显示验证结果（有效或错误列表）

#### 场景：验证所有项目 schema
- **WHEN** 用户运行 `openspec schema validate` 不带名称
- **THEN** 系统验证 `openspec/schemas/` 中的所有 schema
- **AND** 显示每个 schema 的验证结果
- **AND** 如果任何 schema 无效，以非零码退出

#### 场景：未找到 schema
- **WHEN** 用户运行 `openspec schema validate nonexistent`
- **THEN** 系统显示未找到 schema 的错误
- **AND** 以非零码退出

### 需求：schema 验证检查 YAML 语法

CLI 应在可能时报告带有行号的 YAML 解析错误。

#### 场景：无效的 YAML 语法
- **WHEN** 用户运行 `openspec schema validate my-workflow` 且 `schema.yaml` 有语法错误
- **THEN** 系统显示带有行号的 YAML 解析错误
- **AND** 以非零码退出

#### 场景：YAML 有效但缺少必填字段
- **WHEN** `schema.yaml` 是有效的 YAML 但缺少 `name` 字段
- **THEN** 系统为缺失的必填字段显示 Zod 验证错误
- **AND** 标识具体缺失的字段

### 需求：schema 验证检查 template 存在性

CLI 应验证 artifact 引用的所有 template 文件是否存在。

#### 场景：缺失 template 文件
- **WHEN** artifact 引用 `template: proposal.md` 但文件在 schema 目录中不存在
- **THEN** 系统报告错误："未找到 artifact 'proposal' 的 template 文件 'proposal.md'"
- **AND** 以非零码退出

#### 场景：所有 template 存在
- **WHEN** 所有 artifact template 都存在
- **THEN** 系统报告 template 有效
- **AND** template 存在性包含在验证摘要中

### 需求：schema 验证检查依赖关系图

CLI 应验证 artifact 依赖关系是否形成有效的有向无环图。

#### 场景：有效的依赖关系图
- **WHEN** artifact 依赖关系形成有效的 DAG（例如 tasks -> specs -> proposal）
- **THEN** 系统报告依赖关系图有效

#### 场景：检测到循环依赖
- **WHEN** artifact A 需要 B 且 artifact B 需要 A
- **THEN** 系统报告循环依赖错误
- **AND** 标识循环中涉及的 artifact
- **AND** 以非零码退出

#### 场景：未知的依赖引用
- **WHEN** artifact 需要 `nonexistent-artifact`
- **THEN** 系统报告错误："artifact 'x' 需要未知的 artifact 'nonexistent-artifact'"
- **AND** 以非零码退出

### 需求：schema 验证输出 JSON 格式

CLI 应支持 `--json` 标志，用于机器可读的验证结果。

#### 场景：有效 schema 的 JSON 输出
- **WHEN** 用户运行 `openspec schema validate my-workflow --json` 且 schema 有效
- **THEN** 系统输出包含 `valid: true`、`name` 和 `path` 字段的 JSON

#### 场景：无效 schema 的 JSON 输出
- **WHEN** 用户运行 `openspec schema validate my-workflow --json` 且 schema 有错误
- **THEN** 系统输出包含 `valid: false` 和 `issues` 数组的 JSON
- **AND** 每个问题包含 `level`、`path` 和 `message` 字段
- **AND** 格式与现有 `openspec validate` 输出结构匹配

### 需求：schema 验证支持详细 schema

CLI 应支持 `--verbose` 标志，用于详细的验证信息。

#### 场景：详细输出显示所有检查
- **WHEN** 用户运行 `openspec schema validate my-workflow --verbose`
- **THEN** 系统在运行时显示每个验证检查
- **AND** 显示以下各项的通过/失败状态：YAML 解析、Zod 验证、template 存在性、依赖关系图
