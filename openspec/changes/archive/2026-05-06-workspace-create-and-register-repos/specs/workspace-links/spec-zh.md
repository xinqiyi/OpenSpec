## 新增需求

### 需求：引导式 workspace 设置
OpenSpec 应当为开始 workspace planning 的用户提供引导式设置流程。

#### 场景：通过设置创建 workspace
- **WHEN** 用户运行 `openspec workspace setup`
- **THEN** OpenSpec 应引导用户创建 OpenSpec workspace
- **AND** workspace 应使用 workspace 基础架构中的标准 workspace 位置

#### 场景：先询问 workspace 名称
- **WHEN** 交互式设置开始时
- **THEN** OpenSpec 应在询问 repository 或文件夹之前先询问 workspace 名称
- **AND** workspace 名称应使用小写字母、数字和连字符组成的 kebab-case 格式

#### 场景：设置过程中重试无效的 workspace 名称
- **WHEN** 交互式用户输入了无效的 workspace 名称
- **THEN** OpenSpec 应说明 workspace 名称必须为 kebab-case 格式
- **AND** 应让用户在继续设置之前输入另一个 workspace 名称

#### 场景：链接必需的第一个 repository 或文件夹
- **WHEN** 设置询问 repository 或文件夹时
- **THEN** 用户应提供至少一个现有的 repository 或文件夹路径
- **AND** 在至少链接一个路径之前，设置不应成功完成

#### 场景：设置过程中推断链接名称
- **WHEN** 用户在设置过程中提供 repository 或文件夹路径时
- **THEN** OpenSpec 应从文件夹基本名称推断链接名称
- **AND** 仅在推断的名称冲突时询问不同的名称

#### 场景：设置过程中处理推断的链接名称冲突
- **GIVEN** 设置推断的链接名称已存在于 workspace 中
- **WHEN** 设置为交互式时
- **THEN** OpenSpec 应显示冲突的链接名称和该链接的现有路径
- **AND** 应在继续之前询问用户不同的链接名称

#### 场景：保留文件夹风格的链接名称
- **WHEN** OpenSpec 接受 workspace 链接名称时
- **THEN** 它应允许在 workspace 基础架构的链接名称规则下有效的文件夹风格名称
- **AND** 不应要求链接名称使用更严格的 workspace 名称 kebab-case 规则

#### 场景：设置过程中添加多个 repository 或文件夹
- **WHEN** 设置链接一个 repository 或文件夹时
- **THEN** OpenSpec 应让用户通过简单的重复提示添加另一个 repository 或文件夹
- **AND** 每个链接的路径应在不编辑目标 repository 或文件夹的情况下记录

#### 场景：设置过程中存储已验证的绝对路径
- **WHEN** 设置链接一个 repository 或文件夹路径时
- **THEN** OpenSpec 应验证该路径解析为现有的文件夹
- **AND** 应将绝对运行时本地路径存储在机器本地状态中，而不是原始用户输入
- **AND** 相对输入应相对于命令的当前工作目录进行解析

#### 场景：在设置链接路径中保留等号
- **WHEN** 非交互式设置接收到的 `--link` 值解析为现有文件夹且包含 `=`
- **THEN** OpenSpec 应将整个值作为路径处理
- **AND** 应从文件夹基本名称推断链接名称
- **AND** 显式的 `--link <name>=<path>` 输入应保留 `<path>` 内部的 `=` 字符

#### 场景：使用非交互式输入运行设置
- **WHEN** `openspec workspace setup --no-interactive` 接收到 workspace 名称和至少一个有效链接
- **THEN** OpenSpec 应在无需提示的情况下创建 workspace
- **AND** 应支持重复的 `--link` 值

#### 场景：非交互式设置重复链接名称
- **WHEN** `openspec workspace setup --no-interactive` 收到两个具有相同推断或显式名称的链接
- **THEN** OpenSpec 应失败并显示明确的重复链接名称错误
- **AND** 错误信息应显示冲突的链接名称和第一个使用该名称的路径
- **AND** 应建议使用具有不同名称的显式 `--link <name>=<path>` 值

