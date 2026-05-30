# workspace-foundation spec

## 目的
定义 OpenSpec 协调 workspace 的产品和存储基础，包括 workspace 身份、共享与本地状态、托管存储、注册表行为、稳定链接名称和 repository 所有权边界。

## 需求
### Requirement: 可识别的 workspace 根目录
OpenSpec 应为用户和 agent 提供可识别的 workspace 根目录，用于跨 repository planning。

#### Scenario: 跨链接 repository 或文件夹 planning
- **WHEN** 用户为其 planning 的 repository 或文件夹创建 OpenSpec workspace 时
- **THEN** workspace 应提供持久的 planning 根目录
- **AND** workspace 应能够随时间持有多个变更

#### Scenario: 在 workspace 内部工作
- **GIVEN** 用户从 workspace 文件夹或其子目录运行 OpenSpec
- **WHEN** OpenSpec 解析当前 workspace
- **THEN** 它应识别 workspace 位置
- **AND** 它应将 workspace 位置的 `changes/` 目录用作 workspace planning 区域

#### Scenario: 避免意外的 workspace schema
- **GIVEN** 一个目录有 `changes/` 但并非 OpenSpec workspace
- **WHEN** OpenSpec 解析当前 workspace
- **THEN** 它应避免将该目录视为 workspace
- **AND** 仅当 workspace 身份文件存在时，才应进入 workspace schema

### Requirement: 稳定的 workspace 名称
OpenSpec 应使用一个 kebab-case workspace 名称，贯穿 workspace 身份、托管存储和本地注册表。

#### Scenario: 使用一个 workspace 名称
- **WHEN** OpenSpec 创建或记录一个托管 workspace
- **THEN** workspace 名称应存储在 `.openspec-workspace/workspace.yaml` 中
- **AND** 同一名称应作为默认的托管 workspace 文件夹名称
- **AND** 同一名称应用作本地注册表名称

#### Scenario: 拒绝无效的 workspace 名称
- **WHEN** OpenSpec 接受一个 workspace 名称
- **THEN** 它应要求使用小写字母、数字和单个连字符分隔符的 kebab-case 名称
- **AND** 它应拒绝空名称、点号名称、前导或尾随连字符的名称、重复连字符的名称、大写字母、空格、下划线、点号和路径分隔符
- **AND** 设置流程应清晰报告 OS 级别的文件夹创建失败

### Requirement: 专用 workspace 身份
OpenSpec 应区分协调 workspace 和 repository 本地 OpenSpec 项目。

#### Scenario: 读取 workspace 身份
- **WHEN** OpenSpec 读取或写入 workspace 身份和 workspace 状态时
- **THEN** 它应使用 `.openspec-workspace/`

#### Scenario: 保留 repository 本地 OpenSpec 项目
- **GIVEN** 一个 repository 本地 OpenSpec 项目使用 `openspec/`
- **WHEN** 该 repository 链接到 workspace
- **THEN** OpenSpec 应继续将 `openspec/` 视为该 repository 的本地 OpenSpec 目录
- **AND** workspace planning 应保持锚定在 workspace 文件夹中

#### Scenario: 避免在 workspace 文件夹中进行 repository 本地初始化
- **WHEN** 用户从 OpenSpec workspace 文件夹工作时
- **THEN** OpenSpec 应将该文件夹视为 workspace 协调界面
- **AND** 用户无需在 workspace 文件夹内初始化 repository 本地的 `openspec/` 项目

### Requirement: 安全 workspace 共享
OpenSpec 应将共享的 workspace 信息与本地机器路径分开。

#### Scenario: 共享 workspace planning
- **WHEN** workspace 与另一个用户或机器共享时
- **THEN** 共享的 workspace 信息应包含可移植的 workspace 身份和稳定的链接名称
- **AND** 它不应要求其他用户重用原用户的绝对检出路径

#### Scenario: 保持检出路径本地化
- **WHEN** OpenSpec 存储 workspace 的本地路径时
- **THEN** 这些路径应视为当前机器和运行时的本地路径
- **AND** 另一台机器可以将相同的链接名称映射到不同的本地路径

#### Scenario: 保留运行时本地路径
- **WHEN** OpenSpec 读取或写入机器本地路径状态时
- **THEN** 它应保留对当前运行时有效的路径字符串
- **AND** 它应支持本机 Windows 路径和 WSL2/Linux 路径作为本地状态值

#### Scenario: 保持托管 workspace 视图状态本地化
- **WHEN** OpenSpec 创建托管 workspace 时
- **THEN** 它应将 `workspace.yaml` 写入 workspace 根目录，作为私有本地视图状态
- **AND** 该文件应为当前机器保留稳定的链接名称和本地路径值

### Requirement: 标准 workspace 位置
OpenSpec 应为 OpenSpec 托管的 workspace 使用标准位置，而无需要求大多数用户选择。

#### Scenario: 使用标准 workspace 位置
- **WHEN** OpenSpec 需要 OpenSpec 托管 workspace 的位置时
- **THEN** 它应使用 `<global-data-dir>/workspaces`
- **AND** `<global-data-dir>` 应遵循现有的 OpenSpec XDG 和平台数据目录行为

