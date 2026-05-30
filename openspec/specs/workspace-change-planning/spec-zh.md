# workspace-change-planning spec

## 目的
定义 OpenSpec 如何创建、跟踪和指导 workspace 级别的变更，其 planning artifact 在实现所有权最终确定之前协调多个链接的 repository 或文件夹。

## 需求
### 需求：workspace 变更 planning 中心
OpenSpec 应支持 workspace 级别的变更，其共享计划位于 workspace planning 中心。

#### 场景：创建 workspace 变更
- **GIVEN** 命令从 OpenSpec workspace 运行
- **WHEN** 用户创建 workspace planning 的变更
- **THEN** OpenSpec 应在 workspace planning 路径下创建变更
- **AND** 应将 workspace 视为该变更的 planning 中心
- **AND** 当未提供显式 schema 时，应使用 workspace planning schema

#### 场景：workspace planning artifact 结构
- **GIVEN** workspace 变更使用 workspace planning schema
- **WHEN** OpenSpec 报告或创建该变更的 planning artifact
- **THEN** 应使用 workspace 级别的 artifact 用于 proposal、specs、跨区域设计和协调任务
- **AND** 这些 artifact 应位于 workspace 变更根目录下
- **AND** 不应要求在这些正常 planning artifact 之外额外添加区域清单

#### 场景：一次性捕获共享目标
- **WHEN** 提出 workspace 变更时
- **THEN** OpenSpec 应在 workspace 变更级别捕获产品目标
- **AND** 应避免在了解受影响区域之前要求单独的 repository 本地 proposal

#### 场景：在变更创建期间保留链接 repository
- **WHEN** OpenSpec 创建 workspace 级别的变更时
- **THEN** 不应在链接的 repository 或文件夹内创建 repository 本地的 OpenSpec 变更目录
- **AND** 不应编辑链接 repository 或文件夹中的实现文件

### 需求：workspace 受影响区域
OpenSpec 应将 workspace 变更中的所有权或实现边界表示为受影响区域。

#### 场景：使用注册的 workspace 链接作为区域
- **GIVEN** workspace 有链接的 repository 或文件夹
- **WHEN** workspace 变更通过注册的链接名称标识受影响区域
- **THEN** OpenSpec 应针对 workspace 链接验证这些区域名称
- **AND** 应清晰报告无效的区域名称

#### 场景：在所有区域确定之前进行 planning
- **WHEN** 用户仍在探索 workspace 变更时
- **THEN** OpenSpec 应允许在所有受影响区域确定之前存在共享计划
- **AND** 应在正常的 planning artifact 和状态输出中保持未解决的受影响区域问题可见

#### 场景：按区域组织需求
- **GIVEN** workspace 变更的需求由一个或多个受影响区域拥有
- **WHEN** OpenSpec 报告或创建 workspace 范围的 spec
- **THEN** 应允许将特定区域的需求组织在 `specs/<区域或 repository>/<能力>/spec.md` 下
- **AND** 不应要求在正常的 `specs/` artifact 树之外设置单独的区域文件夹
- **AND** 应保留区域或 repository 路径段作为 workspace planning 上下文，而不是将其扁平化为 repository 本地的能力名称

#### 场景：区分区域与交付切片
- **WHEN** workspace 变更报告受影响区域时
- **THEN** OpenSpec 应区分受影响区域与交付切片或阶段
- **AND** 不应要求用户为小型跨区域变更定义交付切片

### 需求：workspace planning 事实源头
OpenSpec 应将 workspace 变更计划作为事实源头，直到选定受影响区域的实现开始。

#### 场景：在实现之前进行探索
- **WHEN** agent 探索 workspace 变更时
- **THEN** 应使用 workspace 级别的 planning artifact 作为共享 planning 源
- **AND** 应将链接的 repository 和文件夹视为可用上下文，而不是已承诺的实现目标

#### 场景：推迟 repository 本地实现
- **WHEN** workspace 变更需要 repository 本地的实现工作
- **THEN** OpenSpec 应要求使用选定的受影响区域进行显式的实现 workflow
- **AND** 应在实现编辑开始前暴露该选定区域的允许编辑根目录
