# workspace-foundation 规范

## 目的
定义 OpenSpec 协调工作区的产品和存储基础，包括工作区身份、共享与本地状态、托管存储、注册表行为、稳定链接名称和仓库所有权边界。

## 需求
### Requirement: 可识别的工作区根目录
OpenSpec 应为用户和代理提供可识别的工作区根目录，用于跨仓库规划。

#### Scenario: 跨链接仓库或文件夹规划
- **WHEN** 用户为其规划的仓库或文件夹创建 OpenSpec 工作区时
- **THEN** 工作区应提供持久的规划根目录
- **AND** 工作区应能够随时间持有多个变更

#### Scenario: 在工作区内部工作
- **GIVEN** 用户从工作区文件夹或其子目录运行 OpenSpec
- **WHEN** OpenSpec 解析当前工作区
- **THEN** 它应识别工作区位置
- **AND** 它应将工作区位置的 `changes/` 目录用作工作区规划区域

#### Scenario: 避免意外的工作区模式
- **GIVEN** 一个目录有 `changes/` 但并非 OpenSpec 工作区
- **WHEN** OpenSpec 解析当前工作区
- **THEN** 它应避免将该目录视为工作区
- **AND** 仅当工作区身份文件存在时，才应进入工作区模式

### Requirement: 稳定的工作区名称
OpenSpec 应使用一个 kebab-case 工作区名称，贯穿工作区身份、托管存储和本地注册表。

#### Scenario: 使用一个工作区名称
- **WHEN** OpenSpec 创建或记录一个托管工作区
- **THEN** 工作区名称应存储在 `.openspec-workspace/workspace.yaml` 中
- **AND** 同一名称应作为默认的托管工作区文件夹名称
- **AND** 同一名称应用作本地注册表名称

#### Scenario: 拒绝无效的工作区名称
- **WHEN** OpenSpec 接受一个工作区名称
- **THEN** 它应要求使用小写字母、数字和单个连字符分隔符的 kebab-case 名称
- **AND** 它应拒绝空名称、点号名称、前导或尾随连字符的名称、重复连字符的名称、大写字母、空格、下划线、点号和路径分隔符
- **AND** 设置流程应清晰报告 OS 级别的文件夹创建失败

### Requirement: 专用工作区身份
OpenSpec 应区分协调工作区和仓库本地 OpenSpec 项目。

#### Scenario: 读取工作区身份
- **WHEN** OpenSpec 读取或写入工作区身份和工作区状态时
- **THEN** 它应使用 `.openspec-workspace/`

#### Scenario: 保留仓库本地 OpenSpec 项目
- **GIVEN** 一个仓库本地 OpenSpec 项目使用 `openspec/`
- **WHEN** 该仓库链接到工作区
- **THEN** OpenSpec 应继续将 `openspec/` 视为该仓库的本地 OpenSpec 目录
- **AND** 工作区规划应保持锚定在工作区文件夹中

#### Scenario: 避免在工作区文件夹中进行仓库本地初始化
- **WHEN** 用户从 OpenSpec 工作区文件夹工作时
- **THEN** OpenSpec 应将该文件夹视为工作区协调界面
- **AND** 用户无需在工作区文件夹内初始化仓库本地的 `openspec/` 项目

### Requirement: 安全工作区共享
OpenSpec 应将共享的工作区信息与本地机器路径分开。

#### Scenario: 共享工作区规划
- **WHEN** 工作区与另一个用户或机器共享时
- **THEN** 共享的工作区信息应包含可移植的工作区身份和稳定的链接名称
- **AND** 它不应要求其他用户重用原用户的绝对检出路径

#### Scenario: 保持检出路径本地化
- **WHEN** OpenSpec 存储工作区的本地路径时
- **THEN** 这些路径应视为当前机器和运行时的本地路径
- **AND** 另一台机器可以将相同的链接名称映射到不同的本地路径

#### Scenario: 保留运行时本地路径
- **WHEN** OpenSpec 读取或写入机器本地路径状态时
- **THEN** 它应保留对当前运行时有效的路径字符串
- **AND** 它应支持本机 Windows 路径和 WSL2/Linux 路径作为本地状态值

#### Scenario: 保持托管工作区视图状态本地化
- **WHEN** OpenSpec 创建托管工作区时
- **THEN** 它应将 `workspace.yaml` 写入工作区根目录，作为私有本地视图状态
- **AND** 该文件应为当前机器保留稳定的链接名称和本地路径值

### Requirement: 标准工作区位置
OpenSpec 应为 OpenSpec 托管的工作区使用标准位置，而无需要求大多数用户选择。

#### Scenario: 使用标准工作区位置
- **WHEN** OpenSpec 需要 OpenSpec 托管工作区的位置时
- **THEN** 它应使用 `<global-data-dir>/workspaces`
- **AND** `<global-data-dir>` 应遵循现有的 OpenSpec XDG 和平台数据目录行为

#### Scenario: 避免工作区特定存储覆盖
- **WHEN** OpenSpec 解析 OpenSpec 托管工作区的位置时
- **THEN** 它不应在此切片中使用工作区特定的环境变量、命令或配置设置
- **AND** 托管工作区存储应保持在 `<global-data-dir>/workspaces` 下

