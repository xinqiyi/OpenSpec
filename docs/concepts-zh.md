# 概念

本指南解释 OpenSpec 的核心思想及其如何协同工作。有关实际使用，请参阅[快速入门](getting-started.md)和[工作流](workflows.md)。

## 理念

OpenSpec 围绕四个原则构建：

```
流动而非僵化        — 没有阶段门控，做有意义的工作
迭代而非瀑布        — 边构建边学习，边做边完善
简单而非复杂        — 轻量级设置，最小化仪式
棕地优先            — 适用于现有代码库，不仅限绿地项目
```

### 为什么这些原则很重要

**流动而非僵化。** 传统的规范系统将您锁定在阶段中：先规划，然后实施，然后完成。OpenSpec 更加灵活——您可以按对工作有意义的任何顺序创建产物。

**迭代而非瀑布。** 需求会变化。理解会加深。开始时看起来不错的方法，在您看到代码库后可能站不住脚。OpenSpec 接受这一现实。

**简单而非复杂。** 某些规范框架需要大量设置、僵化的格式或繁重的流程。OpenSpec 不会阻碍您。几秒钟初始化，立即开始工作，仅在需要时自定义。

**棕地优先。** 大多数软件工作不是从零开始构建——而是修改现有系统。OpenSpec 基于 delta 的方法使指定对现有行为的变更变得容易，而不仅仅是描述新系统。

## 整体架构

OpenSpec 将您的工作组织为两个主要区域：

```
┌────────────────────────────────────────────────────────────────────┐
│                        openspec/                                   │
│                                                                    │
│   ┌─────────────────────┐      ┌───────────────────────────────┐   │
│   │       specs/        │      │         changes/              │   │
│   │                     │      │                               │   │
│   │  唯一真相来源       │◄─────│  提议的修改                   │   │
│   │  系统的当前工作方式  │ 合并 │  每个变更 = 一个文件夹       │   │
│   │                     │      │  包含产物 + delta             │   │
│   │                     │      │                               │   │
│   └─────────────────────┘      └───────────────────────────────┘   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**Specs** 是唯一真相来源——它们描述您的系统当前的行为方式。

**Changes** 是提议的修改——它们位于单独的文件夹中，直到您准备好合并。

这种分离是关键。您可以并行处理多个变更而不会冲突。您可以在变更影响主 specs 之前对其进行审查。当您归档变更时，其 deltas 会干净地合并到唯一真相来源中。

## 协调工作区

工作区支持处于 beta 阶段。下面的本地视图模型是当前方向，但外部自动化、集成和长期工作流仍应将命令行为、状态文件和 JSON 输出视为持续演进中。

以下命令提供了打开链接仓库或文件夹的本地视图的初始设置流程。

仓库本地 OpenSpec 项目是当一个仓库拥有规划、实施和归档流程时的正确默认选择。某些工作跨越多个仓库或文件夹。对于这种情况，OpenSpec 协调工作区是一个机器本地视图，将链接路径、打开方式状态和 agent 设置整合在一起。

工作区的心理模型是：

```text
workspace     = 上下文存储、initiatives、仓库和文件夹的私有本地视图
context store = 持久化共享上下文容器
initiative    = 上下文存储内部的持久化协调上下文
link          = 工作区可以在本地解析的仓库或文件夹的稳定名称
change        = 一个计划的工作单元；实施属于拥有它的仓库
```

工作区与仓库本地项目有不同的形态：

```text
getGlobalDataDir()/workspaces/<workspace-name>/
├── workspace.yaml                 # 私有本地视图记录
├── AGENTS.md                      # 生成的运行时指导
└── <workspace-name>.code-workspace # 生成的编辑器工作区文件
```

仓库本地 OpenSpec 状态保持现有形态：

```text
repo-root/
└── openspec/
    ├── specs/
    └── changes/
```

这个区别很重要。工作区文件夹是一个用于打开和检查链接仓库或文件夹的本地协调层。每个仓库的 `openspec/` 目录仍然是仓库拥有的 specs、仓库本地变更和实施规划的家园。用户无需在工作区文件夹内运行仓库本地 `openspec init`。

稳定的链接名称是工作区引用仓库和文件夹的方式。私有工作区记录保留诸如 `api`、`web` 或 `checkout` 等名称，并将其映射到此运行时的本地路径。

```yaml
# workspace.yaml
version: 1
name: platform
context: null
links:
  api: /repos/api
  web: /repos/web
