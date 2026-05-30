# workspace-links spec

## 目的
定义管理跨 repository 和文件夹的 OpenSpec workspace 时，直接 workspace 设置、发现、链接、重新链接、健康检查和 JSON 输出行为。

## 要求
### 要求：引导式 workspace 设置
OpenSpec 应为开始 workspace planning 的用户提供引导式设置流程。

#### 场景：通过设置创建 workspace
- **WHEN** 用户运行 `openspec workspace setup`
- **THEN** OpenSpec 应引导用户创建 OpenSpec workspace
- **AND** workspace 应使用 workspace 基础所规定的标准 workspace 位置

#### 场景：先询问 workspace 名称
- **WHEN** 交互式设置开始时
- **THEN** OpenSpec 应在询问 repository 或文件夹之前先询问 workspace 名称
- **AND** workspace 名称应使用 kebab-case 格式，包含小写字母、数字和连字符

#### 场景：设置过程中重试无效的 workspace 名称
- **WHEN** 交互式用户输入无效的 workspace 名称时
- **THEN** OpenSpec 应解释 workspace 名称必须为 kebab-case 格式
- **AND** 应在继续设置之前让用户输入另一个 workspace 名称

#### 场景：链接所需的第一个 repository 或文件夹
- **WHEN** 设置询问 repository 或文件夹时
- **THEN** 用户应提供至少一个现有的 repository 或文件夹路径
- **AND** 在链接至少一个路径之前，设置不应成功完成

#### 场景：设置过程中推断链接名称
- **WHEN** 用户在设置过程中提供 repository 或文件夹路径时
- **THEN** OpenSpec 应从文件夹的基本名称推断链接名称
- **AND** 仅当推断的名称冲突时才询问不同的名称

#### 场景：处理设置过程中推断的链接名称冲突
- **GIVEN** 设置推断的链接名称已存在于 workspace 中
- **WHEN** 设置是交互式时
- **THEN** OpenSpec 应显示冲突的链接名称和该链接的现有路径
- **AND** 应在继续之前要求用户提供不同的链接名称

#### 场景：保留文件夹风格的链接名称
- **WHEN** OpenSpec 接受 workspace 链接名称时
- **THEN** 应允许在 workspace 基础链接名称规则下有效的文件夹风格名称
- **AND** 不应要求链接名称使用更严格的 workspace 名称 kebab-case 规则

#### 场景：设置过程中添加多个 repository 或文件夹
- **WHEN** 设置链接一个 repository 或文件夹时
- **THEN** OpenSpec 应让用户通过简单的重复提示添加另一个 repository 或文件夹
- **AND** 每个链接的路径应被记录而不编辑目标 repository 或文件夹

#### 场景：设置过程中存储已验证的绝对路径
- **WHEN** 设置链接一个 repository 或文件夹路径时
- **THEN** OpenSpec 应验证该路径解析到现有文件夹
- **AND** 应在机器本地状态中存储绝对运行时本地路径，而非原始用户输入
- **AND** 相对输入应相对于命令的当前工作目录进行解析

#### 场景：保留设置链接路径中的等号
- **WHEN** 非交互式设置收到一个 `--link` 值，该值解析到现有文件夹且包含 `=`
- **THEN** OpenSpec 应将完整值视为路径
- **AND** 应从文件夹基本名称推断链接名称
- **AND** 显式的 `--link <name>=<path>` 输入应保留 `<path>` 中的 `=` 字符

#### 场景：使用非交互式输入运行设置
- **WHEN** `openspec workspace setup --no-interactive` 收到一个 workspace 名称和至少一个有效链接
- **THEN** OpenSpec 应创建 workspace，无需提示
- **AND** 应支持重复的 `--link` 值

#### 场景：非交互式设置重复的链接名称
- **WHEN** `openspec workspace setup --no-interactive` 收到两个具有相同推断或显式名称的链接
- **THEN** OpenSpec 应失败并显示清晰的重复杂链接名称错误
- **AND** 错误应显示冲突的链接名称和第一个使用该名称的路径
- **AND** 应建议使用不同名称的显式 `--link <name>=<path>` 值

