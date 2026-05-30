## 原因

OpenSpec 目前没有用户级别全局设置或功能标志的机制。随着 CLI 的发展，我们需要一个标准位置来存储跨项目的用户偏好、实验性功能和其他配置。遵循 XDG 基础目录规范提供了一种广泛理解、跨平台的方法。

## 变更内容

- 新增 `src/core/global-config.ts` 模块，包含：
  - 遵循 XDG 基础目录规范的路径解析（`$XDG_CONFIG_HOME/openspec/` 或回退路径）
  - 跨平台支持（Unix、macOS、Windows）
  - 带合理默认值的惰性配置加载
  - 配置结构的 TypeScript 类型
- 导出全局配置目录路径获取器，供未来使用（工作流、模板、缓存）
- 初始配置模式仅支持 1-2 个设置/功能标志

## 影响范围

- 受影响的规范：新的 `global-config` 能力（未修改现有规范）
- 受影响的代码：
  - 新增 `src/core/global-config.ts`
  - 更新 `src/core/index.ts` 以导出新模块