#### Scenario: 从本机 Windows 运行
- **WHEN** OpenSpec 从本机 Windows shell（如 PowerShell）运行
- **AND** `XDG_DATA_HOME` 未设置
- **THEN** OpenSpec 应将托管工作区存储在 Windows 全局数据位置
- **AND** 路径应遵循本机 Windows 路径行为

#### Scenario: 从 WSL2 运行
- **WHEN** OpenSpec 从 WSL2 运行
- **THEN** OpenSpec 应将托管工作区存储在 WSL 内的 Linux/XDG 数据位置
- **AND** 路径应遵循 WSL 内的 Linux 路径行为

#### Scenario: 自动使用工作区位置
- **WHEN** OpenSpec 在后续工作流中创建或解析 OpenSpec 托管工作区时
- **THEN** 它应默认使用解析后的工作区位置
- **AND** 用户应能够遵循正常的工作区流程而无需选择存储位置

#### Scenario: 显示工作区位置
- **WHEN** OpenSpec 在标准工作区位置创建工作区时
- **THEN** 它应向用户报告工作区位置
- **AND** 它不应隐藏规划文件的创建位置

#### Scenario: 保持在当前运行时
- **WHEN** OpenSpec 解析工作区位置或本地仓库路径时
- **THEN** 它应为运行 OpenSpec 的运行时解释路径
- **AND** Windows、UNC WSL 和 WSL 挂载路径应保持为显式的用户提供路径

### Requirement: 本地工作区注册表
OpenSpec 应在当前机器上维护一个已知工作区的轻量级本地注册表。

#### Scenario: 记录已知工作区
- **WHEN** OpenSpec 创建或了解一个托管工作区时
- **THEN** 它应能够将工作区名称和位置记录在本地注册表中
- **AND** 注册表应是机器本地状态

#### Scenario: 保持工作区文件夹的权威性
- **WHEN** OpenSpec 读取工作区详情时
- **THEN** 每个工作区文件夹的 `.openspec-workspace/workspace.yaml` 应保持为该工作区的权威来源
- **AND** 本地注册表仅作为已知工作区位置的索引

#### Scenario: 从任何位置查找工作区
- **WHEN** 后续工作区命令在工作区目录外运行时
- **THEN** OpenSpec 可以使用本地注册表查找已知工作区
- **AND** 需要单个工作区的命令可以使用注册表支持交互式选择器

### Requirement: 稳定的链接名称
OpenSpec 应使用稳定的文件夹样式链接名称来引用工作区规划中的仓库和文件夹。

#### Scenario: 在工作区规划中引用仓库或文件夹
- **WHEN** 工作区状态或后续工作区规划制品引用链接的仓库或文件夹时
- **THEN** 它们应使用稳定的链接名称
- **AND** 即使本地检出路径不同，相同的链接名称应保持有效

#### Scenario: 跨机器重用链接名称
- **WHEN** 工作区在另一台机器上使用时
- **THEN** 链接名称应保持稳定
- **AND** 该机器上的本地检出路径可能不同

#### Scenario: 拒绝无效的链接名称
- **WHEN** OpenSpec 接受工作区链接名称时
- **THEN** 它应拒绝空名称、`.` 或 `..`，以及包含路径分隔符的名称
- **AND** 链接名称在工作区内应唯一
- **AND** 链接名称不要求使用工作区名称的 kebab-case

### Requirement: 链接的仓库和文件夹
OpenSpec 应允许工作区规划在仓库本地 OpenSpec 状态存在之前包含链接的仓库和文件夹。

#### Scenario: 规划尚未采用 OpenSpec 的仓库
- **WHEN** 工作区链接的仓库路径尚未包含仓库本地 `openspec/`
- **THEN** 该仓库仍应可用于工作区级规划
- **AND** 实施准备状态可由后续工作流处理

#### Scenario: 跨单仓库文件夹规划
- **WHEN** 规划涉及单个单仓库内的多个包、服务、应用或目录时
- **THEN** 工作区应能够分别链接这些文件夹
- **AND** 每个文件夹无需自己的仓库本地 `openspec/` 目录即可参与工作区规划

#### Scenario: 一致对待仓库和文件夹
- **WHEN** 工作区计划同时包含单独的仓库和单个单仓库内的文件夹时
- **THEN** OpenSpec 应对两者使用相同的规划模型
- **AND** 用户无需为多仓库和单仓库变更创建不同类型的工作区计划

#### Scenario: 记录链接而不更改目标
- **WHEN** OpenSpec 记录工作区与本地仓库或文件夹之间的链接时
- **THEN** 它应将链接存储在工作区状态中
- **AND** 它不应在链接的仓库或文件夹内创建、复制、移动、初始化或编辑文件

### Requirement: 实施前规划
OpenSpec 应将工作区创建和检测视为规划设置，而非实施。

#### Scenario: 创建或检测工作区
- **WHEN** 工作区存在时
- **THEN** OpenSpec 应将其视为工作区级规划的位置
- **AND** 仓库实施文件应保持不变，直到显式的实施工作流运行