#### 场景：非交互式设置缺失输入
- **WHEN** `openspec workspace setup --no-interactive` 缺少 workspace 名称或链接
- **THEN** OpenSpec 应失败并显示清晰的消息
- **AND** 应解释哪些标志是必需的

#### 场景：完成设置
- **WHEN** 设置完成时
- **THEN** OpenSpec 应显示 workspace 位置、planning 路径和链接的 repository 或文件夹
- **AND** 应检查当前机器可以解析的内容

#### 场景：本地记录已创建的 workspace
- **WHEN** 设置创建 workspace 时
- **THEN** OpenSpec 应在本地 workspace 注册表中记录该 workspace
- **AND** workspace 文件夹应保持为 workspace 状态的真实依据

#### 场景：设置过程中重用已有的 workspace 名称
- **GIVEN** 具有请求名称的受管理 workspace 已存在
- **WHEN** 用户使用该 workspace 名称运行设置时
- **THEN** OpenSpec 应解释该 workspace 已存在
- **AND** 不应覆盖现有 workspace

### 要求：workspace 发现
OpenSpec 应让用户查看当前机器上可用的 OpenSpec 受管理 workspace。

#### 场景：列出售 workspace
- **WHEN** 用户运行 `openspec workspace list`
- **THEN** OpenSpec 应列出已知的受管理 workspace
- **AND** 每个 workspace 应包含 workspace 名称、workspace 位置和链接的 repository 或文件夹

#### 场景：使用简短列出命令
- **WHEN** 用户运行 `openspec workspace ls`
- **THEN** OpenSpec 的行为应与 `openspec workspace list` 相同

#### 场景：没有 workspace 时列出
- **WHEN** 用户运行 `openspec workspace list`
- **AND** 没有受管理 workspace 存在
- **THEN** OpenSpec 应说明未找到 workspace
- **AND** 应向用户展示如何创建一个

#### 场景：列出过期的注册表条目
- **WHEN** 本地注册表包含一个不再存在的 workspace 位置
- **THEN** `workspace list` 应报告过期的 workspace 条目
- **AND** 应避免静默删除注册表状态
- **AND** 应避免自动重写或修复注册表状态

#### 场景：避免注册表清理命令
- **WHEN** 用户在此切片中检查过期的 workspace 注册表条目时
- **THEN** OpenSpec 应将过期条目视为仅报告的诊断信息
- **AND** 不应暴露诸如 `workspace forget` 之类的注册表清理命令

### 要求：全局 workspace 命令
OpenSpec 应允许 workspace 命令从 workspace 目录之外运行。

#### 场景：通过标志选择 workspace
- **WHEN** 需要某个 workspace 的命令收到 `--workspace <name>`
- **THEN** OpenSpec 应从本地注册表中使用该 workspace
- **AND** 如果 workspace 名称未知，应清晰失败

#### 场景：使用当前 workspace
- **GIVEN** 命令从 workspace 文件夹或子目录运行
- **WHEN** 命令需要一个 workspace 且未提供 `--workspace` 标志时
- **THEN** OpenSpec 应使用当前 workspace

#### 场景：使用未注册的当前 workspace
- **GIVEN** 命令从有效的 workspace 文件夹或子目录运行
- **AND** 该 workspace 未在本地 workspace 注册表中记录
- **WHEN** 命令需要一个 workspace 且未提供 `--workspace <name>` 标志时
- **THEN** OpenSpec 应使用当前 workspace
- **AND** 应包含一个非致命警告状态，代码为 `workspace_not_in_local_registry`
- **AND** 警告应解释用户如何让该 workspace 在本地注册

#### 场景：变更操作后注册未注册的当前 workspace
- **GIVEN** 一个变更型 workspace 命令使用一个不在本地 workspace 注册表中记录的有效当前 workspace
- **WHEN** `workspace link` 或 `workspace relink` 成功时
- **THEN** OpenSpec 应将 workspace 名称和位置记录在本地 workspace 注册表中

