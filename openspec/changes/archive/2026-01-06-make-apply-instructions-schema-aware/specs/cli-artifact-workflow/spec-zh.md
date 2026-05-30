## 新增需求

### 需求：Schema Apply 块

系统应在模式定义中支持 `apply` 块，控制实现何时及如何开始。

#### 场景：带有 apply 块的模式

- **当** 模式定义了 `apply` 块
- **那么** 系统使用 `apply.requires` 确定在 apply 之前必须存在哪些工件
- **并且** 使用 `apply.tracks` 标识进度跟踪文件（如果为 null 则不跟踪）
- **并且** 使用 `apply.instruction` 作为向 agent 显示的指导

#### 场景：没有 apply 块的模式

- **当** 模式没有 `apply` 块
- **那么** 系统要求所有工件都存在，然后 apply 才可用
- **并且** 使用默认指令："所有工件已完成。继续实现。"

### 需求：Apply 指令命令

系统应通过 `openspec instructions apply` 生成感知模式的 apply 指令。

#### 场景：生成 apply 指令

- **当** 用户运行 `openspec instructions apply --change <id>`
- **并且** 所有必需的工件（根据模式的 `apply.requires`）都存在
- **那么** 系统输出：
  - 来自所有现有工件的上下文文件
  - 模式特定的指令文本
  - 进度跟踪文件路径（如果设置了 `apply.tracks`）

#### 场景：因缺少工件而被阻塞的 Apply

- **当** 用户运行 `openspec instructions apply --change <id>`
- **并且** 必需的工件缺失
- **那么** 系统指示 apply 被阻塞
- **并且** 列出必须首先创建的工件

#### 场景：Apply 指令 JSON 输出

- **当** 用户运行 `openspec instructions apply --change <id> --json`
- **那么** 系统输出包含以下内容的 JSON：
  - `contextFiles`：现有工件的路径数组
  - `instruction`：apply 指令文本
  - `tracks`：进度文件路径或 null
  - `applyRequires`：必需的工件 ID 列表

## 修改后的需求

### 需求：Status 命令

系统应显示变更的工件完成状态，包括 apply 就绪状态。

#### 场景：状态 JSON 包含 apply 要求

- **当** 用户运行 `openspec status --change <id> --json`
- **那么** 系统输出包含以下内容的 JSON：
  - `changeName`、`schemaName`、`isComplete`、`artifacts` 数组
  - `applyRequires`：apply 阶段所需的工件 ID 数组