```

当工作区打开一个 initiative 时，`context` 记录选中的上下文存储绑定和 initiative ID。通过注册表选择的存储通过 ID 保持可移植性；通过路径选择的存储有意保留运行时本地路径，因为 `workspace.yaml` 是私有本地状态。

```yaml
context:
  kind: initiative
  store:
    id: platform
    selector:
      kind: registry
      id: platform
  initiative:
    id: billing-launch
```

链接的路径可以是完整的仓库、大型 monorepo 内的文件夹或其他现有文件夹。它们不需要仓库本地 `openspec/` 状态即可参与工作区规划。后续的实施、验证或归档工作流可能需要更多的仓库就绪状态，但规划可见性从链接开始。

```text
多仓库：
  api      -> /repos/api
  web      -> /repos/web

大型 monorepo：
  billing  -> /repos/platform/services/billing
  checkout -> /repos/platform/apps/checkout
```

管理的工作区位于标准 OpenSpec 数据目录下：

```text
getGlobalDataDir()/workspaces
```

这意味着当设置了 `XDG_DATA_HOME` 时为 `$XDG_DATA_HOME/openspec/workspaces`，Unix 风格回退为 `~/.local/share/openspec/workspaces`，原生 Windows 回退为 `%LOCALAPPDATA%\openspec\workspaces`。原生 Windows Shell、PowerShell 和 WSL2 各自保留运行 OpenSpec 的运行时路径字符串。这一基础不支持在 `D:\repo`、`/mnt/d/repo` 和 UNC WSL 路径之间转换。

OpenSpec 仍然可以读取旧的 beta 工作区根目录作为兼容性输入，但管理工作区现在使用上面的根 `workspace.yaml` 记录。工作区文件夹仍然是其自身私有本地视图的权威来源。

工作区可见性不等于变更提交。当 OpenSpec 应该知道哪些仓库或文件夹相关时设置工作区；当您准备好规划功能、修复、项目或其他工作单元时再创建变更。

有用的命令：

```bash
# 引导式设置
openspec workspace setup

# 自动化友好的设置
openspec workspace setup --no-interactive --name platform --link /repos/api --link web=/repos/web
openspec workspace setup --no-interactive --name platform --link /repos/api --opener codex-cli

# 查看本地注册表中的已知工作区
openspec workspace list
openspec workspace ls

# 为所选工作区添加或修复链接
openspec workspace link /repos/api
openspec workspace link api-service /repos/api
openspec workspace relink api-service /new/path/to/api

# 检查此机器可以解析的内容
openspec workspace doctor
openspec workspace doctor --workspace platform

# 刷新工作区本地指导和 agent skills
openspec workspace update
openspec workspace update --workspace platform --tools codex,claude

# 打开链接的工作集
openspec workspace open
openspec workspace open platform --agent github-copilot
openspec workspace open --editor

# 将 initiative 作为本地工作区视图打开
openspec workspace open --initiative billing-launch --store platform
openspec workspace open --initiative billing-launch --store-path /repos/platform-context
```

`workspace setup` 总是在标准工作区位置创建工作区，将其记录在本地注册表中，显示工作区位置，并要求至少一个链接的仓库或文件夹。交互式设置询问首选打开方式，并可以为选中的 agent 安装 OpenSpec skills。非交互式设置仅在提供了 `--opener codex-cli`、`--opener claude`、`--opener github-copilot` 或 `--opener editor` 时存储一个。

工作区 skills 仅安装在工作区根目录。激活的全局 profile 选择生成哪些工作流 skills；`--tools` 选择哪些 agent 接收它们。工作区设置和更新不会创建斜杠命令文件，即使全局交付方式包含 commands。运行 `openspec workspace update` 刷新工作区本地指导，并添加、刷新或移除管理工作区本地 skill 目录，无需编辑链接的仓库或文件夹。

OpenSpec 还维护根工作区打开文件：`AGENTS.md` 中的 OpenSpec 管理指导块，以及用于 VS Code 和 GitHub Copilot-in-VS-Code 打开的机器本地 `<workspace-name>.code-workspace` 文件。管理工作区不是仓库，因此 OpenSpec 不会创建默认的工作区 `.gitignore` 或默认的工作区级 `changes/` 目录。

维护的 VS Code 工作区首先列出有效的链接仓库或文件夹，然后在附加时列出 initiative 上下文，最后列出 OpenSpec 工作区文件。VS Code 将这些条目显示为多根工作区。

`workspace open` 使用存储的首选打开方式打开链接的工作集，除非为那次会话传递了 `--agent <tool>` 或 `--editor`。同时传递两个打开方式覆盖是错误。根工作区打开使链接的仓库和文件夹对探索和上下文可见；实施在用户明确要求实施工作后开始。

`workspace link` 和 `workspace relink` 仅记录现有文件夹；它们不会创建、复制、移动、初始化或编辑链接的仓库或文件夹。成功链接或重新链接后，OpenSpec 刷新管理的指导和 VS Code 工作区文件。

需要单个工作区的工作区命令可以从任何位置运行，使用 `--workspace <name>`。如果您在工作区文件夹或子目录中运行它们，OpenSpec 使用该当前工作区。如果有多个已知工作区可用且您没有传递 `--workspace <name>`，人类命令显示选择器；`--json` 和 `--no-interactive` 会失败并返回结构化状态错误，而不是提示。

直接工作区命令支持 JSON 输出供脚本使用。JSON 响应将主要数据放在 `workspace`、`workspaces` 或 `link` 对象中，并在 `status` 数组中报告警告或错误。健康对象使用 `status: []`。

## Specs

Specs 使用结构化的需求和场景描述您的系统行为。

### 结构

```
openspec/specs/
├── auth/
│   └── spec.md           # 身份认证行为
├── payments/
│   └── spec.md           # 支付处理
├── notifications/
│   └── spec.md           # 通知系统
└── ui/
    └── spec.md           # UI 行为和主题