#### 场景：Doctor 不注册当前 workspace
- **GIVEN** `workspace doctor` 使用一个不在本地 workspace 注册表中记录的有效当前 workspace
- **WHEN** doctor 完成时
- **THEN** OpenSpec 应报告非致命的注册表警告
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
- **WHEN** 使用 `--json` 运行的命令需要一个 workspace 且未指定时
- **THEN** OpenSpec 应失败而不显示选择器
- **AND** 应输出结构化的状态错误
- **AND** 应建议传递 `--workspace <name>`

#### 场景：需要 workspace 的命令没有已知 workspace
- **GIVEN** 本地注册表中没有已知 workspace
- **AND** 命令不是从 workspace 文件夹或子目录运行
- **WHEN** `workspace link`、`workspace relink`、`workspace doctor` 或其他需要一个 workspace 的命令在没有 `--workspace <name>` 的情况下运行时
- **THEN** OpenSpec 应失败而不显示选择器，无论交互 schema 如何
- **AND** 应输出 `未找到已知的 OpenSpec workspace。请先运行 'openspec workspace setup'。`
- **AND** 应解释在至少一个 workspace 本地已知后可以使用 `--workspace <name>`

### 要求：workspace 链接
OpenSpec 应让用户在创建变更之前将现有 repository 或文件夹链接到 workspace。

#### 场景：使用推断名称链接
- **WHEN** 用户运行 `openspec workspace link <path>`
- **THEN** OpenSpec 应从文件夹基本名称推断链接名称
- **AND** 应将已验证的绝对本地路径存储为机器本地状态

#### 场景：使用显式名称链接
- **WHEN** 用户运行 `openspec workspace link <name> <path>`
- **THEN** OpenSpec 应使用显式链接名称进行 planning
- **AND** 应将已验证的绝对本地路径存储为机器本地状态

#### 场景：要求路径存在
- **WHEN** 用户链接 repository 或文件夹路径时
- **THEN** 该路径应在当前机器上存在
- **AND** OpenSpec 应拒绝缺失的路径并给出清晰的消息

#### 场景：存储前解析链接路径
- **WHEN** 用户链接 repository 或文件夹路径时
- **THEN** OpenSpec 应存储当前运行时的已验证绝对路径
- **AND** 相对输入应相对于命令的当前工作目录进行解析
- **AND** OpenSpec 不应在原生 Windows、WSL2 和 Unix 运行时之间转换路径

#### 场景：链接单体 repository 文件夹
- **WHEN** 用户链接单体 repository 内的包、服务、应用或目录时
- **THEN** OpenSpec 应将其存储为 workspace 链接
- **AND** 不应要求该文件夹拥有自己的 repository 本地 `openspec/` 目录

#### 场景：链接没有 repository 本地 OpenSpec 的路径
- **WHEN** 用户链接不包含 repository 本地 OpenSpec 状态的路径时
- **THEN** OpenSpec 应保持该 repository 或文件夹可用于 workspace planning
- **AND** 不应将缺少 repository 本地 OpenSpec 状态视为链接失败

#### 场景：仅记录链接
- **WHEN** 用户链接 repository 或文件夹时
- **THEN** OpenSpec 应记录 workspace 状态和本地路径状态
- **AND** 不应在链接的 repository 或文件夹中创建、复制、移动、初始化或编辑文件

#### 场景：本地状态无效时阻止链接
- **GIVEN** workspace 机器本地状态文件存在但无法解析或验证
- **WHEN** 用户运行 `openspec workspace link`
- **THEN** OpenSpec 应失败，状态代码为 `workspace_local_state_invalid`
- **AND** 不应重写共享 workspace 状态或机器本地路径状态

#### 场景：重复使用链接名称
- **GIVEN** workspace 已有一个具有给定名称的链接
- **WHEN** 用户尝试以相同名称链接另一个路径时
- **THEN** OpenSpec 应解释该链接名称已被另一个链接使用
- **AND** 应显示现有的链接名称和现有路径
- **AND** 应建议选择不同的链接名称
- **AND** 当用户意图更改现有链接路径时，应建议 `workspace relink <name> <path>`
- **AND** 应保留现有链接，除非用户显式重新链接它

### 要求：workspace 重新链接
OpenSpec 应让用户更新现有链接路径，而无需重新创建 workspace。

