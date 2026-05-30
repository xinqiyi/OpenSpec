## 新增需求

### 需求：配置配置档案适用于当前 workspace
`openspec config profile` 命令应保持全局性，同时在 OpenSpec workspace 内运行时提供显式的 workspace 应用路径。

#### 场景：在 workspace 内运行配置档案
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** 用户使用交互式 `openspec config profile` 更改档案或交付设置
- **THEN** OpenSpec 应保存全局配置更改
- **AND** 应提示："立即将这些更改应用于此 workspace？"

#### 场景：用户确认 workspace 应用
- **GIVEN** `openspec config profile` 在 workspace 内更改了全局档案或交付设置
- **WHEN** 用户确认 workspace 应用提示
- **THEN** OpenSpec 应对当前 workspace 运行 `openspec workspace update`
- **AND** 不应运行 repository 本地的 `openspec update`，除非当前 planning 中心是 repository 本地

#### 场景：用户拒绝 workspace 应用
- **GIVEN** `openspec config profile` 在 workspace 内更改了全局档案或交付设置
- **WHEN** 用户拒绝 workspace 应用提示
- **THEN** OpenSpec 应说明全局配置已更新
- **AND** 应告知用户稍后运行 `openspec workspace update` 以将档案应用于 workspace 本地的 skill
- **AND** 不应修改 workspace skill 文件

#### 场景：在 workspace 内无操作
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** `openspec config profile` 退出时没有有效的配置更改
- **THEN** OpenSpec 不应提示应用更改
- **AND** 如果 workspace 本地 skill 与当前全局档案不同步应发出警告
- **AND** 警告应建议运行 `openspec workspace update`

#### 场景：在 workspace 内使用核心预设快捷方式
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** 用户运行 `openspec config profile core`
- **THEN** OpenSpec 应保存全局配置更改而不提示立即应用
- **AND** 应告知用户运行 `openspec workspace update` 以将档案应用于 workspace 本地的 skill

#### 场景：在 repository 项目内使用核心预设快捷方式
- **GIVEN** 命令从 repository 本地的 OpenSpec 项目内部运行
- **WHEN** 用户运行 `openspec config profile core`
- **THEN** OpenSpec 应保留现有的 repository 本地快捷方式行为
- **AND** 应告知用户运行 `openspec update` 以将档案应用于项目文件

#### 场景：workspace planning 中心优先于链接的 repository 项目
- **GIVEN** 命令在 workspace planning 中心下的路径中运行，而该位置也可能检测到 repository 本地的 OpenSpec 项目
- **WHEN** OpenSpec 决定显示哪个应用提示
- **THEN** 最近的当前 planning 中心应决定是否提供 `openspec workspace update` 或 repository 本地的 `openspec update`
- **AND** 当当前 planning 中心是 workspace 时，OpenSpec 不应将档案更改应用于链接的 repository

#### 场景：链接的 repository 保持 repository 本地的档案行为
- **GIVEN** repository 本地的 OpenSpec 项目被注册为 workspace 链接
- **AND** 命令从该链接 repository 内部运行，而不是从 workspace planning 中心运行
- **WHEN** OpenSpec 决定显示哪个应用提示或指导
- **THEN** OpenSpec 应为该 repository 保留 repository 本地的 `openspec update` 行为
- **AND** 除非显式选择了 workspace，否则不应提供 `openspec workspace update`
