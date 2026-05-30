## 新增的需求

### 需求：模式验证检查模式结构

CLI 应提供 `openspec schema validate [name]` 命令，用于验证模式配置并报告错误。

#### 场景：验证特定模式
- **当** 用户运行 `openspec schema validate my-workflow`
- **则** 系统按解析顺序定位模式
- **并且** 根据模式 Zod 类型验证 `schema.yaml`
- **并且** 显示验证结果（有效或错误列表）

#### 场景：验证所有项目模式
- **当** 用户运行 `openspec schema validate` 不带名称
- **则** 系统验证 `openspec/schemas/` 中的所有模式
- **并且** 显示每个模式的验证结果
- **并且** 如果任何模式无效，以非零码退出

#### 场景：未找到模式
- **当** 用户运行 `openspec schema validate nonexistent`
- **则** 系统显示未找到模式的错误
- **并且** 以非零码退出

### 需求：模式验证检查 YAML 语法

CLI 应在可能时报告带有行号的 YAML 解析错误。

#### 场景：无效的 YAML 语法
- **当** 用户运行 `openspec schema validate my-workflow` 且 `schema.yaml` 有语法错误
- **则** 系统显示带有行号的 YAML 解析错误
- **并且** 以非零码退出

#### 场景：YAML 有效但缺少必填字段
- **当** `schema.yaml` 是有效的 YAML 但缺少 `name` 字段
- **则** 系统为缺失的必填字段显示 Zod 验证错误
- **并且** 标识具体缺失的字段

### 需求：模式验证检查模板存在性

CLI 应验证工件引用的所有模板文件是否存在。

#### 场景：缺失模板文件
- **当** 工件引用 `template: proposal.md` 但文件在模式目录中不存在
- **则** 系统报告错误："未找到工件 'proposal' 的模板文件 'proposal.md'"
- **并且** 以非零码退出

#### 场景：所有模板存在
- **当** 所有工件模板都存在
- **则** 系统报告模板有效
- **并且** 模板存在性包含在验证摘要中

### 需求：模式验证检查依赖关系图

CLI 应验证工件依赖关系是否形成有效的有向无环图。

#### 场景：有效的依赖关系图
- **当** 工件依赖关系形成有效的 DAG（例如 tasks -> specs -> proposal）
- **则** 系统报告依赖关系图有效

#### 场景：检测到循环依赖
- **当** 工件 A 需要 B 且工件 B 需要 A
- **则** 系统报告循环依赖错误
- **并且** 标识循环中涉及的工件
- **并且** 以非零码退出

#### 场景：未知的依赖引用
- **当** 工件需要 `nonexistent-artifact`
- **则** 系统报告错误："工件 'x' 需要未知的工件 'nonexistent-artifact'"
- **并且** 以非零码退出

### 需求：模式验证输出 JSON 格式

CLI 应支持 `--json` 标志，用于机器可读的验证结果。

#### 场景：有效模式的 JSON 输出
- **当** 用户运行 `openspec schema validate my-workflow --json` 且模式有效
- **则** 系统输出包含 `valid: true`、`name` 和 `path` 字段的 JSON

#### 场景：无效模式的 JSON 输出
- **当** 用户运行 `openspec schema validate my-workflow --json` 且模式有错误
- **则** 系统输出包含 `valid: false` 和 `issues` 数组的 JSON
- **并且** 每个问题包含 `level`、`path` 和 `message` 字段
- **并且** 格式与现有 `openspec validate` 输出结构匹配

### 需求：模式验证支持详细模式

CLI 应支持 `--verbose` 标志，用于详细的验证信息。

#### 场景：详细输出显示所有检查
- **当** 用户运行 `openspec schema validate my-workflow --verbose`
- **则** 系统在运行时显示每个验证检查
- **并且** 显示以下各项的通过/失败状态：YAML 解析、Zod 验证、模板存在性、依赖关系图