#### 场景：更新本地路径
- **GIVEN** workspace 有一个链接
- **WHEN** 用户运行 `openspec workspace relink <name> <path>`
- **THEN** OpenSpec 应保持稳定的链接名称
- **AND** 应将当前机器的机器本地路径更新为已验证的绝对路径

#### 场景：要求重新链接路径存在
- **WHEN** 用户重新链接到新路径时
- **THEN** 新路径应在当前机器上存在
- **AND** OpenSpec 应拒绝缺失的路径并给出清晰的消息

#### 场景：存储前解析重新链接路径
- **WHEN** 用户重新链接到新路径时
- **THEN** OpenSpec 应存储当前运行时的已验证绝对路径
- **AND** 相对输入应相对于命令的当前工作目录进行解析

#### 场景：本地状态无效时阻止重新链接
- **GIVEN** workspace 机器本地状态文件存在但无法解析或验证
- **WHEN** 用户运行 `openspec workspace relink`
- **THEN** OpenSpec 应失败，状态代码为 `workspace_local_state_invalid`
- **AND** 不应重写机器本地路径状态

#### 场景：更新未知链接
- **WHEN** 用户尝试重新链接一个不存在的链接时
- **THEN** OpenSpec 应解释该链接名称未知
- **AND** 应保留现有 workspace 状态

#### 场景：避免所有者与交接字段
- **WHEN** 用户在此切片中链接或重新链接 repository 或文件夹时
- **THEN** OpenSpec 不应询问所有者或交接元数据
- **AND** 链接维护应聚焦于名称和本地路径

### 要求：workspace 健康检查
OpenSpec 应解释当前机器可以对 workspace 解析哪些内容。

#### 场景：Doctor 检查一个选定的 workspace
- **WHEN** 用户运行 `openspec workspace doctor`
- **THEN** OpenSpec 应检查一个选定的 workspace
- **AND** 默认不应扫描本地注册表中的每个已知 workspace

#### 场景：Doctor 推断当前 workspace
- **GIVEN** 命令从 workspace 文件夹或子目录运行
- **WHEN** 用户运行不带 `--workspace <name>` 的 `openspec workspace doctor`
- **THEN** OpenSpec 应检查当前 workspace

#### 场景：检查健康 workspace
- **WHEN** 用户运行 `openspec workspace doctor`
- **THEN** OpenSpec 应显示 workspace 位置和 workspace planning 路径
- **AND** 应显示链接的 repository 或文件夹以及哪些路径在当前机器上可解析

#### 场景：选定的 workspace 位置缺失
- **GIVEN** 选定的 workspace 来自本地注册表
- **AND** 已注册的 workspace 位置缺失或无效
- **WHEN** 用户运行 `openspec workspace doctor`
- **THEN** OpenSpec 应报告选定 workspace 的状态错误
- **AND** 不应尝试检查该 workspace 的链接

#### 场景：报告 repository 本地 specs 路径
- **WHEN** 链接的 repository 或文件夹可解析时
- **THEN** doctor 应在 repository 本地 `openspec/specs` 存在时报告 `repo_specs_path`
- **AND** 当 repository 本地 specs 不存在时报告 `repo_specs_path: null`

#### 场景：检查缺失路径
- **WHEN** 链接指向当前机器上缺失的路径时
- **THEN** doctor 应标识受影响的链接名称
- **AND** 应包含建议的 `workspace relink` 修复

#### 场景：检查共享状态与本地状态的漂移
- **WHEN** 共享 workspace 状态与机器本地路径状态不一致时
- **THEN** doctor 应解释哪些链接名称受影响
- **AND** 应区分共享 workspace 链接和仅本地路径

#### 场景：报告无效的本地状态
- **WHEN** list 或 doctor 读取一个机器本地状态文件无法解析或验证的 workspace 时
- **THEN** OpenSpec 应报告状态代码 `workspace_local_state_invalid`
- **AND** 应避免将无效的本地状态视为空路径映射用于变更或修复建议
- **AND** 不应重写 workspace 注册表状态或机器本地路径状态

