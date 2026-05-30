# cli-artifact-workflow spec

## 目的
用于产物 workflow 操作的 CLI 命令，向用户和 Agent 暴露产物图谱和指令加载器功能。命令是顶级的，以获得流畅的用户体验，并以隔离方式实现以便于移除。

## 新增需求

### 需求：状态命令
系统应显示变更的产物完成状态。

#### 场景：显示所有状态的状态
- **WHEN** 用户运行 `openspec status --change <id>`
- **THEN** 系统显示每个产物及其状态指示器：
 - `[x]` 表示已完成的产物
 - `[ ]]` 表示就绪的产物
 - `[-]` 表示受阻的产物（列出缺失的依赖项）

#### 场景：状态显示完成摘要
- **WHEN** 用户运行 `openspec status --change <id>`
- **THEN** 输出包括完成百分比和计数（例如"2/4 个产物已完成"）

#### 场景：状态 JSON 输出
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 系统输出包含 changeName、schemaName、isComplete 和 artifacts 数组的 JSON

#### 场景：缺失变更参数
- **WHEN** 用户运行 `openspec status` 而不带 `--change`
- **THEN** 系统显示错误并列出可用的变更

#### 场景：未知变更
- **WHEN** 用户运行 `openspec status --change unknown-id`
- **THEN** 系统显示错误，指示该变更不存在

### 需求：下一步命令
系统应显示哪些产物已准备好创建。

#### 场景：显示就绪的产物
- **WHEN** 用户运行 `openspec next --change <id>`
- **THEN** 系统列出所有依赖已满足的产物

#### 场景：没有就绪的产物
- **WHEN** 所有产物要么已完成要么受阻
- **THEN** 系统指示没有就绪的产物（附带说明）

#### 场景：所有产物已完成
- **WHEN** 变更中的所有产物都已完成
- **THEN** 系统指示该变更已完成

#### 场景：Next JSON 输出
- **WHEN** 用户运行 `openspec next --change <id> --json`
- **THEN** 系统输出就绪产物 ID 的 JSON 数组

### 需求：指令命令
系统应输出用于创建产物的增强指令。

#### 场景：显示增强指令
- **WHEN** 用户运行 `openspec instructions <artifact> --change <id>`
- **THEN** 系统输出：
 - 产物元数据（ID、输出路径、描述）
 - template 内容
 - 依赖状态（已完成/缺失）
 - 解锁的产物（完成后变得可用的内容）

#### 场景：指令 JSON 输出
- **WHEN** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **THEN** 系统输出匹配 ArtifactInstructions 接口的 JSON

#### 场景：未知产物
- **WHEN** 用户运行 `openspec instructions unknown-artifact --change <id>`
- **THEN** 系统显示错误，列出该架构的有效产物 ID

#### 场景：依赖未满足的产物
- **WHEN** 用户请求受阻产物的指令
- **THEN** 系统显示指令并附带缺失依赖的警告

### 需求：template 命令
系统应显示架构中所有产物的解析 template 路径。

#### 场景：列出默认架构的 template 路径
- **WHEN** 用户运行 `openspec templates`
- **THEN** 系统使用默认架构显示每个产物及其解析的 template 路径

#### 场景：列出自定义架构的 template 路径
- **WHEN** 用户运行 `openspec templates --schema tdd`
- **THEN** 系统显示指定架构的 template 路径

#### 场景：Templates JSON 输出
- **WHEN** 用户运行 `openspec templates --json`
- **THEN** 系统输出将产物 ID 映射到 template 路径的 JSON

#### 场景：template 解析来源
- **WHEN** 显示 template 路径时
- **THEN** 系统指示每个 template 是来自用户覆盖还是包内置

### 需求：新建变更命令
系统应通过验证创建新的变更目录。

#### 场景：创建有效变更
- **WHEN** 用户运行 `openspec new change add-feature`
- **THEN** 系统创建 `openspec/changes/add-feature/` 目录

#### 场景：无效的变更名称
- **WHEN** 用户使用无效名称运行 `openspec new change "添加功能"`
- **THEN** 系统显示验证错误并附带指导

#### 场景：重复的变更名称
- **WHEN** 用户对现有变更运行 `openspec new change existing-change`
- **THEN** 系统显示错误，指示该变更已存在

#### 场景：带描述创建
- **WHEN** 用户运行 `openspec new change add-feature --description "添加新功能"`
- **THEN** 系统创建变更目录并在 README.md 中包含描述

### 需求：架构选择
系统应支持 workflow 命令的自定义架构选择。

#### 场景：默认架构
- **WHEN** 用户运行 workflow 命令时不带 `--schema`
- **THEN** 系统使用"spec-driven"架构

#### 场景：自定义架构
- **WHEN** 用户运行 `openspec status --change <id> --schema tdd`
- **THEN** 系统使用指定的架构进行产物图谱

#### 场景：未知架构
- **WHEN** 用户指定未知架构
- **THEN** 系统显示错误，列出可用的架构

### 需求：输出格式化
系统应提供一致的输出格式化。

#### 场景：彩色输出
- **WHEN** 终端支持颜色
- **THEN** 状态指示器使用颜色：绿色（已完成）、黄色（就绪）、红色（受阻）

#### 场景：无颜色输出
- **WHEN** 使用 `--no-color` 标志或设置了 NO_COLOR 环境变量
- **THEN** 输出使用纯文本指示器，不带 ANSI 颜色

#### 场景：进度指示
- **WHEN** 加载变更状态需要时间
- **THEN** 系统在加载期间显示旋转指示器

### 需求：实验性隔离
系统应以隔离方式实现产物 workflow 命令，以便于移除。

#### 场景：单文件实现
- **WHEN** 实现产物 workflow 功能时
- **THEN** 所有命令都在 `src/commands/artifact-workflow.ts` 中

#### 场景：帮助文本标记
- **WHEN** 用户在任何产物 workflow 命令上运行 `--help`
- **THEN** 帮助文本指示该命令是实验性的
