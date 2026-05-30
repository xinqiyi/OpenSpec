# global-config 规范

## 目的

本规范定义了 OpenSpec 如何解析、读取和写入用户级全局配置。它管理 `src/core/global-config.ts` 模块，该模块为存储用户偏好、功能标志和跨项目持久化设置提供基础。本规范通过遵循 XDG 基本目录规范并配合平台特定的回退策略来确保跨平台兼容性，并通过模式演化规则保证前后兼容性。

## 需求

### 需求：全局配置存储

系统应将全局配置存储在 `~/.config/openspec/config.json` 中，包括包含 `anonymousId` 和 `noticeSeen` 字段的遥测状态。

#### 场景：初始配置创建
- **当** 不存在全局配置文件时
- **并且** 即将发送第一个遥测事件
- **则** 系统创建包含遥测配置的 `~/.config/openspec/config.json`

#### 场景：遥测配置结构
- **当** 读取或写入遥测配置时
- **则** 配置包含一个 `telemetry` 对象，包含 `anonymousId`（字符串 UUID）和 `noticeSeen`（布尔值）字段

#### 场景：配置文件格式
- **当** 存储配置时
- **则** 系统写入有效的 JSON，用户可以读取和修改

#### 场景：保留现有配置
- **当** 向现有配置文件添加遥测字段时
- **则** 系统保留所有现有配置字段

### 需求：全局配置目录路径

系统应遵循 XDG 基本目录规范解析全局配置目录路径，并配合平台特定的回退策略。

#### 场景：设置了 XDG_CONFIG_HOME 的 Unix/macOS
- **当** `$XDG_CONFIG_HOME` 环境变量设置为 `/custom/config`
- **则** `getGlobalConfigDir()` 返回 `/custom/config/openspec`

#### 场景：未设置 XDG_CONFIG_HOME 的 Unix/macOS
- **当** `$XDG_CONFIG_HOME` 环境变量未设置
- **并且** 平台是 Unix 或 macOS
- **则** `getGlobalConfigDir()` 返回 `~/.config/openspec`（展开为绝对路径）

#### 场景：Windows 平台
- **当** 平台是 Windows
- **并且** `%APPDATA%` 设置为 `C:\Users\User\AppData\Roaming`
- **则** `getGlobalConfigDir()` 返回 `C:\Users\User\AppData\Roaming\openspec`

### 需求：全局配置加载

系统应从配置目录加载全局配置，当配置文件不存在或无法解析时使用合理的默认值。

#### 场景：配置文件存在且有效
- **当** `config.json` 存在于全局配置目录中
- **并且** 文件包含符合配置模式的有效 JSON
- **则** `getGlobalConfig()` 返回解析后的配置

#### 场景：配置文件不存在
- **当** `config.json` 在全局配置目录中不存在
- **则** `getGlobalConfig()` 返回默认配置
- **并且** 不创建目录或文件

#### 场景：配置文件是无效的 JSON
- **当** `config.json` 存在但包含无效的 JSON
- **则** `getGlobalConfig()` 返回默认配置
- **并且** 向 stderr 记录警告

### 需求：全局配置保存

系统应将全局配置保存到配置目录，如果目录不存在则创建。

#### 场景：保存配置到新目录
- **当** 调用 `saveGlobalConfig(config)`
- **并且** 全局配置目录不存在
- **则** 创建该目录
- **并且** 使用提供的配置写入 `config.json`

#### 场景：保存配置到现有目录
- **当** 调用 `saveGlobalConfig(config)`
- **并且** 全局配置目录已存在
- **则** 写入 `config.json`（如存在则覆盖）

### 需求：默认配置

系统应提供默认配置，当没有配置文件时使用。

#### 场景：默认配置结构
- **当** 没有配置文件存在
- **则** 默认配置包含一个空的 `featureFlags` 对象

### 需求：配置模式演化

系统应将加载的配置与默认值合并，以确保即使在加载旧配置文件时新配置字段也可用。

#### 场景：配置文件缺少新字段
- **当** `config.json` 存在且内容为 `{ "featureFlags": {} }`
- **并且** 当前模式包含一个新字段 `defaultAiTool`
- **则** `getGlobalConfig()` 返回 `{ featureFlags: {}, defaultAiTool: <默认值> }`
- **并且** 对于两者都存在的字段，加载的值优先于默认值

#### 场景：配置文件包含额外未知字段
- **当** `config.json` 包含当前模式中没有的字段
- **则** 在返回的配置中保留未知字段
- **并且** 不引发错误或警告
