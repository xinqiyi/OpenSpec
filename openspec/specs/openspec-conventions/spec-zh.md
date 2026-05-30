# OpenSpec 约定 spec

## 目的

OpenSpec 约定应定义系统能力如何被文档化、变更如何被提议和追踪，以及 spec 如何随时间演进。本元 spec 作为 OpenSpec 自身约定的最终依据。

## 要求

### 要求：针对 spec 和变更的结构化约定

OpenSpec 约定应强制要求结构化的 spec 格式，包含清晰的需求和场景章节，以便工具能够一致地解析。

#### 场景：遵循结构化 spec 格式

- **WHEN** 编写或更新 OpenSpec spec 时
- **THEN** 作者应使用 `### Requirement: ...`，后跟至少一个 `#### Scenario: ...` 章节

### 要求：行为优先的 spec 边界

OpenSpec spec 应捕获可验证的行为契约，并避免内部实现细节。

#### 场景：编写行为需求
- **WHEN** 在 `spec.md` 中记录某项能力时
- **THEN** 需求应聚焦于外部可观察的行为、接口、错误处理和约束
- **AND** 场景应保持可测试性或可显式验证

#### 场景：避免实现泄露
- **WHEN** 细节涉及具体的库选择、类/函数结构或执行机制时
- **THEN** 这些细节应记录在 `design.md` 或 `tasks.md` 中，而非行为需求中

### 要求：渐进严谨性

OpenSpec 约定应默认保持 spec 轻量，仅在风险或协作复杂性需要时提升严谨度。

#### 场景：常规变更 spec
- **WHEN** 变更属于本地且低风险时
- **THEN** 作者应使用简洁、行为优先的需求，以最少的仪式性内容完成

#### 场景：高风险或跨边界变更 spec
- **WHEN** 变更是跨团队、跨 repository、API 契约破坏、迁移密集或涉及安全/隐私时
- **THEN** 作者应按比例增加细节和显式验证预期

### 要求：项目结构

OpenSpec 项目应为 spec 和变更维护一致的目录结构。

#### 场景：初始化项目结构
- **WHEN** OpenSpec 项目被初始化时
- **THEN** 应具有以下结构：
```
openspec/
├── project.md # 项目特定上下文
├── AGENTS.md # AI 助手指令
├── specs/ # 当前已部署的能力
│ └── [capability]/ # 单一、聚焦的能力
│ ├── spec.md # 是什么和为什么
│ └── design.md # 如何实现（可选，针对已建立 schema）
└── changes/ # 提议的变更
 ├── [change-name]/ # 描述性变更标识符
 │ ├── proposal.md # 为什么、是什么以及影响
 │ ├── tasks.md # 实现检查清单
 │ ├── design.md # 技术决策（可选）
 │ └── specs/ # 完整的未来状态
 │ └── [capability]/
 │ └── spec.md # 干净的 Markdown（无 diff 语法）
 └── archive/ # 已完成的变更
 └── YYYY-MM-DD-[name]/
```

### 要求：行为 spec 的结构化格式

行为 spec 应使用结构化格式，包含一致的章节标题和关键词，以确保视觉一致性和可解析性。

#### 场景：编写需求章节

- **WHEN** 在行为 spec 中记录需求时
- **THEN** 使用三级标题，格式为 `### Requirement: [Name]`
- **AND** 立即跟上描述核心行为的 SHALL 语句
- **AND** 保持需求名称具有描述性且在 50 个字符以内

#### 场景：记录场景

- **WHEN** 记录特定行为或用例时
- **THEN** 使用四级标题，格式为 `#### Scenario: [Description]`
- **AND** 对步骤使用带粗体关键词的列表项：
 - **GIVEN** 用于初始状态（可选）
 - **WHEN** 用于条件或触发器
 - **THEN** 用于预期结果
 - **AND** 用于附加结果或条件

#### 场景：添加实现细节

- **WHEN** 某一步骤需要额外细节时
- **THEN** 在主步骤下使用子列表项
- **AND** 保持一致的缩进
 - 子列表项提供示例或具体说明
 - 保持子列表项简洁

### 要求：基于标题的需求标识

需求标题应作为唯一标识符，用于当前 spec 和提议变更之间的程序化匹配。

#### 场景：以编程方式匹配需求

- **WHEN** 处理 delta 变更时
- **THEN** 使用 `### Requirement: [Name]` 标题作为唯一标识符
- **AND** 使用 spec 化标题进行匹配：`normalize(header) = trim(header)`
- **AND** spec 化后以大小写敏感的方式比较标题

#### 场景：处理需求重命名

