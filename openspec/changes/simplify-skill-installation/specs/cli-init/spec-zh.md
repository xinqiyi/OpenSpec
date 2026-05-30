## 目的

init 命令应提供简化设置体验，自动检测工具并使用智能默认值，让用户在一分钟内完成第一个变更。

## 修改后的需求

### 需求：按工具生成技能（替换固定的 9 技能要求）
init 命令应根据活跃配置文件生成技能，而不是固定的集合。

#### 场景：核心配置文件技能生成
- **WHEN** 用户使用配置文件 `core` 运行 init
- **THEN** 系统应为 CORE_WORKFLOWS 常量中的工作流生成技能：propose、explore、apply、archive
- **THEN** 系统不应为配置文件之外的工作流生成技能

#### 场景：自定义配置文件技能生成
- **WHEN** 用户使用配置文件 `custom` 运行 init
- **THEN** 系统仅应为配置 `workflows` 数组中列出的工作流生成技能

#### 场景：在技能模板中包含 Propose 工作流
- **WHEN** 生成技能
- **THEN** 系统应将 `propose` 工作流作为可用技能模板包含在内

### 需求：按工具生成命令（替换固定的 9 命令要求）
init 命令应根据配置文件 AND 交付设置生成命令。

#### 场景：仅技能交付
- **WHEN** 交付设置为 `skills`
- **THEN** 系统不应生成任何命令文件

#### 场景：仅命令交付
- **WHEN** 交付设置为 `commands`
- **THEN** 系统不应生成任何技能文件

#### 场景：两者交付
- **WHEN** 交付设置为 `both`
- **THEN** 系统应为配置文件工作流同时生成技能和命令文件

#### 场景：在命令模板中包含 Propose 工作流
- **WHEN** 生成命令
- **THEN** 系统应将 `propose` 工作流作为可用命令模板包含在内

### 需求：工具自动检测
init 命令应通过扫描项目根目录中的配置目录来检测已安装的 AI 工具。

#### 场景：从目录检测
- **WHEN** 扫描工具
- **THEN** 系统应检查与每个受支持 AI 工具配置目录匹配的目录（例如 `.claude/`、`.cursor/`、`.windsurf/`）
- **THEN** 所有具有匹配目录的工具都应作为已检测返回

#### 场景：检测覆盖所有受支持的工具
- **WHEN** 扫描工具
- **THEN** 系统应检查所有在受支持工具配置中定义的、具有配置目录的工具

#### 场景：未检测到工具
- **WHEN** 项目根目录中没有工具配置目录存在
- **THEN** 系统应返回空的已检测工具列表

### 需求：智能默认值初始化流程
init 命令应使用合理的默认值和工具确认，最小化所需的用户输入。

#### 场景：使用检测到的工具初始化（交互式）
- **WHEN** 用户以交互方式运行 `openspec init` 且检测到工具目录
- **THEN** 系统应显示预选的检测工具
- **THEN** 系统应要求确认（而非完整选择）
- **THEN** 系统应使用默认配置文件（`core`）和交付方式（`both`）

#### 场景：未检测到工具时初始化（交互式）
- **WHEN** 用户以交互方式运行 `openspec init` 且未检测到工具目录
- **THEN** 系统应提示选择工具
- **THEN** 系统应使用默认配置文件（`core`）和交付方式（`both`）

#### 场景：检测到工具时非交互式
- **WHEN** 用户以非交互方式运行 `openspec init`（例如在 CI 中）
- **AND** 检测到工具目录
- **THEN** 系统应自动使用检测到的工具而不提示
- **THEN** 系统应使用默认配置文件和交付方式

#### 场景：未检测到工具时非交互式
- **WHEN** 用户以非交互方式运行 `openspec init`
- **AND** 未检测到工具目录
- **THEN** 系统应以退出码 1 失败
- **AND** 显示使用 `--tools` 标志的消息

#### 场景：显式指定工具时非交互式
- **WHEN** 用户运行 `openspec init --tools claude`
- **THEN** 系统应使用指定的工具
- **THEN** 系统不应提示任何输入

#### 场景：显式指定工具时交互式
- **WHEN** 用户以交互方式运行 `openspec init --tools claude`
- **THEN** 系统应使用指定的工具（忽略自动检测）
- **THEN** 系统不应提示选择工具
- **THEN** 系统应以默认配置文件和交付方式继续

#### 场景：初始化成功消息（propose 已安装）
- **WHEN** init 成功完成
- **AND** `propose` 在活跃配置文件中
- **THEN** 系统应显示适合工具的成功消息
- **THEN** 对于使用冒号语法的工具（Claude Code）："Start your first change: /opsx:propose \"your idea\""
- **THEN** 对于使用连字符语法的工具（Cursor 等）："Start your first change: /opsx-propose \"your idea\""