#### 场景：报告而不自动修复
- **WHEN** doctor 发现问题时
- **THEN** 应报告它能找到的所有问题
- **AND** 不应自动修复 workspace 状态

#### 场景：使用可读的人类输出
- **WHEN** doctor 输出人类可读内容时
- **THEN** 应显示可读的 workspace 摘要、链接的 repository 或文件夹以及存在的问题（如有）
- **AND** 应避免将原始 JSON 或依赖严格 YAML 转储作为默认的人类体验

### 要求：可脚本化的 workspace 设置命令
OpenSpec 应为直接 workspace 设置命令提供 JSON 输出。

#### 场景：请求 JSON 输出
- **WHEN** 用户向直接 workspace 设置命令传递 `--json`
- **THEN** OpenSpec 应输出机器可读的内容
- **AND** 输出应避免多余的人类可读文本
- **AND** 输出应将主要对象与结构化的 `status` 条目分开

#### 场景：设置 JSON 需要非交互式设置
- **WHEN** 用户运行 `openspec workspace setup --json` 但不加 `--no-interactive`
- **THEN** OpenSpec 应清晰失败
- **AND** 应解释 `workspace setup --json` 需要 `--no-interactive`

#### 场景：JSON 输出禁用提示
- **WHEN** 直接 workspace 设置命令以 `--json` 运行时
- **THEN** OpenSpec 应避免交互式提示
- **AND** 当所需选择不明确时，应以结构化状态输出失败

#### 场景：JSON 状态条目形态
- **WHEN** 直接 workspace 设置命令在 JSON 输出中报告警告、错误或建议修复时
- **THEN** 每个状态条目应包含稳定的 `code`、`severity` 和人类可读的 `message`
- **AND** 当特定对象字段或建议命令有用时，状态条目可以包含 `target` 和 `fix` 字段

#### 场景：JSON 对象状态形态
- **WHEN** 直接 workspace 设置命令为 workspace、链接或列表对象输出 JSON 时
- **THEN** 每个对象可以包含一个 `status` 数组，用于对象特定的警告或错误
- **AND** 顶级响应应包含一个 `status` 数组，用于命令级别的警告或错误
- **AND** 健康对象和健康响应应使用空的 `status` 数组

#### 场景：带 JSON 输出的命令
- **WHEN** 用户运行 `workspace setup --no-interactive`、`workspace list`、`workspace link`、`workspace relink` 或 `workspace doctor`
- **THEN** 每个命令应支持 JSON 输出

### 要求：workspace 设置安装 agent skill
OpenSpec 应让用户在 workspace 设置期间将 OpenSpec agent skill 安装到 workspace。

#### 场景：提示选择 workspace agent skill
- **WHEN** 交互式 workspace 设置到达 agent skill 安装步骤时
- **THEN** OpenSpec 应询问哪些 agent 应在该 workspace 中获得 OpenSpec skill
- **AND** 提示应使用"agent skill"语言而非"AI 工具"语言

#### 场景：预选首选开启器
- **GIVEN** 用户选择了支持 OpenSpec skill 生成的首选开启器
- **WHEN** 交互式 workspace 设置询问哪些 agent 应获得 skill 时
- **THEN** OpenSpec 应预选中匹配的 agent
- **AND** 用户应能够选择额外 agent 或取消预选已选 agent

#### 场景：安装选定的 workspace skill
- **WHEN** workspace 设置完成时选择了至少一个 agent
- **THEN** OpenSpec 应在 workspace 根目录下为每个选定的 agent 生成或刷新 OpenSpec skill 文件
- **AND** 应报告哪些 agent 获得了 skill
- **AND** 应将选定的 agent 存储在 workspace 本地机器状态中

#### 场景：安装配置文件选定的 workflow
- **GIVEN** 全局配置解析为某个 workflow 配置文件
- **WHEN** workspace 设置安装 agent skill 时
- **THEN** OpenSpec 应为该配置文件选定的 workflow 安装 workspace 本地 skill
- **AND** 应将 `--tools` 视为 agent 选择，而非 workflow 选择
- **AND** 应记录上次应用的 workflow ID 以用于漂移检测