- **WHEN** 重命名需求时
- **THEN** 使用特殊的 `## RENAMED Requirements` 章节
- **AND** 显式指定旧名称和新名称：
 ```markdown
 ## RENAMED Requirements
 - FROM: `### Requirement: Old Name`
 - TO: `### Requirement: New Name`
 ```
- **AND** 如果内容也发生变更，使用新标题归入 MODIFIED 下

#### 场景：验证标题唯一性

- **WHEN** 创建或修改需求时
- **THEN** 确保 spec 内不存在重复的标题
- **AND** 验证工具应将重复标题标记为错误

### 要求：变更存储约定

变更 proposal 应仅存储对 spec 的添加、修改和删除，而非完整的未来状态。

#### 场景：创建带新增内容的变更 proposal

- **WHEN** 创建添加新需求的变更 proposal 时
- **THEN** 仅将新需求放在 `## ADDED Requirements` 下
- **AND** 每条需求应包含其完整内容
- **AND** 对需求和场景使用标准的结构化格式

#### 场景：创建带修改内容的变更 proposal

- **WHEN** 创建修改现有需求的变更 proposal 时
- **THEN** 将修改后的需求放在 `## MODIFIED Requirements` 下
- **AND** 使用与当前 spec 相同的标题文本（spec 化后）
- **AND** 包含完整的修改后需求（不是 diff）
- **AND** 可选地使用行内注释标注变更内容，如 `← (was X)`

#### 场景：创建带删除内容的变更 proposal

- **WHEN** 创建删除需求的变更 proposal 时
- **THEN** 将其列在 `## REMOVED Requirements` 下
- **AND** 使用 spec 化后的标题文本进行标识
- **AND** 包含删除原因
- **AND** 如适用，记录任何迁移路径

`changes/[name]/specs/` 目录应包含：
- 仅显示变更内容的 delta 文件
- ADDED、MODIFIED、REMOVED 和 RENAMED 需求章节
- 用于需求标识的 spec 化标题匹配
- 使用结构化格式的完整需求
- 每条需求变更类型的清晰指示

#### 场景：使用标准输出符号

- **WHEN** 在 CLI 输出中显示 delta 操作时
- **THEN** 使用以下标准符号：
 - `+` 表示 ADDED（绿色）
 - `~` 表示 MODIFIED（黄色）
 - `-` 表示 REMOVED（红色）
 - `→` 表示 RENAMED（青色）

### 要求：archive 流程增强

archive 流程应以编程方式基于标题匹配将 delta 变更应用到当前 spec。

#### 场景：使用 delta archive 变更

- **WHEN** archive 已完成的变更时
- **THEN** archive 命令应：
 1. 首先解析 RENAMED 章节并应用重命名
 2. 解析 REMOVED 章节并按 spec 化标题匹配删除
 3. 解析 MODIFIED 章节并按 spec 化标题匹配替换（如已重命名则使用新名称）
 4. 解析 ADDED 章节并追加新需求
- **AND** 验证所有 MODIFIED/REMOVED 标题在当前 spec 中存在
- **AND** 验证 ADDED 标题尚不存在
- **AND** 在主 specs/ 目录中生成更新后的 spec

#### 场景：处理 archive 过程中的冲突

- **WHEN** delta 变更与当前 spec 状态冲突时
- **THEN** archive 命令应报告具体冲突
- **AND** 在继续前要求人工解决
- **AND** 提供解决冲突的清晰指导

### 要求：proposal 格式

proposal 应显式记录所有变更，包含清晰的从/到比较。

#### 场景：记录变更

- **WHEN** 记录变更内容时
- **THEN** proposal 应显式描述每个变更：

```markdown
**[章节或行为名称]**
- From: [当前状态/需求]
- To: [未来状态/需求]
- Reason: [为何需要此变更]
- Impact: [破坏性/非破坏性，谁受影响]
```

这种显式格式弥补了没有行内 diff 的不足，确保审阅者确切了解将要变更的内容。

### 要求：变更审阅

系统应支持多种方法来审阅提议的变更。

#### 场景：审阅变更

- **WHEN** 审阅提议的变更时
- **THEN** 审阅者可以使用以下方式进行比较：
 - 变更提交后的 GitHub PR diff 视图
 - 命令行：`diff -u specs/[capability]/spec.md changes/[name]/specs/[capability]/spec.md`
 - 任何比较当前状态与未来状态的视觉 diff 工具

### 要求：结构化格式的采用

行为 spec 应采用结构化格式，默认使用 `### Requirement:` 和 `#### Scenario:` 标题。

