## 新增需求

### 需求：workspace planning schema
artifact 图应提供一个内置的 workspace planning schema，用于 workspace 范围的变更。

#### 场景：内置的 workspace planning schema 可用
- **WHEN** 从包内置项解析 schema 时
- **THEN** 应提供一个名为 `workspace-planning` 的 schema
- **AND** 它应描述 workspace 范围 planning 的 artifact 结构

#### 场景：workspace planning schema artifact
- **WHEN** 加载 `workspace-planning` schema 时
- **THEN** 它应包括共享 proposal、workspace 范围规格、跨区域设计和协调任务等标准 planning artifact
- **AND** 在这些标准 planning artifact 之外，不应再要求额外的区域清单

#### 场景：workspace planning schema 支持嵌套规格
- **WHEN** `workspace-planning` schema 定义其规格 artifact 时
- **THEN** 规格 artifact 应解析 `specs/**/*.md` 下的 workspace 范围规格文件
- **AND** schema 指引应将 `specs/<区域或 repository>/<能力>/spec.md` 描述为按区域组织需求的默认约定

#### 场景：workspace planning schema template
- **WHEN** 请求 `workspace-planning` schema 的 artifact 指令时
- **THEN** schema 应提供指导 agent 编写 workspace 级别 planning 内容的 template
- **AND** 这些 template 应避免指示 agent 创建 repository 本地的实施 artifact
- **AND** 规格指令应支持在 workspace 范围的 `specs/` 路径下组织特定区域的需求

#### 场景：workspace 嵌套规格路径保持 workspace 范围
- **GIVEN** workspace 变更有位于 `specs/<区域或 repository>/<能力>/spec.md` 下的规格文件
- **WHEN** OpenSpec 报告 workspace 变更的状态或 artifact 指令时
- **THEN** 应保留具体的嵌套 workspace 规格路径
- **AND** 除非有明确的影响区域实施上下文，否则不应将这些文件视为需要同步或 archive 的 repository 本地规格

#### 场景：workspace planning 应用就绪状态
- **WHEN** `workspace-planning` schema 定义应用就绪状态时
- **THEN** 在开始实施之前应要求完成协调任务
- **AND** 应用指引应指导 agent 在做出实施编辑之前先选择影响区域
