## 1. 核心实现

- [x] 1.1 创建 `src/core/global-config.ts`，包含路径解析
 - 实现遵循 XDG spec 的 `getGlobalConfigDir()`
 - 支持 `$XDG_CONFIG_HOME` 环境变量覆盖
 - 平台特定的回退（Unix：`~/.config/`，Windows：`%APPDATA%`）
- [x] 1.2 为配置结构定义 TypeScript 接口
 - `GlobalConfig` 接口，包含可选字段
 - 从最小化开始：仅 `featureFlags?: Record<string, boolean>`
- [x] 1.3 实现带默认值的配置加载
 - `getGlobalConfig()` - 如果 config.json 存在则读取，与默认值合并
 - 读取时不创建目录/文件（惰性初始化）
- [x] 1.4 实现配置保存
 - `saveGlobalConfig(config)` - 写入 config.json，必要时创建目录

## 2. 集成

- [x] 2.1 从 `src/core/index.ts` 导出新模块
- [x] 2.2 为配置文件名和目录名添加常量

## 3. 测试

- [x] 3.1 在当前平台上手动测试路径解析
- [x] 3.2 测试设置/未设置 `$XDG_CONFIG_HOME` 的情况
- [x] 3.3 测试文件不存在时的配置加载（应返回默认值）
- [x] 3.4 在 `test/core/global-config.test.ts` 中编写单元测试（18 个测试）
