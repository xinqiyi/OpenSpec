## 目的

配置文件应定义安装哪些 workflow，使新用户能够获得简化的核心体验，同时允许高级用户自定义其 workflow 选择。

## 新增需求

### 需求：配置定义
系统应支持两个 workflow 配置：`core` 和 `custom`。

#### 场景：核心配置内容
- **WHEN** 配置设置为 `core`
- **THEN** 该配置应包含 workflow：`propose`、`explore`、`apply`、`archive`

#### 场景：自定义配置内容
- **WHEN** 配置设置为 `custom`
- **THEN** 该配置应仅包含全局配置 `workflows` 数组中指定的 workflow

### 需求：交付独立于配置
交付设置应控制 workflow 的安装方式（skill、命令或两者兼有），与安装哪些 workflow 分开。

#### 场景：交付选项
- **WHEN** 配置交付时
- **THEN** 系统应支持三个选项：`both`（skill 和命令）、`skills`（仅 skill 文件）、`commands`（仅命令文件）

#### 场景：两者交付
- **WHEN** 交付设置为 `both`
- **THEN** 系统应为每个 workflow 同时安装 skill 文件和命令文件

#### 场景：仅 skill 交付
- **WHEN** 交付设置为 `skills`
- **THEN** 系统应为每个 workflow 仅安装 skill 文件
- **THEN** 系统应不安装命令文件

#### 场景：仅命令交付
- **WHEN** 交付设置为 `commands`
- **THEN** 系统应为每个 workflow 仅安装命令文件
- **THEN** 系统应不安装 skill 文件

#### 场景：带自定义交付的核心配置
- **WHEN** 配置设置为 `core`
- **AND** 交付设置为 `skills`
- **THEN** 系统应将核心 workflow 仅安装为 skill（无命令）

#### 场景：交付默认值
- **WHEN** 全局配置中未设置交付
- **THEN** 系统应默认为 `both`

### 需求：通过交互式选择器进行配置配置
系统应提供用于配置配置的交互式选择器。

#### 场景：交互式配置配置
- **WHEN** 用户运行 `openspec config profile`
- **THEN** 系统应显示交互式选择器，包含：
 - 交付选择：`skills`、`commands`、`both`
 - 所有可用 workflow 的 workflow 开关
- **THEN** 系统应预选当前配置值
- **THEN** 确认后，系统应更新全局配置
- **THEN** 如果选择的 workflow 与核心默认值不同，系统应将配置设置为 `custom`
- **THEN** 如果选择的 workflow 与核心默认值完全匹配（propose、explore、apply、archive），无论交付设置如何，系统应将配置设置为 `core`
- **THEN** 系统应不修改任何项目文件
- **THEN** 系统应显示："配置已更新。在你的项目中运行 `openspec update` 以应用。"

#### 场景：核心预设快捷方式
- **WHEN** 用户运行 `openspec config profile core`
- **THEN** 系统应将配置设置为 `core`
- **THEN** 系统应将 workflow 设置为 `['propose', 'explore', 'apply', 'archive']`
- **THEN** 系统应不更改交付设置（保留用户偏好）
- **THEN** 系统应不修改任何项目文件
- **THEN** 系统应显示："配置已更新。在你的项目中运行 `openspec update` 以应用。"
- **THEN** 新配置将在下次运行 `openspec init` 或 `openspec update` 时生效

#### 场景：在项目内运行配置配置
- **WHEN** 用户在 OpenSpec 项目目录内运行 `openspec config profile`
- **THEN** 更新全局配置后，系统应提示："立即应用于此项目？(y/n)"
- **WHEN** 用户确认时
- **THEN** 系统应自动运行 `openspec update`
- **THEN** 系统仍应显示："在你的其他项目中运行 `openspec update` 以应用。"

#### 场景：配置配置 - 用户拒绝应用
- **WHEN** 用户在 OpenSpec 项目目录内运行 `openspec config profile`
- **AND** 用户拒绝"立即应用于此项目？"提示
- **THEN** 系统应显示："配置已更新。在你的项目中运行 `openspec update` 以应用。"
- **THEN** 系统应成功退出，不修改项目文件

#### 场景：非交互式配置配置
- **WHEN** 用户以非交互方式运行 `openspec config profile`（例如，在 CI 中，无 TTY）
- **THEN** 系统应显示错误："需要交互 schema。使用 `openspec config profile core` 或通过环境变量/标志设置配置。"
- **THEN** 系统应以退出码 1 退出

### 需求：配置设置存储在全局配置中
配置和交付设置应存储在现有的全局配置文件中（`~/.config/openspec/config.json`），与遥测和功能标志一起。

#### 场景：配置 schema
- **WHEN** 读取配置配置时
- **THEN** 配置应包含 `profile`（core|custom）、`delivery`（both|skills|commands）以及可选的 `workflows`（workflow 名称数组）

#### 场景：schema 演进
- **WHEN** 加载没有配置/交付字段的配置时
- **THEN** 系统应使用默认值（profile=core、delivery=both）
- **AND** 现有的配置字段（telemetry、featureFlags）应被保留

#### 场景：配置列表显示配置文件设置
- **WHEN** 用户运行 `openspec config list`
- **THEN** 系统应显示配置、交付和 workflow 设置
- **AND** 应指示哪些值是默认值，哪些是显式设置的

### 需求：配置是全局的，项目是显式的
配置更改不应自动传播到项目。

#### 场景：配置更新不修改项目
- **WHEN** 用户通过 `openspec config profile` 更新配置
- **THEN** 系统应仅更新全局配置（`~/.config/openspec/config.json`）
- **THEN** 系统应不修改任何项目 skill/命令文件
- **THEN** 现有项目保留其当前 workflow 文件，直到用户运行 `openspec update`

### 需求：通过更新命令应用配置更改
现有的 `openspec update` 命令应将当前全局配置应用到项目。有关详细的更新行为，请参见 `specs/cli-update/spec.md`。

#### 场景：配置更改需要显式项目同步
- **WHEN** 用户通过 `openspec config profile` 更新配置或交付
- **THEN** 全局配置应立即更新
- **AND** 项目文件应保持不变，直到对该项目运行 `openspec update`

### 需求：配置默认值
系统应将 `core` 作为新用户的默认配置，同时通过迁移保留现有用户的 workflow。

#### 场景：无全局配置（新用户）
- **WHEN** 全局配置文件不存在
- **AND** 项目中未安装现有 workflow
- **THEN** 系统应表现得如同配置是 `core`

#### 场景：全局配置存在但配置字段缺失（新用户）
- **WHEN** 全局配置文件存在但不包含 `profile` 字段
- **AND** 项目中未安装现有 workflow
- **THEN** 系统应表现得如同配置是 `core`

#### 场景：配置字段缺失但存在现有 workflow（现有用户迁移）
- **WHEN** 全局配置不包含 `profile` 字段
- **AND** `update` 命令检测到项目中的现有 workflow 文件
- **THEN** 系统应执行一次性迁移（详见 `specs/cli-update/spec.md`）
- **THEN** 系统应将配置设置为 `custom`，并使用检测到的 workflow
- **THEN** 系统应在迁移期间不添加或移除任何 workflow 文件