#### 场景：缺少非交互式设置输入
- **WHEN** `openspec workspace setup --no-interactive` 缺少 workspace 名称或链接
- **THEN** OpenSpec 应失败并显示清晰的消息
- **AND** 应说明哪些标志是必需的

#### 场景：完成设置
- **WHEN** 设置完成
- **THEN** OpenSpec 应显示 workspace 位置、planning 路径和链接的 repository 或文件夹
- **AND** 应检查当前机器可以解析哪些内容

#### 场景：在本地记录已创建的 workspace
- **WHEN** 设置创建 workspace
- **THEN** OpenSpec 应将其记录在本地 workspace 注册表中
- **AND** workspace 文件夹应保持为 workspace 状态的唯一真实来源

#### 场景：设置过程中重用现有 workspace 名称
- **GIVEN** 具有所请求名称的托管 workspace 已存在
- **WHEN** 用户使用该 workspace 名称运行设置
- **THEN** OpenSpec 应说明该 workspace 已存在
- **AND** 不应覆盖现有的 workspace

### 需求：workspace 发现
OpenSpec 应让用户看到当前机器上可用的 OpenSpec 托管 workspace。

#### 场景：列出 workspace
- **WHEN** 用户运行 `openspec workspace list`
- **THEN** OpenSpec 应列出已知的托管 workspace
- **AND** 每个 workspace 应包含 workspace 名称、workspace 位置以及链接的 repository 或文件夹

#### 场景：使用简短列表命令
- **WHEN** 用户运行 `openspec workspace ls`
- **THEN** OpenSpec 的行为应与 `openspec workspace list` 相同

#### 场景：没有 workspace 时列出
- **WHEN** 用户运行 `openspec workspace list`
- **AND** 没有托管 workspace 存在
- **THEN** OpenSpec 应说明未找到 workspace
- **AND** 应向用户展示如何创建一个

#### 场景：列出过期的注册表条目
- **WHEN** 本地注册表包含一个不再存在的 workspace 位置
- **THEN** `workspace list` 应报告过期的 workspace 条目
- **AND** 应避免静默删除注册表状态
- **AND** 应避免自动重写或修复注册表状态

#### 场景：避免注册表清理命令
- **WHEN** 用户在此切片中检查过期的 workspace 注册表条目时
- **THEN** OpenSpec 应将过期条目视为仅报告诊断
- **AND** 不应公开诸如 `workspace forget` 之类的注册表清理命令

### 需求：全局 workspace 命令
OpenSpec 应让 workspace 命令从 workspace 目录外部运行。

#### 场景：通过标志选择 workspace
- **WHEN** 需要一个 workspace 的命令接收到 `--workspace <name>`
- **THEN** OpenSpec 应从本地注册表中使用该 workspace
- **AND** 如果 workspace 名称未知，应清晰地失败

#### 场景：使用当前 workspace
- **GIVEN** 命令从 workspace 文件夹或子目录运行
- **WHEN** 命令需要一个 workspace 且未提供 `--workspace` 标志
- **THEN** OpenSpec 应使用当前 workspace

#### 场景：使用未注册的当前 workspace
- **GIVEN** 命令从有效的 workspace 文件夹或子目录运行
- **AND** 该 workspace 未在本地 workspace 注册表中记录
- **WHEN** 命令需要一个 workspace 且未提供 `--workspace <name>` 标志
- **THEN** OpenSpec 应使用当前 workspace
- **AND** 应包含一个非致命警告状态，代码为 `workspace_not_in_local_registry`
- **AND** 警告应说明用户如何让该 workspace 在本地记录

