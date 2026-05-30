## 新增需求

### 需求：可识别的 workspace 中心
OpenSpec 应为用户和 agent 提供一个可识别的 workspace 中心，用于跨 repository planning。

#### 场景：跨链接 repository 或文件夹进行 planning
- **WHEN** 用户为其 planning 的 repository 或文件夹创建 OpenSpec workspace
- **THEN** workspace 应提供一个持久化的 planning 中心
- **AND** workspace 应能够随时间持有多个变更

#### 场景：从 workspace 内部工作
- **GIVEN** 用户从 workspace 根目录或其子目录之一运行 OpenSpec
- **WHEN** OpenSpec 解析当前 workspace
- **THEN** 它应识别 workspace 根目录
- **AND** 它应使用 workspace 根目录的 `changes/` 目录作为 workspace planning 区域

#### 场景：避免意外的 workspace schema
- **GIVEN** 一个目录有 `changes/` 但不是一个 OpenSpec workspace
- **WHEN** OpenSpec 解析当前 workspace
- **THEN** 它应避免将该目录视为 workspace
- **AND** 仅当 workspace 标识文件存在时才进入 workspace schema

### 需求：稳定的 workspace 名称
OpenSpec 应在 workspace 标识、托管存储和本地注册表中使用一个文件夹风格的 workspace 名称。

#### 场景：使用一个 workspace 名称
- **WHEN** OpenSpec 创建或注册一个托管 workspace
- **THEN** workspace 名称应存储在 `.openspec-workspace/workspace.yaml` 中
- **AND** 相同的名称应作为默认的托管 workspace 文件夹名称
- **AND** 相同的名称应作为本地注册表名称

#### 场景：拒绝无效的文件夹风格名称
- **WHEN** OpenSpec 接受一个 workspace 名称
- **THEN** 它应拒绝空名称、`.` 或 `..`，以及包含路径分隔符的名称
- **AND** setup 或 create 流程应清晰地报告操作系统级别的文件夹创建失败

### 需求：专用 workspace 标识
OpenSpec 应区分协调 workspace 和 repository 本地的 OpenSpec 项目。

#### 场景：读取 workspace 标识
- **WHEN** OpenSpec 读取或写入 workspace 标识和 workspace 状态
- **THEN** 它应使用 `.openspec-workspace/`

#### 场景：保留 repository 本地的 OpenSpec 项目
- **GIVEN** repository 本地的 OpenSpec 项目使用 `openspec/`
- **WHEN** 该 repository 被链接到一个 workspace
- **THEN** OpenSpec 应继续将 `openspec/` 视为该 repository 的本地 OpenSpec 目录
- **AND** workspace planning 应保持锚定在 workspace 根目录

#### 场景：避免在 workspace 根目录进行 repository 本地初始化
- **WHEN** 用户从 OpenSpec workspace 根目录工作
- **THEN** OpenSpec 应将该根目录视为 workspace 协调界面
- **AND** 用户无需在 workspace 根目录内初始化 repository 本地的 `openspec/` 项目

### 需求：安全的 workspace 共享
OpenSpec 应将共享 workspace 信息与本地机器路径分开保存。

#### 场景：共享 workspace planning
- **WHEN** workspace 与另一个用户或机器共享
- **THEN** 共享 workspace 信息应包括可移植的 workspace 标识和稳定的链接名称
- **AND** 不应要求其他用户重用原始用户的绝对检出路径

#### 场景：保持检出路径本地化
- **WHEN** OpenSpec 存储 workspace 的本地路径
- **THEN** 这些路径应被视为当前机器和运行时的本地路径
- **AND** 另一台机器可以将相同的链接名称映射到不同的本地路径

#### 场景：保留运行时本地路径
- **WHEN** OpenSpec 读取或写入本地 workspace 路径
- **THEN** 它应保留对当前运行时有效的路径字符串
- **AND** 它应支持原生 Windows 路径和 WSL2/Linux 路径作为本地状态值

#### 场景：从可移植协作中排除本地状态
- **WHEN** OpenSpec 创建一个 workspace
- **THEN** 它应默认从可移植协作状态中排除 `.openspec-workspace/local.yaml`
- **AND** `.openspec-workspace/workspace.yaml` 应保持为可移植的 workspace 标识和链接名称状态

### 需求：标准 workspace 位置
OpenSpec 应使用标准位置存储 OpenSpec 托管的 workspace，无需大多数用户自行选择。

#### 场景：使用标准 workspace 位置
- **WHEN** OpenSpec 需要 OpenSpec 托管 workspace 的位置
- **THEN** 它应使用 `<global-data-dir>/workspaces`
- **AND** `<global-data-dir>` 应遵循现有的 OpenSpec XDG 和平台数据目录行为

#### 场景：避免 workspace 特定的存储覆盖
- **WHEN** OpenSpec 解析 OpenSpec 托管 workspace 的位置
- **THEN** 在此切片中，它不应使用 workspace 特定的环境变量、命令或配置设置
- **AND** 托管 workspace 存储应保持在 `<global-data-dir>/workspaces` 下

#### 场景：从原生 Windows 运行
- **WHEN** OpenSpec 从原生 Windows shell（如 PowerShell）运行
- **AND** 未设置 `XDG_DATA_HOME`
- **THEN** OpenSpec 应将托管 workspace 存储在 Windows 全局数据位置下
- **AND** 路径应遵循原生 Windows 路径行为

#### 场景：从 WSL2 运行
- **WHEN** OpenSpec 从 WSL2 运行
- **THEN** OpenSpec 应将托管 workspace 存储在 WSL 内的 Linux/XDG 数据位置下
- **AND** WSL 内的路径应遵循 Linux 路径行为