#### 场景：对行为使用结构化标题

- **WHEN** 记录行为需求时
- **THEN** 对需求使用 `### Requirement:`
- **AND** 对场景使用 `#### Scenario:`，配合粗体的 WHEN/THEN/AND 关键词

### 要求：动词-名词 CLI 命令结构

OpenSpec CLI 设计应使用动词作为顶级命令，名词作为参数或标志来限定范围。

#### 场景：动词优先的命令发现
- **WHEN** 用户运行类似 `openspec list` 的命令时
- **THEN** 动词清晰地传达操作意图
- **AND** 名词通过标志或参数细化范围（例如 `--changes`、`--specs`）

#### 场景：名词命令的向后兼容
- **WHEN** 用户运行名词前缀的命令如 `openspec spec ...` 或 `openspec change ...` 时
- **THEN** CLI 应至少在一个版本内继续支持它们
- **AND** 显示指向动词优先替代方案的弃用警告

#### 场景：消歧指引
- **WHEN** 项目名称在变更和 spec 之间产生歧义时
- **THEN** `openspec show` 和 `openspec validate` 应接受 `--type spec|change`
- **AND** 帮助文本应清晰记录此行为

### 要求：workspace 产品语言

OpenSpec 约定应在面向用户的产品术语中描述协作 workspace。

#### 场景：描述 workspace 结构
- **WHEN** OpenSpec 文档描述 workspace 支持时
- **THEN** 应将 workspace 呈现为跨链接 repository 或文件夹进行 planning 的工作家园
- **AND** 应将 `changes/` 描述为 workspace planning 区域

#### 场景：避免内部 workspace 术语
- **WHEN** OpenSpec 文档解释 workspace 包含什么时
- **THEN** 应优先使用平实的产品语言，如"repository 或文件夹"
- **AND** 应避免在面向用户的内容中使用"工作集"、"代码区域"、"条目"、"别名"或"本地覆盖"等术语

#### 场景：区分 workspace 与变更
- **WHEN** OpenSpec 文档解释 workspace planning 时
- **THEN** 应将 workspace 描述为持久性的 planning 家园
- **AND** 应将各个功能、修复和项目描述为 workspace 内的变更

#### 场景：区分 workspace 和 repository 本地界面
- **WHEN** OpenSpec 文档比较 workspace 与 repository 本地流程时
- **THEN** 应解释 workspace planning 位于 workspace 文件夹中
- **AND** 应解释 repository 本地 spec 和变更继续位于每个 repository 的 `openspec/` 目录下

#### 场景：安排 workspace 路线图
- **WHEN** workspace 重新实现工作被拆分为多个并行的活跃变更时
- **THEN** 约定应允许这些变更保持为 `openspec/changes/` 下的平级兄弟项
- **AND** 在正式的变更堆叠元数据可用之前，依赖顺序可以在 proposal 正文中记录

### 要求：workspace planning 术语

OpenSpec 约定应使用面向用户的产品语言来区分 workspace planning 概念。

#### 场景：命名受影响区域
- **WHEN** 文档或生成的指导内容提及 workspace 变更所触及的 repository、文件夹、包、服务、应用或文档站点时
- **THEN** 应称其为受影响区域
- **AND** 应避免使用"目标 repository"或"repository 切片"作为主要的面向用户术语

#### 场景：命名交付切片
- **WHEN** 文档或生成的指导内容提及较大变更内部的交付 delta 时
- **THEN** 仅在交付排序是主题时称其为切片或阶段
- **AND** 不应将切片用作 repository、文件夹或受影响区域的同义词

### 要求：workspace planning 与实现边界

OpenSpec 约定应区分 workspace 级别的 planning 与 repository 本地的实现所有权。

#### 场景：workspace 作为共享 planning 家园
- **WHEN** 变更跨越链接的 repository 或文件夹时
- **THEN** 约定应将 workspace 描述为共享的 planning 家园
- **AND** repository 本地的实现家园应保留其代码和 spec 行为的拥有权

#### 场景：避免物化优先的语言
- **WHEN** 文档解释 workspace 变更创建时
- **THEN** 应以共享 planning 和受影响区域的术语描述用户成果
- **AND** 应避免让用户在能够 planning 之前必须先理解物化等实现术语

#### 场景：保留熟悉的 workflow 动词
- **WHEN** workspace 指导描述 OpenSpec workflow 时
- **THEN** 应保留熟悉的动词：探索、提议、应用、验证和 archive
- **AND** 应解释 workspace 上下文改变的是路径、范围和允许的编辑根目录，而非创建一套独立的 workflow 体系