#### 场景：变更后记录未注册的当前 workspace
- **GIVEN** 一个可变 workspace 命令使用了未在本地 workspace 注册表中记录的有效当前 workspace
- **WHEN** `workspace link` 或 `workspace relink` 成功时
- **THEN** OpenSpec 应将 workspace 名称和位置记录在本地 workspace 注册表中

#### 场景：Doctor 不注册当前 workspace
- **GIVEN** `workspace doctor` 使用了未在本地 workspace 注册表中记录的有效当前 workspace
- **WHEN** doctor 完成时
- **THEN** OpenSpec 应报告非致命注册表警告
- **AND** 不应写入注册表状态

#### 场景：从多个 workspace 中选择
- **GIVEN** 存在多个已知 workspace
- **WHEN** 交互式命令需要一个 workspace 且未指定时
- **THEN** OpenSpec 应显示 workspace 选择器
- **AND** 选择器应包含 workspace 名称和路径

#### 场景：模糊的非交互式 workspace 选择
- **GIVEN** 存在多个已知 workspace
- **WHEN** 非交互式命令需要一个 workspace 且未指定时
- **THEN** OpenSpec 应失败并显示清晰的消息
- **AND** 应建议传递 `--workspace <name>`

#### 场景：模糊的 JSON workspace 选择
- **GIVEN** 存在多个已知 workspace
- **WHEN** 以 `--json` 运行的命令需要一个 workspace 且未指定时
- **THEN** OpenSpec 应失败而不显示选择器
- **AND** 应发出结构化的状态错误
- **AND** 应建议传递 `--workspace <name>`

#### 场景：需要 workspace 的命令没有已知 workspace
- **GIVEN** 本地注册表中没有已知 workspace
- **AND** 命令不是从 workspace 文件夹或子目录运行
- **WHEN** `workspace link`、`workspace relink`、`workspace doctor` 或其他需要一个 workspace 的命令在未带 `--workspace <name>` 的情况下运行
- **THEN** OpenSpec 应失败，无论交互 schema 如何，都不显示选择器
- **AND** 应打印 `未找到已知的 OpenSpec workspace。请先运行 'openspec workspace setup'。`
- **AND** 应说明在至少一个 workspace 已知后可以使用 `--workspace <name>`

### 需求：workspace 链接
OpenSpec 应让用户在创建变更之前将现有 repository 或文件夹链接到 workspace。

#### 场景：使用推断名称链接
- **WHEN** 用户运行 `openspec workspace link <path>`
- **THEN** OpenSpec 应从文件夹基本名称推断链接名称
- **AND** 应将验证后的绝对本地路径存储为机器本地状态

#### 场景：使用显式名称链接
- **WHEN** 用户运行 `openspec workspace link <name> <path>`
- **THEN** OpenSpec 应使用显式链接名称进行 planning
- **AND** 应将验证后的绝对本地路径存储为机器本地状态

#### 场景：要求路径存在
- **WHEN** 用户链接 repository 或文件夹路径时
- **THEN** 该路径应在当前机器上存在
- **AND** OpenSpec 应拒绝缺失路径并显示清晰的消息

#### 场景：存储前解析链接路径
- **WHEN** 用户链接 repository 或文件夹路径时
- **THEN** OpenSpec 应存储当前运行时的验证绝对路径
- **AND** 相对输入应相对于命令的当前工作目录进行解析
- **AND** OpenSpec 不应在原生 Windows、WSL2 和 Unix 运行时之间转换路径

#### 场景：链接 monorepo 文件夹
- **WHEN** 用户链接 monorepo 中的包、服务、应用或目录时
- **THEN** OpenSpec 应将其存储为 workspace 链接
- **AND** 不应要求该文件夹拥有自己的 repository 本地 `openspec/` 目录

#### 场景：链接没有本地 OpenSpec 的 repository
- **WHEN** 用户链接一个不包含 repository 本地 OpenSpec 状态的路径
- **THEN** OpenSpec 应保留该 repository 或文件夹以供 workspace planning 使用
- **AND** 不应将缺失的 repository 本地 OpenSpec 状态视为链接失败