#### Scenario: 推迟仓库实施
- **WHEN** 需要仓库本地的实施、应用、验证或归档行为时
- **THEN** 该行为需要显式的后续工作区工作流

### Requirement: 仓库所有权边界
OpenSpec 在规划在工作区中进行时应保持仓库所有权的清晰可辨。

#### Scenario: 跨拥有仓库规划
- **WHEN** 工作区计划引用由仓库或源代码区域拥有的行为时
- **THEN** 该所有者应保持为规范规范和实施工作的归属地
- **AND** 工作区应使跨边界计划可见，而不从该所有者处夺走所有权

#### Scenario: 所有权未明确时的草稿
- **WHEN** 跨仓库行为仍在探索中且所有权不明确时
- **THEN** 工作区可以持有规划说明或草稿行为
- **AND** 这些草稿应保持与规范的仓库拥有规范可区分

### Requirement: 工作区首选开启器状态
当用户明确选择时，OpenSpec 应将工作区的首选开启器存储在机器本地工作区状态中。

#### Scenario: 记录交互式设置开启器选择
- **WHEN** 交互式用户在 `openspec workspace setup` 期间选择首选开启器时
- **THEN** OpenSpec 应将开启器记录在 `.openspec-workspace/local.yaml` 中
- **AND** 存储值应使用结构化的 `preferred_opener` 对象，包含 `kind` 和 `id`

#### Scenario: 记录非交互式设置开启器选择
- **WHEN** 非交互式用户运行 `openspec workspace setup --no-interactive --opener codex`
- **THEN** OpenSpec 应将 `preferred_opener.kind` 记录为 `agent`
- **AND** 它应将 `preferred_opener.id` 记录为 `codex`

#### Scenario: 非交互式设置中保持开启器未设置
- **WHEN** 非交互式用户运行 `openspec workspace setup --no-interactive` 且未选择开启器时
- **THEN** OpenSpec 应保持工作区首选开启器未设置
- **AND** 未设置状态应允许 `workspace open` 后续提示

#### Scenario: 支持的首选开启器值
- **WHEN** OpenSpec 接受首选开启器值时
- **THEN** 它应接受 `codex`、`claude`、`github-copilot` 和 `editor`
- **AND** 它应将 `editor` 映射到 `kind: editor` 和 `id: vscode`
- **AND** 它应将代理值映射到 `kind: agent` 和对应的代理 `id`

#### Scenario: 对设置开启器选项排序
- **WHEN** 交互式设置显示开启器选项时
- **THEN** OpenSpec 应显示所有支持的开启器
- **AND** 它应将检测到可执行文件的开启器排在不可用的开启器之前
- **AND** 不可用的开启器应保持可见并附带可用性说明

### Requirement: 维护的工作区开启表面
OpenSpec 应维护使工作区在设置和链接更改后可直接开启的文件。

#### Scenario: 在设置期间创建开启表面
- **WHEN** `openspec workspace setup` 创建工作区时
- **THEN** OpenSpec 应创建或刷新 `AGENTS.md`
- **AND** 它应创建或刷新 `<workspace-name>.code-workspace`
- **AND** 默认情况下，它不应为机器本地开启文件创建工作区忽略规则

#### Scenario: 链接后刷新开启表面
- **WHEN** `openspec workspace link` 成功时
- **THEN** OpenSpec 应刷新 `AGENTS.md`
- **AND** 它应刷新 `<workspace-name>.code-workspace`

#### Scenario: 重新链接后刷新开启表面
- **WHEN** `openspec workspace relink` 成功时
- **THEN** OpenSpec 应刷新 `AGENTS.md`
- **AND** 它应刷新 `<workspace-name>.code-workspace`

#### Scenario: 构建 VS Code 工作区文件
- **WHEN** OpenSpec 刷新 `<workspace-name>.code-workspace`
- **THEN** 该文件应在工作区本地文件之前包含每个具有有效本地路径的链接仓库或文件夹
- **AND** 它应在可用时包含附加上下文倡议
- **AND** 它应将工作区根目录作为 `OpenSpec workspace` 包含
- **AND** 它应省略本地路径缺失或无效的链接仓库或文件夹

#### Scenario: 清理遗留工作区忽略规则
- **WHEN** OpenSpec 刷新工作区开启表面时
- **THEN** 它应移除维护的 `<workspace-name>.code-workspace` 文件的遗留忽略规则（如果存在）
- **AND** 它应保留不相关的用户编写的忽略规则

#### Scenario: 保留用户编写的 AGENTS 内容
- **GIVEN** `AGENTS.md` 包含 OpenSpec 工作区指导标记外的内容
- **WHEN** OpenSpec 刷新工作区指导时
- **THEN** 它应仅替换标记的 OpenSpec 工作区指导块
- **AND** 它应保留标记外的内容

#### Scenario: 标记缺失时追加 AGENTS 指导
- **GIVEN** `AGENTS.md` 存在且 OpenSpec 工作区指导标记缺失
- **WHEN** OpenSpec 刷新工作区指导时
- **THEN** 它应追加标记的 OpenSpec 工作区指导块
- **AND** 它应保留现有文件内容