```

按领域组织 specs——对您的系统有意义的逻辑分组。常见模式：

- **按功能区域**：`auth/`、`payments/`、`search/`
- **按组件**：`api/`、`frontend/`、`workers/`
- **按限界上下文**：`ordering/`、`fulfillment/`、`inventory/`

### Spec 格式

一个 spec 包含需求，每个需求有场景：

```markdown
# 身份认证规范

## 用途
应用程序的身份认证和会话管理。

## 需求

### 需求：用户身份认证
系统在成功登录后应签发 JWT 令牌。

#### 场景：有效凭据
- GIVEN 一个拥有有效凭据的用户
- WHEN 用户提交登录表单
- THEN 返回一个 JWT 令牌
- AND 用户被重定向到仪表板

#### 场景：无效凭据
- GIVEN 无效的凭据
- WHEN 用户提交登录表单
- THEN 显示错误消息
- AND 不签发令牌

### 需求：会话过期
系统必须在 30 分钟不活动后使会话过期。

#### 场景：空闲超时
- GIVEN 一个已认证的会话
- WHEN 30 分钟没有活动
- THEN 会话失效
- AND 用户必须重新认证
```

**关键元素：**

| 元素 | 用途 |
|---------|---------|
| `## 用途` | 此 spec 领域的高级描述 |
| `### 需求：` | 系统必须具有的特定行为 |
| `#### 场景：` | 需求在行动中的具体示例 |
| SHALL/MUST/SHOULD | RFC 2119 关键词，表示需求的强度 |

### 为什么这样组织 Specs

**需求是"什么"**——它们陈述系统应该做什么，而不指定实现方式。

**场景是"何时"**——它们提供可验证的具体示例。好的场景：
- 可测试（您可以为其编写自动化测试）
- 涵盖快乐路径和边界情况
- 使用 Given/When/Then 或类似的结构化格式

**RFC 2119 关键词**（SHALL、MUST、SHOULD、MAY）传达意图：
- **MUST/SHALL** — 绝对需求
- **SHOULD** — 推荐，但存在例外
- **MAY** — 可选

### Spec 是什么（以及不是什么）

Spec 是一个**行为契约**，而不是实施计划。

好的 spec 内容：
- 用户或下游系统依赖的可观察行为
- 输入、输出和错误条件
- 外部约束（安全性、隐私性、可靠性、兼容性）
- 可以测试或显式验证的场景

Specs 中应避免：
- 内部类/函数名称
- 库或框架选择
- 逐步实施细节
- 详细的执行计划（这些属于 `design.md` 或 `tasks.md`）

快速测试：
- 如果实现可以在不改变外部可见行为的情况下更改，那么它可能不属于 spec。

### 保持轻量：渐进式严谨

OpenSpec 旨在避免官僚主义。使用仍然使变更可验证的最轻量级别。

**精简 spec（默认）：**
- 简短的行为优先需求
- 明确的范围和非目标
- 几个具体的验收检查点

**完整 spec（适用于较高风险）：**
- 跨团队或跨仓库变更
- API/契约变更、迁移、安全/隐私问题
- 歧义可能导致昂贵的返工的变更