#### 场景：仅在设置期间安装 skill
- **WHEN** workspace 设置安装 agent skill 时
- **THEN** OpenSpec 应仅生成 skill 文件
- **AND** 不应生成斜杠命令文件或全局命令文件作为 workspace 设置的一部分

#### 场景：workspace 设置忽略命令交付方式
- **GIVEN** 全局配置交付方式为 `commands` 或 `both`
- **WHEN** workspace 设置安装 agent skill 时
- **THEN** OpenSpec 仍应仅生成 workspace 本地 skill
- **AND** 应报告 workspace 命令生成不属于此切片

#### 场景：skill 安装期间保留已链接的 repository
- **WHEN** workspace 设置安装 agent skill 时
- **THEN** OpenSpec 应保持已链接的 repository 和文件夹不变
- **AND** 生成的 skill 应限定在 workspace planning 家园范围内

#### 场景：非交互式设置工具选择
- **WHEN** 非交互式 workspace 设置收到 `--tools all`、`--tools none` 或 `--tools <ids>`
- **THEN** OpenSpec 应使用选定的工具集进行 workspace agent skill 安装
- **AND** 应使用与 repository 初始化 skill 生成相同的受支持工具 ID 来验证工具 ID

#### 场景：非交互式设置未选择工具
- **WHEN** 非交互式 workspace 设置省略 `--tools`
- **THEN** OpenSpec 应创建 workspace 而不安装 agent skill
- **AND** 应报告未安装 workspace skill
- **AND** 应告知用户稍后运行 `openspec workspace update --tools <ids>` 安装 skill

#### 场景：在 JSON 输出中报告设置 skill
- **WHEN** 非交互式 workspace 设置安装 agent skill 且启用 JSON 输出时
- **THEN** OpenSpec 应在机器可读输出中包含已生成、刷新、跳过或失败的 skill 安装结果

### 要求：workspace 更新管理 agent skill
OpenSpec 应提供 workspace 更新流程，用于在设置后刷新 agent skill。

#### 场景：更新当前 workspace
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** 用户运行 `openspec workspace update`
- **THEN** OpenSpec 应更新该当前 workspace

#### 场景：更新命名 workspace
- **GIVEN** 名为 `platform` 的 workspace 在本地已知
- **WHEN** 用户运行 `openspec workspace update platform`
- **THEN** OpenSpec 应更新 `platform` workspace

#### 场景：通过标志更新选定的 workspace
- **GIVEN** 名为 `platform` 的 workspace 在本地已知
- **WHEN** 用户运行 `openspec workspace update --workspace platform`
- **THEN** OpenSpec 应更新 `platform` workspace

#### 场景：更新选定的 workspace skill
- **WHEN** workspace 更新完成且选定了 agent
- **THEN** OpenSpec 应为选定的 agent 刷新 OpenSpec skill
- **AND** 应为新选定的 agent 添加 skill
- **AND** 应移除不再选定的 agent 的 OpenSpec 管理 workflow skill 目录
- **AND** 应更新存储的 workspace 本地选定 agent 列表

#### 场景：识别管理 workflow skill 目录
- **WHEN** workspace 更新评估要移除的 workflow skill 目录时
- **THEN** OpenSpec 仅当目录名称与已知的生成 workflow skill 目录匹配且其 `SKILL.md` 包含 OpenSpec 生成的元数据时，才将其视为 OpenSpec 管理的目录
- **AND** 生成的元数据应包含 OpenSpec skill 生成写入的 `generatedBy` 标记
- **AND** OpenSpec 不应移除缺少生成元数据的目录，即使其名称与已知 workflow skill 目录名称匹配

#### 场景：更新配置文件选定的 workflow
- **GIVEN** 全局配置解析为某个 workflow 配置文件
- **WHEN** workspace 更新刷新 workspace 本地 skill 时
- **THEN** OpenSpec 应将 workspace 本地 skill workflow 集同步到该配置文件选定的 workflow
- **AND** 取消选定的 workflow skill 目录仅在其为已知的 OpenSpec 管理 workflow skill 目录时才被移除
- **AND** 应更新上次用于漂移检测的应用 workflow ID