## 核心原则

系统应遵循以下原则：
- spec 反映当前已构建和部署的内容
- 变更包含应对什么进行变更的 proposal
- AI 驱动文档编写过程
- spec 是与已部署代码保持同步的活的文档

## 目录结构

### 项目结构

OpenSpec 项目应为 spec 和变更维护一致的目录结构。

#### 场景：初始化项目结构

- **WHEN** OpenSpec 项目被初始化时
- **THEN** 应具有以下结构：
```
openspec/
├── project.md # 项目特定上下文
├── AGENTS.md # AI 助手指令
├── specs/ # 当前已部署的能力
│ └── [capability]/ # 单一、聚焦的能力
│ ├── spec.md # 是什么和为什么
│ └── design.md # 如何实现（可选，针对已建立 schema）
└── changes/ # 提议的变更
 ├── [change-name]/ # 描述性变更标识符
 │ ├── proposal.md # 为什么、是什么以及影响
 │ ├── tasks.md # 实现检查清单
 │ ├── design.md # 技术决策（可选）
 │ └── specs/ # 完整的未来状态
 │ └── [capability]/
 │ └── spec.md # 干净的 Markdown（无 diff 语法）
 └── archive/ # 已完成的变更
 └── YYYY-MM-DD-[name]/
```

## spec 格式

### 行为 spec 格式

行为 spec 应使用结构化格式，包含一致的章节标题和关键词，以确保视觉一致性和可解析性。

#### 场景：编写需求章节

- **WHEN** 在行为 spec 中记录需求时
- **THEN** 使用三级标题，格式为 `### Requirement: [Name]`
- **AND** 立即跟上描述核心行为的 SHALL 语句
- **AND** 保持需求名称具有描述性且在 50 个字符以内

#### 场景：记录场景

- **WHEN** 记录特定行为或用例时
- **THEN** 使用四级标题，格式为 `#### Scenario: [Description]`
- **AND** 对步骤使用带粗体关键词的列表项：
 - **GIVEN** 用于初始状态（可选）
 - **WHEN** 用于条件或触发器
 - **THEN** 用于预期结果
 - **AND** 用于附加结果或条件

#### 场景：添加实现细节

- **WHEN** 某一步骤需要额外细节时
- **THEN** 在主步骤下使用子列表项
- **AND** 保持一致的缩进
 - 子列表项提供示例或具体说明
 - 保持子列表项简洁

## 变更存储约定

### 基于标题的需求标识

需求标题应作为唯一标识符，用于当前 spec 和提议变更之间的程序化匹配。

#### 场景：以编程方式匹配需求

- **WHEN** 处理 delta 变更时
- **THEN** 使用 `### Requirement: [Name]` 标题作为唯一标识符
- **AND** 使用 spec 化标题进行匹配：`normalize(header) = trim(header)`
- **AND** spec 化后以大小写敏感的方式比较标题

#### 场景：处理需求重命名

- **WHEN** 重命名需求时
- **THEN** 使用特殊的 `## RENAMED Requirements` 章节
- **AND** 显式指定旧名称和新名称：
 ```markdown
 ## RENAMED Requirements
 - FROM: `### Requirement: Old Name`
 - TO: `### Requirement: New Name`
 ```
- **AND** 如果内容也发生变更，使用新标题归入 MODIFIED 下

#### 场景：验证标题唯一性

- **WHEN** 创建或修改需求时
- **THEN** 确保 spec 内不存在重复的标题
- **AND** 验证工具应将重复标题标记为错误

### 变更存储约定

变更 proposal 应仅存储对 spec 的添加、修改和删除，而非完整的未来状态。

#### 场景：创建带新增内容的变更 proposal

- **WHEN** 创建添加新需求的变更 proposal 时
- **THEN** 仅将新需求放在 `## ADDED Requirements` 下
- **AND** 每条需求应包含其完整内容
- **AND** 对需求和场景使用标准的结构化格式

#### 场景：创建带修改内容的变更 proposal

- **WHEN** 创建修改现有需求的变更 proposal 时
- **THEN** 将修改后的需求放在 `## MODIFIED Requirements` 下
- **AND** 使用与当前 spec 相同的标题文本（spec 化后）
- **AND** 包含完整的修改后需求（不是 diff）
- **AND** 可选地使用行内注释标注变更内容，如 `← (was X)`

#### 场景：创建带删除内容的变更 proposal

- **WHEN** 创建删除需求的变更 proposal 时
- **THEN** 将其列在 `## REMOVED Requirements` 下
- **AND** 使用 spec 化后的标题文本进行标识
- **AND** 包含删除原因
- **AND** 如适用，记录任何迁移路径

