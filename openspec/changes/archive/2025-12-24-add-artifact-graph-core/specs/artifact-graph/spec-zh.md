## 新增需求

### 需求：schema 加载
系统应从 YAML schema 文件加载 artifact 图定义。

#### 场景：加载有效 schema
- **WHEN** 提供了有效的 schema YAML 文件
- **THEN** 系统返回包含所有 artifact 和依赖的 ArtifactGraph

#### 场景：拒绝无效 schema
- **WHEN** schema YAML 文件缺少必填字段
- **THEN** 系统抛出带有描述性消息的错误

#### 场景：检测到循环依赖
- **WHEN** schema 包含循环的 artifact 依赖
- **THEN** 系统抛出错误，列出循环中的 artifact ID

#### 场景：无效的依赖引用
- **WHEN** artifact 的 `requires` 数组引用了不存在的 artifact ID
- **THEN** 系统抛出错误，标识无效引用

#### 场景：拒绝重复 artifact ID
- **WHEN** schema 包含多个具有相同 ID 的 artifact
- **THEN** 系统抛出错误，标识重复项

### 需求：构建顺序计算
系统应计算 artifact 的有效拓扑构建顺序。

#### 场景：线性依赖链
- **WHEN** artifact 形成线性链（A → B → C）
- **THEN** getBuildOrder() 返回 [A, B, C]

#### 场景：菱形依赖
- **WHEN** artifact 形成菱形（A → B, A → C, B → D, C → D）
- **THEN** getBuildOrder() 返回 A 在 B 和 C 之前，D 在最后

#### 场景：独立 artifact
- **WHEN** artifact 没有依赖
- **THEN** getBuildOrder() 以稳定的顺序返回它们

### 需求：状态检测
系统应通过扫描文件系统检测 artifact 完成状态。

#### 场景：简单文件存在
- **WHEN** artifact 生成 "proposal.md" 且该文件存在
- **THEN** artifact 标记为已完成

#### 场景：简单文件缺失
- **WHEN** artifact 生成 "proposal.md" 但该文件不存在
- **THEN** artifact 未标记为已完成

#### 场景：包含文件的 Glob schema
- **WHEN** artifact 生成 "specs/*.md" 且 specs/ 目录包含 .md 文件
- **THEN** artifact 标记为已完成

#### 场景：空的 Glob schema
- **WHEN** artifact 生成 "specs/*.md" 但 specs/ 目录为空或不存在
- **THEN** artifact 未标记为已完成

#### 场景：缺少变更目录
- **WHEN** 变更目录不存在
- **THEN** 所有 artifact 标记为未完成（空状态）

### 需求：就绪 artifact 查询
系统应基于依赖完成情况识别哪些 artifact 可以创建。

#### 场景：根 artifact 初始就绪
- **WHEN** 没有 artifact 已完成
- **THEN** getNextArtifacts() 返回没有依赖的 artifact

#### 场景：依赖 artifact 变为就绪
- **WHEN** artifact 的所有依赖都已完成
- **THEN** getNextArtifacts() 包含该 artifact

#### 场景：排除被阻塞的 artifact
- **WHEN** artifact 有未完成的依赖
- **THEN** getNextArtifacts() 不包含该 artifact

### 需求：完成检查
系统应确定图中的所有 artifact 何时完成。

#### 场景：全部完成
- **WHEN** 图中的所有 artifact 都在完成集合中
- **THEN** isComplete() 返回 true

#### 场景：部分完成
- **WHEN** 图中的部分 artifact 未完成
- **THEN** isComplete() 返回 false

### 需求：阻塞查询
系统应识别哪些 artifact 被阻塞，并返回其所有未满足的依赖。

#### 场景：artifact 被单依赖阻塞
- **WHEN** artifact B 需要 artifact A 且 A 未完成
- **THEN** getBlocked() 返回 `{ B: ['A'] }`

#### 场景：artifact 被多依赖阻塞
- **WHEN** artifact C 需要 A 和 B，且只有 A 已完成
- **THEN** getBlocked() 返回 `{ C: ['B'] }`

#### 场景：artifact 被所有依赖阻塞
- **WHEN** artifact C 需要 A 和 B，且两者都未完成
- **THEN** getBlocked() 返回 `{ C: ['A', 'B'] }`