#### 场景：workspace 更新忽略命令交付方式
- **GIVEN** 全局配置交付方式为 `commands` 或 `both`
- **WHEN** workspace 更新刷新 workspace 本地 skill 时
- **THEN** OpenSpec 仍应仅更新 workspace 本地 skill
- **AND** 不应生成斜杠命令文件或全局命令文件

#### 场景：仅移除受管理的 skill 目录
- **WHEN** workspace 更新为未选定的 agent 移除 skill 时
- **THEN** OpenSpec 应仅移除已知的 OpenSpec 管理 workflow skill 目录
- **AND** 应保留 agent 目录中的不相关文件

#### 场景：通过标志更新存储的 agent 选择
- **WHEN** workspace 更新收到 `--tools <ids>` 或 `--tools none`
- **THEN** OpenSpec 应将存储的 workspace 本地选定 agent 列表替换为该选择
- **AND** 未来不带 `--tools` 的 workspace 更新应使用存储的选择

#### 场景：非交互式更新工具选择
- **WHEN** workspace 更新收到 `--tools all`、`--tools none` 或 `--tools <ids>`
- **THEN** OpenSpec 应使用该选定工具集更新 workspace agent skill
- **AND** 应避免提示选择 agent

#### 场景：非交互式更新未选择工具
- **GIVEN** workspace 本地选定的 agent 已存储
- **WHEN** 非交互式 workspace 更新省略 `--tools`
- **THEN** OpenSpec 应使用活跃的全局配置文件刷新已存储的选定 agent
- **AND** 应避免提示选择 agent

#### 场景：非交互式更新没有存储的选择
- **GIVEN** 未存储 workspace 本地选定的 agent
- **WHEN** 非交互式 workspace 更新省略 `--tools`
- **THEN** OpenSpec 应完成而不安装 agent skill
- **AND** 应报告无操作并提供传递 `--tools` 的指导

#### 场景：报告 workspace skill 漂移
- **GIVEN** workspace 本地 skill 状态记录了上次应用的 workflow ID
- **AND** 活跃的全局配置文件解析为不同的 workflow 集
- **WHEN** OpenSpec 报告 workspace skill 状态时
- **THEN** 应报告 workspace 本地 skill 与全局配置文件不同步
- **AND** 应建议 `openspec workspace update`

#### 场景：报告干净的 workspace skill 同步
- **GIVEN** workspace 本地 skill 状态与活跃的全局配置文件和选定的 agent 匹配
- **WHEN** OpenSpec 报告 workspace skill 状态时
- **THEN** 不应报告配置文件漂移

#### 场景：报告 workspace skill 更新结果
- **WHEN** workspace 更新更改 agent skill 状态时
- **THEN** OpenSpec 应报告哪些 agent 被刷新、添加、移除、跳过或失败

#### 场景：在 JSON 输出中报告 workspace 更新结果
- **WHEN** workspace 更新启用 JSON 输出运行时
- **THEN** OpenSpec 应在机器可读输出中包含已刷新、添加、移除、跳过或失败的 skill 结果

### 要求：workspace skill 更新界面已文档化
OpenSpec 应在面向用户的命令界面中暴露 workspace skill 设置/更新行为。

#### 场景：workspace 更新出现在帮助中
- **WHEN** 用户运行 `openspec workspace --help`
- **THEN** OpenSpec 应列出 `workspace update`
- **AND** 应将其描述为刷新 workspace 本地 agent skill

#### 场景：workspace 更新选项出现在帮助中
- **WHEN** 用户运行 `openspec workspace update --help`
- **THEN** OpenSpec 应文档化 workspace 选择选项
- **AND** 应文档化 `--tools all|none|<ids>`
- **AND** 应说明全局配置文件选择 workflow，`--tools` 选择 agent

#### 场景：workspace 更新出现在自动补全中
- **WHEN** 生成 shell 自动补全时
- **THEN** workspace 命令注册表应包含 `workspace update`
- **AND** 应包含相关选项，如 `--workspace`、`--tools`、`--json` 和 `--no-interactive`