#### 场景：仅记录链接
- **WHEN** 用户链接 repository 或文件夹时
- **THEN** OpenSpec 应记录 workspace 状态和本地路径状态
- **AND** 不应在链接的 repository 或文件夹中创建、复制、移动、初始化或编辑文件

#### 场景：本地状态无效时阻止链接
- **GIVEN** workspace 机器本地状态文件存在但无法解析或验证
- **WHEN** 用户运行 `openspec workspace link`
- **THEN** OpenSpec 应失败，状态码为 `workspace_local_state_invalid`
- **AND** 不应重写共享 workspace 状态或机器本地路径状态

#### 场景：重用链接名称
- **GIVEN** workspace 已有一个具有给定名称的链接
- **WHEN** 用户尝试用相同名称链接另一个路径时
- **THEN** OpenSpec 应说明该链接名称已被另一个链接使用
- **AND** 应显示现有的链接名称和路径
- **AND** 应建议选择不同的链接名称
- **AND** 应在用户意图更改现有链接路径时建议 `workspace relink <name> <path>`
- **AND** 除非用户显式重新链接，否则应保留现有链接

### 需求：workspace 重新链接
OpenSpec 应让用户无需重建 workspace 即可更新现有的链接路径。

#### 场景：更新本地路径
- **GIVEN** workspace 有一个链接
- **WHEN** 用户运行 `openspec workspace relink <name> <path>`
- **THEN** OpenSpec 应保留稳定的链接名称
- **AND** 应将当前机器的机器本地路径更新为验证后的绝对路径

#### 场景：要求重新链接路径存在
- **WHEN** 用户重新链接到新路径时
- **THEN** 新路径应在当前机器上存在
- **AND** OpenSpec 应拒绝缺失路径并显示清晰的消息

#### 场景：存储前解析重新链接路径
- **WHEN** 用户重新链接到新路径时
- **THEN** OpenSpec 应存储当前运行时的验证绝对路径
- **AND** 相对输入应相对于命令的当前工作目录进行解析

#### 场景：本地状态无效时阻止重新链接
- **GIVEN** workspace 机器本地状态文件存在但无法解析或验证
- **WHEN** 用户运行 `openspec workspace relink`
- **THEN** OpenSpec 应失败，状态码为 `workspace_local_state_invalid`
- **AND** 不应重写机器本地路径状态

#### 场景：更新未知链接
- **WHEN** 用户尝试重新链接一个不存在的链接时
- **THEN** OpenSpec 应说明该链接名称未知
- **AND** 应保留现有的 workspace 状态

#### 场景：避免所有者和交接字段
- **WHEN** 用户在此切片中链接或重新链接 repository 或文件夹时
- **THEN** OpenSpec 不应询问所有者或交接元数据
- **AND** 链接维护应专注于名称和本地路径

### 需求：workspace 健康检查
OpenSpec 应说明当前机器可以为 workspace 解析哪些内容。

#### 场景：Doctor 检查一个选定的 workspace
- **WHEN** 用户运行 `openspec workspace doctor`
- **THEN** OpenSpec 应检查一个选定的 workspace
- **AND** 默认情况下不应扫描本地注册表中的每个已知 workspace

#### 场景：Doctor 推断当前 workspace
- **GIVEN** 命令从 workspace 文件夹或子目录运行
- **WHEN** 用户运行 `openspec workspace doctor` 而不带 `--workspace <name>`
- **THEN** OpenSpec 应检查当前 workspace

#### 场景：检查健康的 workspace
- **WHEN** 用户运行 `openspec workspace doctor`
- **THEN** OpenSpec 应显示 workspace 位置和 workspace planning 路径
- **AND** 应显示链接的 repository 或文件夹以及哪些路径在当前机器上可解析

