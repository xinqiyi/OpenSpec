## 新增的需求

### 需求：全局配置目录路径

系统应遵循 XDG 基本目录 spec 解析全局配置目录路径，并配合平台特定的回退策略。

#### 场景：设置了 XDG_CONFIG_HOME 的 Unix/macOS
- **WHEN** `$XDG_CONFIG_HOME` 环境变量设置为 `/custom/config`
- **THEN** `getGlobalConfigDir()` 返回 `/custom/config/openspec`

#### 场景：未设置 XDG_CONFIG_HOME 的 Unix/macOS
- **WHEN** `$XDG_CONFIG_HOME` 环境变量未设置
- **AND** 平台是 Unix 或 macOS
- **THEN** `getGlobalConfigDir()` 返回 `~/.config/openspec`（展开为绝对路径）

#### 场景：Windows 平台
- **WHEN** 平台是 Windows
- **AND** `%APPDATA%` 设置为 `C:\Users\User\AppData\Roaming`
- **THEN** `getGlobalConfigDir()` 返回 `C:\Users\User\AppData\Roaming\openspec`

### 需求：全局配置加载

系统应从配置目录加载全局配置，当配置文件不存在或无法解析时使用合理的默认值。

#### 场景：配置文件存在且有效
- **WHEN** `config.json` 存在于全局配置目录中
- **AND** 文件包含符合配置 schema 的有效 JSON
- **THEN** `getGlobalConfig()` 返回解析后的配置

#### 场景：配置文件不存在
- **WHEN** `config.json` 在全局配置目录中不存在
- **THEN** `getGlobalConfig()` 返回默认配置
- **AND** 不创建目录或文件

#### 场景：配置文件是无效的 JSON
- **WHEN** `config.json` 存在但包含无效的 JSON
- **THEN** `getGlobalConfig()` 返回默认配置
- **AND** 向 stderr 记录警告

### 需求：全局配置保存

系统应将全局配置保存到配置目录，如果目录不存在则创建。

#### 场景：保存配置到新目录
- **WHEN** 调用 `saveGlobalConfig(config)`
- **AND** 全局配置目录不存在
- **THEN** 创建该目录
- **AND** 使用提供的配置写入 `config.json`

#### 场景：保存配置到现有目录
- **WHEN** 调用 `saveGlobalConfig(config)`
- **AND** 全局配置目录已存在
- **THEN** 写入 `config.json`（如存在则覆盖）

### 需求：默认配置

系统应提供默认配置，当没有配置文件时使用。

#### 场景：默认配置结构
- **WHEN** 没有配置文件存在
- **THEN** 默认配置包含一个空的 `featureFlags` 对象

### 需求：配置 schema 演化

系统应将加载的配置与默认值合并，以确保即使在加载旧配置文件时新配置字段也可用。

#### 场景：配置文件缺少新字段
- **WHEN** `config.json` 存在且内容为 `{ "featureFlags": {} }`
- **AND** 当前 schema 包含一个新字段 `defaultAiTool`
- **THEN** `getGlobalConfig()` 返回 `{ featureFlags: {}, defaultAiTool: <默认值> }`
- **AND** 对于两者都存在的字段，加载的值优先于默认值

#### 场景：配置文件包含额外未知字段
- **WHEN** `config.json` 包含当前 schema 中没有的字段
- **THEN** 在返回的配置中保留未知字段
- **AND** 不引发错误或警告
