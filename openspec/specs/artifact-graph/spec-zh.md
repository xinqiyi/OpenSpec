# artifact-graph spec

## 目的
定义 schema 驱动 workflow 使用的 artifact 图模型、依赖验证和完成状态逻辑。

## 需求
### 需求：Schema 加载
系统应从 schema 目录中的 YAML schema 文件加载 artifact 图定义。

#### 场景：加载有效 schema
- **WHEN** schema 目录包含有效的 `schema.yaml` 文件
- **THEN** 系统返回包含所有 artifact 和依赖关系的 ArtifactGraph

#### 场景：拒绝无效 schema
- **WHEN** schema YAML 文件缺少必需字段
- **THEN** 系统抛出带有描述性消息的错误

#### 场景：检测到循环依赖
- **WHEN** schema 包含循环的 artifact 依赖关系
- **THEN** 系统抛出错误，列出循环中的 artifact ID

#### 场景：无效的依赖引用
- **WHEN** artifact 的 `requires` 数组引用了不存在的 artifact ID
- **THEN** 系统抛出错误，指出无效的引用

#### 场景：拒绝重复的 artifact ID
- **WHEN** schema 包含多个具有相同 ID 的 artifact
- **THEN** 系统抛出错误，指出重复项

#### 场景：未找到 schema 目录
- **WHEN** 解析的 schema 名称没有对应的目录
- **THEN** 系统抛出错误，列出可用的 schema

### 需求：构建顺序计算
系统应计算 artifact 的有效拓扑构建顺序。

#### 场景：线性依赖链
- **WHEN** artifact 形成线性链（A → B → C）
- **THEN** getBuildOrder() 返回 [A, B, C]

#### 场景：菱形依赖
- **WHEN** artifact 形成菱形（A → B, A → C, B → D, C → D）
- **THEN** getBuildOrder() 返回 A 在 B 和 C 之前，D 最后

#### 场景：独立 artifact
- **WHEN** artifact 没有依赖关系
- **THEN** getBuildOrder() 以稳定的顺序返回它们

### 需求：状态检测
系统应通过扫描文件系统检测 artifact 的完成状态。

#### 场景：简单文件存在
- **WHEN** artifact 生成 "proposal.md" 且文件存在
- **THEN** artifact 标记为已完成

#### 场景：简单文件缺失
- **WHEN** artifact 生成 "proposal.md" 且文件不存在
- **THEN** artifact 未标记为已完成

#### 场景：包含文件的 Glob schema
- **WHEN** artifact 生成 "specs/*.md" 且 specs/ 目录包含 .md 文件
- **THEN** artifact 标记为已完成

#### 场景：Glob schema 为空
- **WHEN** artifact 生成 "specs/*.md" 且 specs/ 目录为空或不存在
- **THEN** artifact 未标记为已完成

#### 场景：缺少变更目录
- **WHEN** 变更目录不存在
- **THEN** 所有 artifact 标记为未完成（空状态）

### 需求：就绪 artifact 查询
系统应根据依赖完成情况识别哪些 artifact 可以创建。

#### 场景：根 artifact 初始就绪
- **WHEN** 没有 artifact 已完成
- **THEN** getNextArtifacts() 返回没有依赖关系的 artifact

#### 场景：依赖 artifact 变为就绪
- **WHEN** artifact 的所有依赖项都已完成
- **THEN** getNextArtifacts() 包含该 artifact

#### 场景：排除阻塞 artifact
- **WHEN** artifact 有未完成的依赖项
- **THEN** getNextArtifacts() 不包含该 artifact

### 需求：完成检查
系统应确定图中的所有 artifact 是否都已完成。

#### 场景：全部完成
- **WHEN** 图中的所有 artifact 都在已完成集合中
- **THEN** isComplete() 返回 true

#### 场景：部分完成
- **WHEN** 图中的某些 artifact 未完成
- **THEN** isComplete() 返回 false

### 需求：阻塞查询
系统应识别哪些 artifact 被阻塞，并返回它们所有未满足的依赖项。

#### 场景：artifact 被单个依赖阻塞
- **WHEN** artifact B 需要 artifact A 且 A 未完成
- **THEN** getBlocked() 返回 `{ B: ['A'] }`

#### 场景：artifact 被多个依赖阻塞
- **WHEN** artifact C 需要 A 和 B，且只有 A 完成
- **THEN** getBlocked() 返回 `{ C: ['B'] }`

#### 场景：artifact 被所有依赖阻塞
- **WHEN** artifact C 需要 A 和 B，且两者都未完成
- **THEN** getBlocked() 返回 `{ C: ['A', 'B'] }`

### 需求：Schema 目录结构
系统应支持带有同位置 template 的自包含 schema 目录。

#### 场景：带 template 的 Schema
- **WHEN** schema 目录包含 `schema.yaml` 和 `templates/` 子目录
- **THEN** artifact 可以引用相对于 schema template 目录的 template

#### 场景：用户 Schema 覆盖
- **WHEN** `${XDG_DATA_HOME}/openspec/schemas/<name>/` 存在 schema 目录
- **THEN** 系统使用该目录替代内置目录

#### 场景：内置 Schema 回退
- **WHEN** schema 不存在用户覆盖
- **THEN** 系统使用包内置的 schema 目录

#### 场景：列出可用 Schema
- **WHEN** 列出 schema
- **THEN** 系统返回用户目录和包目录中的 schema 名称

### 需求：workspace planning schema
artifact 图应提供用于 workspace 范围变更的内置 workspace planning schema。

#### 场景：内置 workspace planning schema 可用
- **WHEN** 从包内置项解析 schema
- **THEN** 应提供一个名为 `workspace-planning` 的 schema
- **AND** 它应描述 workspace 范围 planning 的 artifact 结构

#### 场景：workspace planning schema artifact
- **WHEN** 加载 `workspace-planning` schema
- **THEN** 它应包含用于共享 proposal、workspace 范围 spec、跨区域设计和协调任务的正常 planning artifact
- **AND** 它不应要求在这些正常 planning artifact 之外再提供额外的区域清单

#### 场景：workspace planning schema 支持嵌套 spec
- **WHEN** `workspace-planning` schema 定义其 spec artifact
- **THEN** spec artifact 应在 `specs/**/*.md` 下解析 workspace 范围的 spec 文件
- **AND** schema 指导应将 `specs/<area-or-repo>/<capability>/spec.md` 描述为按区域划分需求的默认约定

#### 场景：workspace planning schema template
- **WHEN** 请求 `workspace-planning` schema 的 artifact 指令
- **THEN** schema 应提供指导 agent 编写 workspace 级别 planning 内容的 template
- **AND** 这些 template 应避免指示 agent 创建 repository 本地的实现 artifact
- **AND** spec 指令应支持在 workspace 范围的 `specs/` 路径下组织按区域划分的需求

#### 场景：workspace 嵌套 spec 路径保持 workspace 范围
- **GIVEN** workspace 变更在 `specs/<area-or-repo>/<capability>/spec.md` 下有 spec 文件
- **WHEN** OpenSpec 报告 workspace 变更的状态或 artifact 指令
- **THEN** 它应保留具体的嵌套 workspace spec 路径
- **AND** 它不应将这些文件视为 repository 本地 spec 进行同步或 archive，除非有明确的影响区域实现上下文

#### 场景：workspace planning apply 就绪
- **WHEN** `workspace-planning` schema 定义 apply 就绪条件
- **THEN** 它应在实现开始之前要求完成协调任务
- **AND** apply 指导应引导 agent 在选择影响区域后再进行实现编辑