#### Scenario: 避免 workspace 特定存储覆盖
- **WHEN** OpenSpec 解析 OpenSpec 托管 workspace 的位置时
- **THEN** 它不应在此切片中使用 workspace 特定的环境变量、命令或配置设置
- **AND** 托管 workspace 存储应保持在 `<global-data-dir>/workspaces` 下

#### Scenario: 从本机 Windows 运行
- **WHEN** OpenSpec 从本机 Windows shell（如 PowerShell）运行
- **AND** `XDG_DATA_HOME` 未设置
- **THEN** OpenSpec 应将托管 workspace 存储在 Windows 全局数据位置
- **AND** 路径应遵循本机 Windows 路径行为

#### Scenario: 从 WSL2 运行
- **WHEN** OpenSpec 从 WSL2 运行
- **THEN** OpenSpec 应将托管 workspace 存储在 WSL 内的 Linux/XDG 数据位置
- **AND** 路径应遵循 WSL 内的 Linux 路径行为

#### Scenario: 自动使用 workspace 位置
- **WHEN** OpenSpec 在后续 workflow 中创建或解析 OpenSpec 托管 workspace 时
- **THEN** 它应默认使用解析后的 workspace 位置
- **AND** 用户应能够遵循正常的 workspace 流程而无需选择存储位置

#### Scenario: 显示 workspace 位置
- **WHEN** OpenSpec 在标准 workspace 位置创建 workspace 时
- **THEN** 它应向用户报告 workspace 位置
- **AND** 它不应隐藏 planning 文件的创建位置

#### Scenario: 保持在当前运行时
- **WHEN** OpenSpec 解析 workspace 位置或本地 repository 路径时
- **THEN** 它应为运行 OpenSpec 的运行时解释路径
- **AND** Windows、UNC WSL 和 WSL 挂载路径应保持为显式的用户提供路径

### Requirement: 本地 workspace 注册表
OpenSpec 应在当前机器上维护一个已知 workspace 的轻量级本地注册表。

#### Scenario: 记录已知 workspace
- **WHEN** OpenSpec 创建或了解一个托管 workspace 时
- **THEN** 它应能够将 workspace 名称和位置记录在本地注册表中
- **AND** 注册表应是机器本地状态

#### Scenario: 保持 workspace 文件夹的权威性
- **WHEN** OpenSpec 读取 workspace 详情时
- **THEN** 每个 workspace 文件夹的 `.openspec-workspace/workspace.yaml` 应保持为该 workspace 的权威来源
- **AND** 本地注册表仅作为已知 workspace 位置的索引

#### Scenario: 从任何位置查找 workspace
- **WHEN** 后续 workspace 命令在 workspace 目录外运行时
- **THEN** OpenSpec 可以使用本地注册表查找已知 workspace
- **AND** 需要单个 workspace 的命令可以使用注册表支持交互式选择器

### Requirement: 稳定的链接名称
OpenSpec 应使用稳定的文件夹样式链接名称来引用 workspace planning 中的 repository 和文件夹。

#### Scenario: 在 workspace planning 中引用 repository 或文件夹
- **WHEN** workspace 状态或后续 workspace planning 制品引用链接的 repository 或文件夹时
- **THEN** 它们应使用稳定的链接名称
- **AND** 即使本地检出路径不同，相同的链接名称应保持有效

#### Scenario: 跨机器重用链接名称
- **WHEN** workspace 在另一台机器上使用时
- **THEN** 链接名称应保持稳定
- **AND** 该机器上的本地检出路径可能不同

#### Scenario: 拒绝无效的链接名称
- **WHEN** OpenSpec 接受 workspace 链接名称时
- **THEN** 它应拒绝空名称、`.` 或 `..`，以及包含路径分隔符的名称
- **AND** 链接名称在 workspace 内应唯一
- **AND** 链接名称不要求使用 workspace 名称的 kebab-case

### Requirement: 链接的 repository 和文件夹
OpenSpec 应允许 workspace planning 在 repository 本地 OpenSpec 状态存在之前包含链接的 repository 和文件夹。

#### Scenario: planning 尚未采用 OpenSpec 的 repository
- **WHEN** workspace 链接的 repository 路径尚未包含 repository 本地 `openspec/`
- **THEN** 该 repository 仍应可用于 workspace 级 planning
- **AND** 实施准备状态可由后续 workflow 处理

#### Scenario: 跨单 repository 文件夹 planning
- **WHEN** planning 涉及单个单 repository 内的多个包、服务、应用或目录时
- **THEN** workspace 应能够分别链接这些文件夹
- **AND** 每个文件夹无需自己的 repository 本地 `openspec/` 目录即可参与 workspace planning

#### Scenario: 一致对待 repository 和文件夹
- **WHEN** workspace 计划同时包含单独的 repository 和单个单 repository 内的文件夹时
- **THEN** OpenSpec 应对两者使用相同的 planning 模型
- **AND** 用户无需为多 repository 和单 repository 变更创建不同类型的 workspace 计划