#### 场景：初始化成功消息（propose 未安装，new 已安装）
- **WHEN** init 成功完成
- **AND** `propose` 不在活跃配置文件中
- **AND** `new` 在活跃配置文件中
- **THEN** 对于使用冒号语法的工具："Start your first change: /opsx:new \"your idea\""
- **THEN** 对于使用连字符语法的工具："Start your first change: /opsx-new \"your idea\""

#### 场景：初始化成功消息（既无 propose 也无 new）
- **WHEN** init 成功完成
- **AND** 活跃配置文件中既没有 `propose` 也没有 `new`
- **THEN** 系统应显示："Done. Run 'openspec config profile' to configure your workflows."

### 需求：Init 在现有项目上执行迁移
init 命令应在重新初始化现有项目时执行一次性迁移，使用与 update 命令相同的共享迁移逻辑。

#### 场景：在现有项目上重新初始化（未设置配置文件）
- **WHEN** 用户在具有现有工作流文件的项目上运行 `openspec init`
- **AND** 全局配置不包含 `profile` 字段
- **THEN** 系统应在继续之前执行一次性迁移（参见 `specs/cli-update/spec.md`）
- **THEN** 系统应使用迁移后的配置继续 init

#### 场景：在新项目上初始化（无现有工作流）
- **WHEN** 用户在没有现有工作流文件的项目上运行 `openspec init`
- **AND** 全局配置不包含 `profile` 字段
- **THEN** 系统不应执行迁移
- **THEN** 系统应使用 `core` 配置文件默认值

### 需求：Init 遵循全局配置
init 命令应读取并应用全局配置中的设置。

#### 场景：用户有配置文件偏好
- **WHEN** 全局配置包含带有自定义工作流的 `profile: "custom"`
- **THEN** init 应安装自定义配置文件工作流

#### 场景：用户有交付偏好
- **WHEN** 全局配置包含 `delivery: "skills"`
- **THEN** init 应仅安装技能文件，而非命令

#### 场景：通过标志覆盖
- **WHEN** 用户运行 `openspec init --profile core`
- **THEN** 系统应使用标志值而非配置值
- **THEN** 系统不应更新全局配置

#### 场景：无效的配置文件覆盖
- **WHEN** 用户运行 `openspec init --profile <invalid>`
- **AND** `<invalid>` 不是 `core` 或 `custom` 之一
- **THEN** 系统应以退出码 1 退出
- **THEN** 系统应显示验证错误，列出允许的配置文件值

### 需求：Init 应用配置的配置文件无需确认
init 命令应直接应用已解析的配置文件（`--profile` 覆盖或全局配置），无需提示确认。

#### 场景：使用自定义配置文件初始化（交互式）
- **WHEN** 用户以交互方式运行 `openspec init`
- **AND** 全局配置指定了带有工作流的 `profile: "custom"`
- **THEN** 系统应直接使用自定义配置文件工作流
- **AND** 系统不应显示配置文件确认提示

#### 场景：使用自定义配置文件非交互式初始化
- **WHEN** 用户以非交互方式运行 `openspec init`
- **AND** 全局配置指定了自定义配置文件
- **THEN** 系统应在无确认的情况下继续

#### 场景：使用核心配置文件初始化
- **WHEN** 用户以交互方式运行 `openspec init`
- **AND** 配置文件是 `core`（默认）
- **THEN** 系统应直接继续，无需配置文件确认提示

### 需求：Init 保留现有工作流
init 命令不应移除已安装的工作流，但应遵循交付设置。

#### 场景：现有自定义安装
- **WHEN** 用户具有带有额外工作流的自定义配置文件，并使用核心配置文件运行 `openspec init`
- **THEN** 系统不应移除额外的工作流
- **THEN** 系统应重新生成核心工作流文件，用最新模板覆盖现有内容

#### 场景：使用不同交付设置的 Init
- **WHEN** 用户在现有项目上运行 `openspec init`
- **AND** 交付设置与已安装的不同（例如，之前是 `both`，现在是 `skills`）
- **THEN** 系统应生成匹配当前交付设置的文件
- **THEN** 系统应删除不匹配交付的文件（例如，如果设置为 `skills` 则移除命令）
- **THEN** 这适用于所有工作流，包括配置文件中没有的额外工作流

#### 场景：即使模板是最新的，重新初始化也应用交付清理
- **WHEN** 用户在现有项目上运行 `openspec init`
- **AND** 现有文件已经是最新模板版本
- **AND** 自上次初始化以来交付已更改
- **THEN** 系统仍应删除不再匹配交付的文件
- **THEN** 例如，从 `both` 切换到 `skills` 应删除生成的命令文件

### 需求：Init 工具确认用户体验
init 命令应显示检测到的工具并要求确认。

#### 场景：确认提示
- **WHEN** 在交互模式下检测到工具
- **THEN** 系统应显示："Detected: Claude Code, Cursor"
- **THEN** 系统应显示预选的复选框以供确认
- **THEN** 系统应允许用户取消选择不需要的工具