#### 场景：选定的 workspace 位置缺失
- **GIVEN** 选定的 workspace 来自本地注册表
- **AND** 注册的 workspace 位置缺失或无效
- **WHEN** 用户运行 `openspec workspace doctor`
- **THEN** OpenSpec 应报告选定的 workspace 状态错误
- **AND** 不应尝试检查该 workspace 的链接

#### 场景：报告 repository 本地 spec 路径
- **WHEN** 链接的 repository 或文件夹可解析时
- **THEN** doctor 应在 repository 本地 `openspec/specs` 存在时报告 `repo_specs_path`
- **AND** 当 repository 本地 spec 不存在时报告 `repo_specs_path: null`

#### 场景：检查缺失的路径
- **WHEN** 链接指向当前机器上缺失的路径时
- **THEN** doctor 应标识受影响的链接名称
- **AND** 应包含建议的 `workspace relink` 修复

#### 场景：检查共享状态和本地状态漂移
- **WHEN** 共享 workspace 状态和机器本地路径状态不一致时
- **THEN** doctor 应说明哪些链接名称受影响
- **AND** 应区分共享 workspace 链接和仅本地路径

#### 场景：报告无效的本地状态
- **WHEN** list 或 doctor 读取的 workspace 其机器本地状态文件无法解析或验证时
- **THEN** OpenSpec 应报告状态码 `workspace_local_state_invalid`
- **AND** 应避免将无效的本地状态视为空路径映射以进行变更或修复建议
- **AND** 不应重写 workspace 注册表状态或机器本地路径状态

#### 场景：不自动修复的报告
- **WHEN** doctor 发现问题时
- **THEN** 它应报告它能找到的所有问题
- **AND** 不应自动修复 workspace 状态

#### 场景：使用可读的人类输出
- **WHEN** doctor 打印人类可读输出时
- **THEN** 它应显示可读的 workspace 摘要、链接的 repository 或文件夹以及存在的问题（如果有）
- **AND** 应避免打印原始 JSON 或依赖僵硬的 YAML 转储作为默认的人类体验

### 需求：可脚本化的 workspace 设置命令
OpenSpec 应为直接的 workspace 设置命令提供 JSON 输出。

#### 场景：请求 JSON 输出
- **WHEN** 用户向直接的 workspace 设置命令传递 `--json`
- **THEN** OpenSpec 应打印机器可读的输出
- **AND** 输出应避免额外的人类可读文本
- **AND** 输出应将主要对象与结构化的 `status` 条目分开

#### 场景：设置 JSON 需要非交互式设置
- **WHEN** 用户运行 `openspec workspace setup --json` 而不带 `--no-interactive`
- **THEN** OpenSpec 应清晰地失败
- **AND** 应说明 `workspace setup --json` 需要 `--no-interactive`

#### 场景：JSON 输出禁用提示
- **WHEN** 直接的 workspace 设置命令以 `--json` 运行
- **THEN** OpenSpec 应避免交互式提示
- **AND** 当必需的选择不明确时，应失败并输出结构化状态

#### 场景：JSON 状态条目格式
- **WHEN** 直接的 workspace 设置命令在 JSON 输出中报告警告、错误或建议修复时
- **THEN** 每个状态条目应包含稳定的 `code`、`severity` 和人类可读的 `message`
- **AND** 当特定对象字段或建议命令有用时，状态条目可以包含 `target` 和 `fix` 字段

#### 场景：JSON 对象状态格式
- **WHEN** 直接的 workspace 设置命令为 workspace、链接或列表对象输出 JSON 时
- **THEN** 每个对象可以包含一个 `status` 数组，用于对象特定的警告或错误
- **AND** 顶层响应应包含一个 `status` 数组，用于命令级别的警告或错误
- **AND** 健康的对象和健康的响应应使用空的 `status` 数组

#### 场景：支持 JSON 输出的命令
- **WHEN** 用户运行 `workspace setup --no-interactive`、`workspace list`、`workspace link`、`workspace relink` 或 `workspace doctor`
- **THEN** 每个命令应支持 JSON 输出