#### 场景：自动使用 workspace 位置
- **WHEN** OpenSpec 在后续 workflow 中创建或解析 OpenSpec 托管 workspace
- **THEN** 它应默认使用已解析的 workspace 位置
- **AND** 用户应能够遵循正常的 workspace 流程而无需选择存储位置

#### 场景：显示 workspace 路径
- **WHEN** OpenSpec 在标准 workspace 位置创建一个 workspace
- **THEN** 它应向用户报告 workspace 路径
- **AND** 它不应隐藏 planning 文件的创建位置

#### 场景：保持在当前运行时
- **WHEN** OpenSpec 解析 workspace 路径或本地 repository 路径
- **THEN** 它应为运行 OpenSpec 的运行时解释路径
- **AND** Windows、UNC WSL 和 WSL 挂载路径应保持为显式用户提供的路径

### 需求：本地 workspace 注册表
OpenSpec 应在当前机器上维护一个轻量级的已知 workspace 本地注册表。

#### 场景：记录已知 workspace
- **WHEN** OpenSpec 创建或了解到一个托管 workspace
- **THEN** 它应能够将 workspace 名称和路径记录在本地注册表中
- **AND** 注册表应是机器本地状态

#### 场景：保持 workspace 文件夹的权威性
- **WHEN** OpenSpec 读取 workspace 详细信息
- **THEN** 每个 workspace 文件夹的 `.openspec-workspace/workspace.yaml` 应保持为该 workspace 的真相来源
- **AND** 本地注册表应仅作为已知 workspace 路径的索引

#### 场景：从任何位置查找 workspace
- **WHEN** 后续 workspace 命令在 workspace 目录外部运行
- **THEN** OpenSpec 可以使用本地注册表查找已知 workspace
- **AND** 需要一个 workspace 的命令可以使用注册表来支持交互式选择器

### 需求：稳定的链接名称
OpenSpec 应使用稳定的链接名称在 workspace planning 中引用 repository 和文件夹。

#### 场景：在 workspace planning 中引用 repository 或文件夹
- **WHEN** workspace 状态或后续 workspace planning artifact 引用链接的 repository 或文件夹
- **THEN** 它们应使用稳定的链接名称
- **AND** 即使本地检出路径不同，相同的链接名称也应保持有效

#### 场景：跨机器重用链接名称
- **WHEN** workspace 在另一台机器上使用
- **THEN** 链接名称应保持稳定
- **AND** 该机器上的本地检出路径可能不同

#### 场景：拒绝无效的链接名称
- **WHEN** OpenSpec 接受一个 workspace 链接名称
- **THEN** 它应拒绝空名称、`.` 或 `..`，以及包含路径分隔符的名称
- **AND** 链接名称在 workspace 内应是唯一的

### 需求：链接的 repository 和文件夹
OpenSpec 应允许 workspace planning 在链接的 repository 和文件夹具有 repository 本地 OpenSpec 状态之前就包含它们。

#### 场景：planning 尚未采用 OpenSpec 的 repository
- **WHEN** workspace 链接了一个尚未包含 repository 本地 `openspec/` 的 repository 路径
- **THEN** 该 repository 仍应可用于 workspace 级别的 planning
- **AND** 实现就绪性可由后续 workflow 处理

#### 场景：跨单 repository 文件夹进行 planning
- **WHEN** planning 跨越一个单 repository 内的多个包、服务、应用或目录
- **THEN** workspace 应能够分别链接这些文件夹
- **AND** 每个文件夹无需拥有自己的 repository 本地 `openspec/` 目录即可参与 workspace planning

#### 场景：一致对待 repository 和文件夹
- **WHEN** workspace 计划同时包含单独的 repository 和单 repository 内的文件夹
- **THEN** OpenSpec 应对两者使用相同的 planning 模型
- **AND** 用户无需为多 repository 和单 repository 变更创建不同类型的 workspace 计划

#### 场景：记录链接而不修改目标
- **WHEN** OpenSpec 记录 workspace 与本地 repository 或文件夹之间的链接
- **THEN** 它应将链接存储在 workspace 状态中
- **AND** 它不应在链接的 repository 或文件夹内创建、复制、移动、初始化或编辑文件

### 需求：先 planning 后实现
OpenSpec 应将 workspace 创建和检测视为 planning 设置，而非实现。

#### 场景：创建或检测 workspace
- **WHEN** workspace 存在
- **THEN** OpenSpec 应将其视为 workspace 级 planning 的地方
- **AND** repository 实现文件应保持不变，直到显式的实现 workflow 运行

#### 场景：推迟 repository 实现
- **WHEN** 需要 repository 本地的实现、应用、验证或 archive 行为
- **THEN** 该行为需要显式的后续 workspace workflow

### 需求：repository 所有权边界
当在 workspace 中进行 planning 时，OpenSpec 应保持 repository 所有权清晰可读。

#### 场景：跨所属 repository 进行 planning
- **WHEN** workspace 计划引用属于某个 repository 或源代码区域的行为
- **THEN** 该所有者应仍然是 spec 规格和实现工作的归属地
- **AND** workspace 应使跨边界计划可见，而不从该所有者处夺取所有权

#### 场景：在所有权明确之前进行草稿
- **WHEN** 跨 repository 行为仍在探索中，所有权不明确
- **THEN** workspace 可以持有 planning 说明或草稿行为
- **AND** 这些草稿应保持与 spec 的 repository 所属规格可区分
