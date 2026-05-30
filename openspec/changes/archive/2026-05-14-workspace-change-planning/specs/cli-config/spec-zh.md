## 新增需求

### 需求：配置配置档案适用于当前工作区
`openspec config profile` 命令应保持全局性，同时在 OpenSpec 工作区内运行时提供显式的工作区应用路径。

#### 场景：在工作区内运行配置档案
- **给定** 命令从 OpenSpec 工作区内部运行
- **当** 用户使用交互式 `openspec config profile` 更改档案或交付设置
- **那么** OpenSpec 应保存全局配置更改
- **并且** 应提示："立即将这些更改应用于此工作区？"

#### 场景：用户确认工作区应用
- **给定** `openspec config profile` 在工作区内更改了全局档案或交付设置
- **当** 用户确认工作区应用提示
- **那么** OpenSpec 应对当前工作区运行 `openspec workspace update`
- **并且** 不应运行仓库本地的 `openspec update`，除非当前规划中心是仓库本地

#### 场景：用户拒绝工作区应用
- **给定** `openspec config profile` 在工作区内更改了全局档案或交付设置
- **当** 用户拒绝工作区应用提示
- **那么** OpenSpec 应说明全局配置已更新
- **并且** 应告知用户稍后运行 `openspec workspace update` 以将档案应用于工作区本地的技能
- **并且** 不应修改工作区技能文件

#### 场景：在工作区内无操作
- **给定** 命令从 OpenSpec 工作区内部运行
- **当** `openspec config profile` 退出时没有有效的配置更改
- **那么** OpenSpec 不应提示应用更改
- **并且** 如果工作区本地技能与当前全局档案不同步应发出警告
- **并且** 警告应建议运行 `openspec workspace update`

#### 场景：在工作区内使用核心预设快捷方式
- **给定** 命令从 OpenSpec 工作区内部运行
- **当** 用户运行 `openspec config profile core`
- **那么** OpenSpec 应保存全局配置更改而不提示立即应用
- **并且** 应告知用户运行 `openspec workspace update` 以将档案应用于工作区本地的技能

#### 场景：在仓库项目内使用核心预设快捷方式
- **给定** 命令从仓库本地的 OpenSpec 项目内部运行
- **当** 用户运行 `openspec config profile core`
- **那么** OpenSpec 应保留现有的仓库本地快捷方式行为
- **并且** 应告知用户运行 `openspec update` 以将档案应用于项目文件

#### 场景：工作区规划中心优先于链接的仓库项目
- **给定** 命令在工作区规划中心下的路径中运行，而该位置也可能检测到仓库本地的 OpenSpec 项目
- **当** OpenSpec 决定显示哪个应用提示
- **那么** 最近的当前规划中心应决定是否提供 `openspec workspace update` 或仓库本地的 `openspec update`
- **并且** 当当前规划中心是工作区时，OpenSpec 不应将档案更改应用于链接的仓库

#### 场景：链接的仓库保持仓库本地的档案行为
- **给定** 仓库本地的 OpenSpec 项目被注册为工作区链接
- **并且** 命令从该链接仓库内部运行，而不是从工作区规划中心运行
- **当** OpenSpec 决定显示哪个应用提示或指导
- **那么** OpenSpec 应为该仓库保留仓库本地的 `openspec update` 行为
- **并且** 除非显式选择了工作区，否则不应提供 `openspec workspace update`