大多数变更应保持在精简模式。

### 人类 + Agent 协作

在许多团队中，人类进行探索，agent 起草产物。预期的循环是：

1. 人类提供意图、上下文和约束。
2. Agent 将其转换为行为优先的需求和场景。
3. Agent 将实施细节保留在 `design.md` 和 `tasks.md` 中，而不是 `spec.md`。
4. 验证在实施前确认结构和清晰度。

这使 specs 对人类可读，对 agent 保持一致。

## 变更

变更是对系统的提议修改，打包为一个文件夹，包含理解和实施所需的一切。

### 变更结构

```
openspec/changes/add-dark-mode/
├── proposal.md           # 原因和内容
├── design.md             # 如何（技术方法）
├── tasks.md              # 实施检查清单
├── .openspec.yaml        # 变更元数据（可选）
└── specs/                # Delta specs
    └── ui/
        └── spec.md       # ui/spec.md 中正在更改的内容
```

每个变更是自包含的。它有：
- **产物** — 捕获意图、设计和任务的文档
- **Delta specs** — 关于添加、修改或删除内容的规范
- **元数据** — 此特定变更的可选配置

### 为什么变更是文件夹

将变更打包为文件夹有几个好处：

1. **一切在一起。** Proposal、设计、任务和 specs 位于一个位置。无需在不同位置之间寻找。

2. **并行工作。** 多个变更可以同时存在而无冲突。在 `add-dark-mode` 进行中的同时处理 `fix-auth-bug`。

3. **干净的历史。** 归档后，变更移至 `changes/archive/` 并保留其完整上下文。您可以回顾并理解不仅更改了什么，还有为什么。

4. **审查友好。** 变更文件夹易于审查——打开它，阅读 proposal，检查设计，查看 spec deltas。

## 产物

产物是变更内指导工作的文档。

### 产物流

```
proposal ──────► specs ──────► design ──────► tasks ──────► implement
    │               │             │              │
   为什么         什么          如何          步骤
  + 范围         变更         方法          执行
```

产物相互构建。每个产物为下一个提供上下文。

### 产物类型

#### Proposal（`proposal.md`）

Proposal 在高级别捕获**意图**、**范围**和**方法**。

```markdown
# 提案：添加暗色模式

## 意图
用户要求添加暗色模式选项，以减少夜间使用时的眼睛疲劳，
并匹配系统偏好。

## 范围
范围内：
- 设置中的主题切换开关
- 系统偏好检测
- 在 localStorage 中持久化偏好

范围外：
- 自定义颜色主题（未来工作）
- 每页主题覆盖

## 方法
使用 CSS 自定义属性进行主题化，使用 React Context
进行状态管理。首次加载时检测系统偏好，
允许手动覆盖。
```

**何时更新 proposal：**
- 范围变化（缩小或扩大）
- 意图明确（更好地理解问题）
- 方法发生根本性转变

#### Specs（`specs/` 中的 delta specs）

