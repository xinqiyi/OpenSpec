## 新增需求

### 需求：workspace 产品语言
OpenSpec 约定应使用面向用户的产品术语来描述协调 workspace。

#### 场景：描述 workspace 结构
- **WHEN** OpenSpec 文档描述 workspace 支持时
- **THEN** 应将 workspace 呈现为跨链接 repository 或文件夹进行工作的 planning 中心
- **AND** 应将 `changes/` 描述为 workspace planning 区域

#### 场景：避免内部 workspace 词汇
- **WHEN** OpenSpec 文档解释 workspace 包含的内容时
- **THEN** 应优先使用简洁的产品语言，例如"repository 或文件夹"
- **AND** 应避免在面向用户的内容中依赖诸如"工作集"、"代码区域"、"条目"、"别名"或"本地覆盖层"等术语

#### 场景：区分 workspace 和变更
- **WHEN** OpenSpec 文档解释 workspace planning 时
- **THEN** 应将 workspace 描述为持久的 planning 中心
- **AND** 应将各个功能、修复和项目描述为 workspace 内的变更

#### 场景：区分 workspace 和 repository 本地表面
- **WHEN** OpenSpec 文档比较 workspace 和 repository 本地流程时
- **THEN** 应解释 workspace planning 位于 workspace 根目录
- **AND** 应解释 repository 本地规格和变更继续存放在每个 repository 的 `openspec/` 目录下

#### 场景：安排 workspace 路线图顺序
- **WHEN** workspace 重构工作分布在多个活动变更中时
- **THEN** 约定应允许这些变更作为 `openspec/changes/` 下的同级项保持扁平结构
- **AND** 在正式的变更堆叠元数据可用之前，依赖顺序可以通过 proposal 文本来记录