`changes/[name]/specs/` 目录应包含：
- 仅显示变更内容的 delta 文件
- ADDED、MODIFIED、REMOVED 和 RENAMED 需求章节
- 用于需求标识的 spec 化标题匹配
- 使用结构化格式的完整需求
- 每条需求变更类型的清晰指示

#### 场景：使用标准输出符号

- **WHEN** 在 CLI 输出中显示 delta 操作时
- **THEN** 使用以下标准符号：
 - `+` 表示 ADDED（绿色）
 - `~` 表示 MODIFIED（黄色）
 - `-` 表示 REMOVED（红色）
 - `→` 表示 RENAMED（青色）

### archive 流程增强

archive 流程应以编程方式基于标题匹配将 delta 变更应用到当前 spec。

#### 场景：使用 delta archive 变更

- **WHEN** archive 已完成的变更时
- **THEN** archive 命令应：
 1. 首先解析 RENAMED 章节并应用重命名
 2. 解析 REMOVED 章节并按 spec 化标题匹配删除
 3. 解析 MODIFIED 章节并按 spec 化标题匹配替换（如已重命名则使用新名称）
 4. 解析 ADDED 章节并追加新需求
- **AND** 验证所有 MODIFIED/REMOVED 标题在当前 spec 中存在
- **AND** 验证 ADDED 标题尚不存在
- **AND** 在主 specs/ 目录中生成更新后的 spec

#### 场景：处理 archive 过程中的冲突

- **WHEN** delta 变更与当前 spec 状态冲突时
- **THEN** archive 命令应报告具体冲突
- **AND** 在继续前要求人工解决
- **AND** 提供解决冲突的清晰指导

### proposal 格式

proposal 应显式记录所有变更，包含清晰的从/到比较。

#### 场景：记录变更

- **WHEN** 记录变更内容时
- **THEN** proposal 应显式描述每个变更：

```markdown
**[章节或行为名称]**
- From: [当前状态/需求]
- To: [未来状态/需求]
- Reason: [为何需要此变更]
- Impact: [破坏性/非破坏性，谁受影响]
```

这种显式格式弥补了没有行内 diff 的不足，确保审阅者确切了解将要变更的内容。

## 变更生命周期

变更过程应遵循以下状态：

1. **提议**：AI 创建包含未来状态 spec 和显式 proposal 的变更
2. **审阅**：人类审阅 proposal 和未来状态
3. **批准**：变更获批进入实现阶段
4. **实现**：按 tasks.md 检查清单执行（可跨越多个 PR）
5. **部署**：变更被部署到生产环境
6. **更新**：`specs/` 中的 spec 被更新以匹配已部署的实际情况
7. **archive**：变更被移至 `archive/YYYY-MM-DD-[name]/`

## 查看变更

### 变更审阅

系统应支持多种方法来审阅提议的变更。

#### 场景：审阅变更

- **WHEN** 审阅提议的变更时
- **THEN** 审阅者可以使用以下方式进行比较：
 - 变更提交后的 GitHub PR diff 视图
 - 命令行：`diff -u specs/[capability]/spec.md changes/[name]/specs/[capability]/spec.md`
 - 任何比较当前状态与未来状态的视觉 diff 工具

系统依赖工具来生成 diff，而非存储 diff。

## 能力命名

能力应使用：
- 动词-名词 schema（例如 `user-auth`、`payment-capture`）
- 小写字母加连字符的名称
- 单一关注点（每项能力一个职责）
- 无嵌套（在 `specs/` 下保持扁平结构）

## 何时需要 proposal

以下情况应创建 proposal：
- 新功能或新能力
- 对现有行为的破坏性变更
- 架构或 schema 变更
- 改变行为的性能优化
- 影响访问 schema 的安全更新

以下情况不需要 proposal：
- 恢复预期行为的错误修复
- 拼写或格式修正
- 非破坏性的依赖更新
- 为现有行为添加测试
- 文档澄清

## 为何采用此方法

清晰的未来状态存储带来以下好处：
- **可读性**：无 diff 语法污染
- **AI 兼容性**：AI 工具能够理解的标准 Markdown
- **简洁性**：无需特殊解析或处理
- **工具无关性**：任何 diff 工具都可以展示变更
- **意图清晰**：显式的 proposal 记录推理过程

结构化格式带来以下好处：
- **视觉一致性**：Requirement 和 Scenario 前缀使章节一目了然
- **可解析性**：一致的结构支持工具化和自动化
- **渐进采用**：现有 spec 可以逐步迁移