Delta specs 描述相对于当前 specs **正在更改的内容**。请参见下文中的 [Delta Specs](#delta-specs)。

#### 设计（`design.md`）

设计捕获**技术方法**和**架构决策**。

````markdown
# 设计：添加暗色模式

## 技术方法
通过 React Context 管理主题状态，以避免 prop 穿透。
CSS 自定义属性支持运行时切换，无需类切换。

## 架构决策

### 决策：使用 Context 而非 Redux
对主题状态使用 React Context，因为：
- 简单的二元状态（亮/暗）
- 没有复杂的状态转换
- 避免添加 Redux 依赖

### 决策：CSS 自定义属性
使用 CSS 变量而非 CSS-in-JS，因为：
- 与现有样式表兼容
- 无运行时开销
- 浏览器原生解决方案

## 数据流
```
ThemeProvider (context)
       │
       ▼
ThemeToggle ◄──► localStorage
       │
       ▼
CSS Variables (applied to :root)
```

## 文件更改
- `src/contexts/ThemeContext.tsx`（新增）
- `src/components/ThemeToggle.tsx`（新增）
- `src/styles/globals.css`（已修改）
````

**何时更新设计：**
- 实施揭示此方法行不通
- 发现更好的解决方案
- 依赖或约束发生变化

#### 任务（`tasks.md`）

任务是**实施检查清单**——带有复选框的具体步骤。

```markdown
# 任务

## 1. 主题基础设施
- [ ] 1.1 创建具有亮/暗状态的 ThemeContext
- [ ] 1.2 添加颜色相关的 CSS 自定义属性
- [ ] 1.3 实现 localStorage 持久化
- [ ] 1.4 添加系统偏好检测

## 2. UI 组件
- [ ] 2.1 创建 ThemeToggle 组件
- [ ] 2.2 将切换开关添加到设置页面
- [ ] 2.3 更新 Header 以包含快速切换

## 3. 样式
- [ ] 3.1 定义暗色主题调色板
- [ ] 3.2 更新组件以使用 CSS 变量
- [ ] 3.3 测试对比度以确保可访问性
```

**任务最佳实践：**
- 在标题下分组相关任务
- 使用分层编号（1.1、1.2 等）
- 保持任务足够小，以便在一次会话中完成
- 完成后勾选任务

## Delta Specs

Delta specs 是使 OpenSpec 适用于棕地开发的关键概念。它们描述**正在更改的内容**，而不是重述整个 spec。

### 格式

```markdown
# 身份认证的 Delta

## 已添加的需求

### 需求：双因素身份认证
系统必须支持基于 TOTP 的双因素身份认证。

#### 场景：2FA 注册
- GIVEN 一个未启用 2FA 的用户
- WHEN 用户在设置中启用 2FA
- THEN 显示用于认证器应用设置的二维码
- AND 用户必须通过代码验证后才能激活

#### 场景：2FA 登录
- GIVEN 一个已启用 2FA 的用户
- WHEN 用户提交有效凭据
- THEN 显示 OTP 挑战
- AND 仅在有效 OTP 后完成登录

## 已修改的需求

### 需求：会话过期
系统必须在 15 分钟不活动后使会话过期。
（之前：30 分钟）

#### 场景：空闲超时
- GIVEN 一个已认证的会话
- WHEN 15 分钟没有活动
- THEN 会话失效

## 已移除的需求

### 需求：记住我
（已弃用，改用 2FA。用户应在每个会话中重新认证。）
```

### Delta 部分

| 部分 | 含义 | 归档时发生的情况 |
|---------|---------|------------------------|
| `## 已添加的需求` | 新行为 | 追加到主 spec |
| `## 已修改的需求` | 更改的行为 | 替换现有需求 |
| `## 已移除的需求` | 已弃用的行为 | 从主 spec 中删除 |

### 为什么使用 Deltas 而非完整 Specs

**清晰。** Delta 精确显示正在更改的内容。阅读完整 spec，您需要在心里对比当前版本进行差异比较。

**避免冲突。** 两个变更可以涉及相同的 spec 文件而不冲突，只要它们修改不同的需求。

**审查效率。** 审查者看到变更，而不是未更改的上下文。关注重要内容。

**棕地适配。** 大多数工作修改现有行为。Deltas 使修改成为一等公民，而非事后考虑。

## Schemas

Schemas 定义工作流的产物类型及其依赖关系。

### Schema 如何工作

```yaml
# openspec/schemas/spec-driven/schema.yaml
name: spec-driven
artifacts:
  - id: proposal
    generates: proposal.md
    requires: []              # 无依赖，可以首先创建

  - id: specs
    generates: specs/**/*.md
    requires: [proposal]      # 创建前需要 proposal

  - id: design
    generates: design.md
    requires: [proposal]      # 可以与 specs 并行创建

  - id: tasks
    generates: tasks.md
    requires: [specs, design] # 需要 specs 和 design 都存在
```

**产物形成一个依赖关系图：**

```
                    proposal
                   (根节点)
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
      specs                       design
   (需要：                      (需要：
    proposal)                    proposal)
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
                    tasks
                (需要：
                specs, design)
```

**依赖关系是使能器，而非门控。** 它们显示可以创建什么，而不是您必须下一步创建什么。如果不需要，您可以跳过设计。您可以在设计之前或之后创建 specs——两者都只依赖于 proposal。

### 内置 Schema

**spec-driven**（默认）

规范驱动开发的标准工作流：

```
proposal → specs → design → tasks → implement
```

最适合：大多数功能工作，您希望在实施前就 specs 达成一致。

### 自定义 Schema

为您的团队工作流创建自定义 schema：

```bash
# 从零创建
openspec schema init research-first

# 或 fork 一个现有的
openspec schema fork spec-driven research-first
```

**自定义 schema 示例：**

```yaml
# openspec/schemas/research-first/schema.yaml
name: research-first
artifacts:
  - id: research
    generates: research.md
    requires: []           # 先做研究

  - id: proposal
    generates: proposal.md
    requires: [research]   # 提案由研究提供信息

  - id: tasks
    generates: tasks.md
    requires: [proposal]   # 跳过 specs/design，直接到 tasks
```

有关创建和使用自定义 schema 的完整详细信息，请参阅[自定义](customization.md)。

## 归档

归档通过将 delta specs 合并到主 specs 并将变更保留在历史记录中来完成变更。

### 归档时发生的情况

```
归档前：

openspec/
├── specs/
│   └── auth/
│       └── spec.md ◄────────────────┐
└── changes/                         │
    └── add-2fa/                     │
        ├── proposal.md              │
        ├── design.md                │ 合并
        ├── tasks.md                 │
        └── specs/                   │
            └── auth/                │
                └── spec.md ─────────┘


归档后：

openspec/
├── specs/
│   └── auth/
│       └── spec.md        # 现在包含 2FA 需求
└── changes/
    └── archive/
        └── 2025-01-24-add-2fa/    # 保留在历史记录中
            ├── proposal.md
            ├── design.md
            ├── tasks.md
            └── specs/
                └── auth/
                    └── spec.md
```

### 归档过程

1. **合并 deltas。** 每个 delta spec 部分（已添加/已修改/已移除）被应用到相应主 spec。

2. **移至归档。** 变更文件夹移至 `changes/archive/`，带有日期前缀以按时间顺序排列。

3. **保留上下文。** 所有产物在归档中保持完整。您可以随时回顾以了解为什么进行了某个变更。

### 为什么归档很重要

**干净的状态。** 活跃变更（`changes/`）仅显示进行中的工作。已完成的工作移开。

**审计追踪。** 归档保留每个变更的完整上下文——不仅是更改了什么，还有解释为什么的 proposal、解释如何的设计以及展示所完成工作的任务。

**Spec 演进。** 随着变更被归档，specs 有机地增长。每次归档合并其 deltas，随着时间的推移建立起全面的规范。

## 一切如何协同工作

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              OPENSPEC 流程                                   │
│                                                                              │
│   ┌────────────────┐                                                         │
│   │  1. 开始变更   │  /opsx:propose（core）或 /opsx:new（扩展）               │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐                                                         │
│   │  2. 创建产物   │  /opsx:ff 或 /opsx:continue（扩展工作流）                │
│   │                │  创建 proposal → specs → design → tasks                 │
│   │                │  （基于 schema 依赖关系）                                │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐                                                         │
│   │  3. 实施任务   │  /opsx:apply                                            │
│   │                │  逐项完成任务，勾选完成                                  │
│   │                │◄──── 边学习边更新产物                                    │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐                                                         │
│   │  4. 验证工作   │  /opsx:verify（可选）                                    │
│   │                │  检查实施是否匹配 specs                                  │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐     ┌──────────────────────────────────────────────┐    │
│   │  5. 归档变更   │────►│  Delta specs 合并到主 specs                   │    │
│   │                │     │  变更文件夹移至 archive/                      │    │
│   └────────────────┘     │  Specs 现在是更新的唯一真相来源               │    │
│                          └──────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**良性循环：**

1. Specs 描述当前行为
2. 变更提议修改（作为 deltas）
3. 实施使变更成为现实
4. 归档将 deltas 合并到 specs
5. Specs 现在描述新行为
6. 下一个变更基于更新的 specs

## 术语表

| 术语 | 定义 |
|------|------------|
| **产物（Artifact）** | 变更内的文档（proposal、design、tasks 或 delta specs） |
| **归档（Archive）** | 完成变更并将其 deltas 合并到主 specs 的过程 |
| **变更（Change）** | 对系统的提议修改，打包为一个包含产物的文件夹 |
| **Delta spec** | 描述相对于当前 specs 的更改（已添加/已修改/已移除）的 spec |
| **领域（Domain）** | Specs 的逻辑分组（例如 `auth/`、`payments/`） |
| **需求（Requirement）** | 系统必须具有的特定行为 |
| **场景（Scenario）** | 需求的具体示例，通常采用 Given/When/Then 格式 |
| **Schema** | 产物类型及其依赖关系的定义 |
| **Spec** | 描述系统行为的规范，包含需求和场景 |
| **唯一真相来源（Source of truth）** | `openspec/specs/` 目录，包含当前商定的行为 |

## 下一步

- [快速入门](getting-started.md) - 实际的第一步
- [工作流](workflows.md) - 常见模式及何时使用每个命令
- [命令](commands.md) - 完整的命令参考
- [自定义](customization.md) - 创建自定义 schema 和配置您的项目