#### Scenario: 记录链接而不更改目标
- **WHEN** OpenSpec 记录 workspace 与本地 repository 或文件夹之间的链接时
- **THEN** 它应将链接存储在 workspace 状态中
- **AND** 它不应在链接的 repository 或文件夹内创建、复制、移动、初始化或编辑文件

### Requirement: 实施前 planning
OpenSpec 应将 workspace 创建和检测视为 planning 设置，而非实施。

#### Scenario: 创建或检测 workspace
- **WHEN** workspace 存在时
- **THEN** OpenSpec 应将其视为 workspace 级 planning 的位置
- **AND** repository 实施文件应保持不变，直到显式的实施 workflow 运行

#### Scenario: 推迟 repository 实施
- **WHEN** 需要 repository 本地的实施、应用、验证或 archive 行为时
- **THEN** 该行为需要显式的后续 workspace workflow

### Requirement: repository 所有权边界
OpenSpec 在 planning 在 workspace 中进行时应保持 repository 所有权的清晰可辨。

#### Scenario: 跨拥有 repository planning
- **WHEN** workspace 计划引用由 repository 或源代码区域拥有的行为时
- **THEN** 该所有者应保持为 spec spec 和实施工作的归属地
- **AND** workspace 应使跨边界计划可见，而不从该所有者处夺走所有权

#### Scenario: 所有权未明确时的草稿
- **WHEN** 跨 repository 行为仍在探索中且所有权不明确时
- **THEN** workspace 可以持有 planning 说明或草稿行为
- **AND** 这些草稿应保持与 spec 的 repository 拥有 spec 可区分

### Requirement: workspace 首选开启器状态
当用户明确选择时，OpenSpec 应将 workspace 的首选开启器存储在机器本地 workspace 状态中。

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
- **THEN** OpenSpec 应保持 workspace 首选开启器未设置
- **AND** 未设置状态应允许 `workspace open` 后续提示

#### Scenario: 支持的首选开启器值
- **WHEN** OpenSpec 接受首选开启器值时
- **THEN** 它应接受 `codex`、`claude`、`github-copilot` 和 `editor`
- **AND** 它应将 `editor` 映射到 `kind: editor` 和 `id: vscode`
- **AND** 它应将 agent 值映射到 `kind: agent` 和对应的 agent `id`

#### Scenario: 对设置开启器选项排序
- **WHEN** 交互式设置显示开启器选项时
- **THEN** OpenSpec 应显示所有支持的开启器
- **AND** 它应将检测到可执行文件的开启器排在不可用的开启器之前
- **AND** 不可用的开启器应保持可见并附带可用性说明

### Requirement: 维护的 workspace 开启表面
OpenSpec 应维护使 workspace 在设置和链接更改后可直接开启的文件。

#### Scenario: 在设置期间创建开启表面
- **WHEN** `openspec workspace setup` 创建 workspace 时
- **THEN** OpenSpec 应创建或刷新 `AGENTS.md`
- **AND** 它应创建或刷新 `<workspace-name>.code-workspace`
- **AND** 默认情况下，它不应为机器本地开启文件创建 workspace 忽略规则

#### Scenario: 链接后刷新开启表面
- **WHEN** `openspec workspace link` 成功时
- **THEN** OpenSpec 应刷新 `AGENTS.md`
- **AND** 它应刷新 `<workspace-name>.code-workspace`

#### Scenario: 重新链接后刷新开启表面
- **WHEN** `openspec workspace relink` 成功时
- **THEN** OpenSpec 应刷新 `AGENTS.md`
- **AND** 它应刷新 `<workspace-name>.code-workspace`

#### Scenario: 构建 VS Code workspace 文件
- **WHEN** OpenSpec 刷新 `<workspace-name>.code-workspace`
- **THEN** 该文件应在 workspace 本地文件之前包含每个具有有效本地路径的链接 repository 或文件夹
- **AND** 它应在可用时包含附加上下文倡议
- **AND** 它应将 workspace 根目录作为 `OpenSpec workspace` 包含
- **AND** 它应省略本地路径缺失或无效的链接 repository 或文件夹

#### Scenario: 清理遗留 workspace 忽略规则
- **WHEN** OpenSpec 刷新 workspace 开启表面时
- **THEN** 它应移除维护的 `<workspace-name>.code-workspace` 文件的遗留忽略规则（如果存在）
- **AND** 它应保留不相关的用户编写的忽略规则

#### Scenario: 保留用户编写的 AGENTS 内容
- **GIVEN** `AGENTS.md` 包含 OpenSpec workspace 指导标记外的内容
- **WHEN** OpenSpec 刷新 workspace 指导时
- **THEN** 它应仅替换标记的 OpenSpec workspace 指导块
- **AND** 它应保留标记外的内容

#### Scenario: 标记缺失时追加 AGENTS 指导
- **GIVEN** `AGENTS.md` 存在且 OpenSpec workspace 指导标记缺失
- **WHEN** OpenSpec 刷新 workspace 指导时
- **THEN** 它应追加标记的 OpenSpec workspace 指导块
- **AND** 它应保留现有文件内容
