# workspace 用户旅程

## 目的

本文档描述了 OpenSpec 在以下场景中的精确用户体验：

1. 单 repository 项目
2. Monorepo
3. 行为类似多个 repository 的大型 Monorepo
4. 真正的多 repository 行动倡议

本文有意以用户体验为先。目标是定义：

- 用户从哪里开始
- 他们运行什么命令
- Agent 看到什么
- 产物存储在哪里
- OpenSpec 如何决定读取哪些 spec
- 当 repository 根缺失、不明确或部分可用时，OpenSpec 的行为

这是一个提议的用户体验模型，而不是实现 spec。

---

## 核心心智模型

用户不应该需要为 repository 准备一种心智模型，而为 monorepo 准备另一种心智模型。

OpenSpec 应该基于**范围（scopes）**运作。

一个范围是一个拥有所有权界限的 planning 和实现边界。根据代码库的不同，一个范围可以是：

- 整个 repository
- monorepo 内的一个包或应用
- monorepo 内的一个服务
- 一个共享契约领域
- 其他明确拥有的域

用户体验应该是：

- 选择你想要变更的东西
- 确认涉及哪些范围
- OpenSpec 只读取相关的 spec
- OpenSpec 将每个产物存储在所属位置
- 如果工作跨越多个所属位置，OpenSpec 创建一个中立的协调 workspace

### 持久对象

有三个不同的持久对象：

1. **spec（Spec）**
 一个 spec 化的行为契约。始终存储在所属范围中。

2. **变更（Change）**
 一个 repository 本地或范围本地的 planning 产物。随实现/spec 差异的拥有者一起存储。

3. **行动倡议（Initiative）**
 一个跨范围协调产物。仅在工作跨越多个拥有根时需要。存储在中立的协调 workspace 中。

关键规则是：

> spec 化 spec 永远不会移动到协调 workspace 中。

workspace 负责协调。拥有根仍然是 spec 化的。

### 跨边界 spec

有些行为真正跨越多个范围、应用或 repository：

- 由 Web、iOS、Android 和后端共享的 checkout 行为
- 应用客户端和 API 服务共享的认证/会话规则
- 发票、支付和报告共享的计费规则
- 跨多个系统共享的隐私或审计保证

这些不仅仅是"本地 spec 之间的引用"。它们是第一类共享契约。

OpenSpec 应将其明确建模为：

1. **spec 化共享契约**
 一个定义跨边界必须成立的 spec 的 spec。

2. **本地实现 spec**
 每个范围的 spec，描述每个拥有者如何在本地满足该契约。

3. **行动倡议**
 一个用于一起更新契约及其实现的变更或项目。

第一性原则规则是：

> 一个跨边界 spec 可能有许多消费者，但它仍然必须有一个 spec 化的拥有者。

如果还没有拥有者，共享行为可以在探索期间临时作为行动倡议笔记存在，但 OpenSpec 不应在所有权明确之前将其提升为 spec 化 spec。

---

## 用户体验原则

### 1. 任何地方都使用相同的顶层 workflow

用户应该仍然能认出现有的 OpenSpec workflow：

- `openspec init`
- `openspec update`
- `/opsx:explore`
- `/opsx:propose`
- `/opsx:apply`
- `/opsx:archive`

新的行为是 OpenSpec 可能会问：

- "这影响哪个范围？"
- "这跨越多个拥有根吗？"
- "我应该创建一个协调 workspace 吗？"

### 2. 不需要事先注册 workspace

用户不应该为了以防万一而预先注册所有 repository 或模块。

OpenSpec 应支持：

- 临时发现
- 一次性本地链接
- 可选的后保存 workspace

### 3. 跨根 planning 必须有一个中立的家

如果一个变更跨越多个 repository，planning 产物不应被强制放在某个 repository 中。

相反，OpenSpec 应为行动倡议创建一个中立的协调 workspace。

### 4. spec 化存储跟随所有权

- 共享契约 spec 存储在契约拥有的范围中
- Web 特定 spec 存储在 Web 拥有的范围中
- iOS 特定 spec 存储在 iOS 拥有的范围中
- repository 本地代码任务存储在 repository 本地变更中

### 5. 引用是信息性的

跨范围或跨 repository 的 `references` 最初应仅为文档性质。

OpenSpec 可以向用户和 agent 展示它们，但不应要求在第一个版本中跨根解析或验证。

### 6. 共享契约需要明确的所有权

当用户描述跨越多个边界的行为时，OpenSpec 应帮助他们决定他们正在创建的是：

- 一个本地 spec
- 一个共享契约
- 一个尚未成为 spec 化的行动倡议笔记

如果工作是一个真正的长期契约，OpenSpec 应提示选择一个 spec 化拥有者，而不是将其埋在用户碰巧所在的 repository 中。

### 7. 不要将"共享所有权"强制为隐式共同所有权

OpenSpec 应帮助团队创建**共享契约所有权**，而不是模糊的共同所有权。

这意味着：

- 一个范围或 repository 拥有 spec 化共享契约
- 其他范围消费和引用它
- 协调 workspace 可以总结它
- 所有权和审查路径保持清晰

### 8. 仅将当前 repository 作为起点，而非事实依据

当用户在 `web-client` 中开始并描述跨越 web、iOS、Android 和后端的 checkout 行为时，OpenSpec 应将当前 cwd 视为关于可能消费者的线索，而非证明 `web-client` 应拥有共享契约的证据。

---

## 术语

### 项目

一个单一的 OpenSpec 根，spec 化和变更可以存放在其中。

在实践中，项目可以是：

- 带有 `openspec/` 的 repository 根
- 带有一个 `openspec/` 的 monorepo 根
- 如果 OpenSpec 后来支持嵌套根，则是一个嵌套的拥有范围

### 范围

项目内或跨项目的逻辑边界。范围是用户在 planning 期间选择的内容。

示例：

- `repo`
- `contracts/checkout`
- `apps/web`
- `services/billing`
- `mobile/ios`

### 协调 workspace

一个仅用于跨根协调的中立目录。它存储行动倡议级别的 planning 数据和 agent workspace 指令。

示例：

```text
~/work/openspec-workspaces/add-3ds/
 .openspec-workspace/
 workspace.yaml
 initiative.md
 links.yaml
 agents/
 claude.md
 codex.md
```

这个协调 workspace 可以以两种 schema 存在：

1. **个人协调 workspace**
 一个人用于临时或探索性跨根 planning 的本地目录。

2. **共享协调 workspace**
 由团队或多个团队使用的已提交协调 repository 或共享 workspace。

用户体验应支持这两者，而无需更改核心心智模型。

### 拥有根

spec 化拥有 spec、代码库区域或 repository 本地变更的 repository 或范围。

### 共享契约拥有者

spec 化拥有跨边界 spec 的范围或 repository。

这可能是：

- monorepo 内现有的共享契约领域
- 现有的后端/API 契约拥有者
- 一个专门的契约 repository
- 作为 planning 流程的一部分创建的新共享范围

这不应该是用户启动 agent 的位置带来的意外后果。

---

## 推荐的文件结构

### 单 repository

```text
repo/
 openspec/
 specs/
 changes/
 config.yaml
```

### Monorepo

```text
monorepo/
 openspec/
 specs/
 changes/
 config.yaml
 apps/
 web/
 admin/
 services/
 billing/
 packages/
 contracts/
```

可选的范围标记：

```text
monorepo/
 apps/web/openspec.scope.yaml
 services/billing/openspec.scope.yaml
 packages/contracts/openspec.scope.yaml
```

### 带协调 workspace 的多 repository

```text
~/work/
 contracts/
 openspec/
 web-client/
 openspec/
 ios-client/
 openspec/
 openspec-workspaces/
 add-3ds/
 .openspec-workspace/
 workspace.yaml
 initiative.md
 links.yaml
 agents/
 claude.md
 codex.md
```

---

## 发现模型

OpenSpec 需要回答两个独立的问题：

1. 涉及哪些范围？
2. 它们目前在磁盘上的什么位置？

这两个问题并不相同。

### 范围发现

OpenSpec 从以下来源发现候选项：

- 当前 repository 根
- `openspec/specs/**`
- 可选的范围标记文件
- 先前的行动倡议元数据
- 用户明确选择

### 根解析

对于多 repository 工作，持久标识符不应是原始路径。

稳定的项目标识符应如下所示：

- `github.com/Fission-AI/web-client`
- `github.com/Fission-AI/contracts`

用户简写可以接受：

- `Fission-AI/web-client`
- `fission/web-client`

OpenSpec 使用以下顺序将这些解析为本地路径：

1. 本次运行的显式传入路径
2. 已保存的本地 OpenSpec 注册表
3. 本地 git remote 扫描
4. 用户提示

像 `../web-client` 这样的相对路径可以作为单次运行的临时提示使用，但不应成为持久标识符。

### 共享清单 vs 本地覆盖

对于团队使用，OpenSpec 应区分：

1. **共享协调状态**
 可以提交并与团队成员共享的稳定信息。

2. **本地解析状态**
 特定机器的路径映射和本地可用性。

#### 共享协调状态应包括

- 行动倡议 ID 和摘要
- 稳定的项目标识符
- 选定的范围
- 链接的 repository 本地变更 ID
- 所有权元数据
- 发布或排序说明
- 未解决但已知的参与项目

#### 本地解析状态应包括

- 项目标识符的本地文件系统路径
- 本地 repository 可用性
- 多个匹配中的本地首选克隆
- 特定机器的 agent 附加提示

这种分离对于连贯的团队故事至关重要。

没有它，协调 workspace 要么变得：

- 过于本地化而无法共享，要么
- 充斥着特定机器的路径，对团队成员来说无法使用

---

## 团队协作模型

本节描述同一用户体验应如何从一个人扩展到大型组织。

### 最小单元：一个用户，一台机器

用户可以创建本地协调 workspace 并保持一切本地化。

这对于以下情况没问题：

- 一次性的跨 repository 探索
- 共享前的私有 planning
- 尝试多 repository 想法

### 团队单元：共享行动倡议

一旦跨 repository 工作变得协作，协调 workspace 应该是可共享和可提交的。

这意味着：

- 行动倡议元数据被提交
- 所有权决策被提交
- 链接的变更被提交
- 本地路径不被提交

### 跨团队单元：发起式行动倡议

当工作跨越团队时，行动倡议需要明确的协调拥有者，即使 spec 和代码保持分布式。

这与 spec 化 spec 所有权不同。

现在有两个不同的职责：

1. **共享契约拥有者**
 拥有 spec 化跨边界 spec。

2. **行动倡议发起人/推动者**
 拥有当前变更的协调过程。

它们可能是同一团队，但不一定。

示例：

- 平台团队发起发布，认证团队拥有 spec 化认证契约
- 支付团队发起行动倡议，契约 repository 拥有 spec 化 checkout 契约
- 移动平台团队发起全应用迁移，后端团队拥有 API 契约

### 我们应该告诉团队什么

OpenSpec 应清晰地传达这一点：

> 如果工作是协作性的，将协调 workspace 视为一个轻量级共享 planning repository 或已提交的 workspace。在那里提交稳定的行动倡议元数据，并将特定机器的 repository 路径映射保留在本地。

这提供了清晰的答案：

- 我们如何共享跨 repository 计划？
- 团队成员如何打开同一个行动倡议？
- 拥有不同本地克隆布局的人如何在同一行动倡议上工作？

---

## 所有权决策模型

本节回答一个关键的产品问题：

> 团队或 agent 应如何决定共享跨边界 spec 属于哪里？

### 第一性原理启发式

OpenSpec 应帮助团队选择最可信地能够做到以下所有事情的拥有者：

1. 定义保证
2. 审查和批准对该保证的变更
3. 向消费者传达该保证
4. 在保证变更时吸收协调成本

拥有者不一定是：

- 发起变更的团队
- 前端团队
- 后端团队
- 代码最多的 repository

拥有者是最稳定和最权威的边界。

### 所有权决策问题

当 OpenSpec 检测到可能的共享契约时，它应询问或从以下问题推断：

1. 这个行为是否旨在长期跨多个范围成立？
2. 这是一个外部契约、内部产品规则还是实现细节？
3. 哪个团队或范围可以批准对此契约的变更？
4. 消费者自然会看哪个拥有者作为事实来源？
5. 共享契约领域是否已经存在？
6. 这个契约是否会比当前行动倡议存活得更久？

### 推荐的结果

#### 结果 A：已有现有拥有者

示例：

- monorepo 中已存在 `packages/contracts/checkout`
- 多 repository 环境中已存在 `contracts` repository

OpenSpec 应默认使用该现有拥有者。

#### 结果 B：共享契约属于现有域拥有者

示例：

- API 请求/响应契约属于 API/后端拥有者
- 共享认证令牌契约属于认证平台拥有者

如果没有专门的共享领域，OpenSpec 应建议该现有域拥有者。

#### 结果 C：应创建新的共享契约范围

示例：

- checkout 行为在多个客户端和服务之间共享
- 没有现有的共享拥有者
- 这可能会重复出现，需要长期治理

OpenSpec 应帮助创建新的共享契约范围。

#### 结果 D：暂时保持为仅行动倡议

示例：

- 团队仍在探索
- 边界不明确
- 目前还没有人能回答谁应该拥有 spec 化保证

OpenSpec 应允许该行为暂时保留在行动倡议笔记中，并明确标记为非 spec 化，直到选择所有权。

### OpenSpec 默认应建议的内容

#### 对于 Monorepo

默认建议顺序：

1. monorepo 内现有的共享契约范围
2. 现有的域/平台拥有者
3. 在 monorepo 内创建新的共享范围
4. 保持为仅行动倡议直到明确

#### 对于多 repository 环境

默认建议顺序：

1. 现有的 contracts/shared-specs repository
2. 已经拥有稳定契约的现有域/平台 repository
3. 创建专门的共享契约 repository 或范围
4. 保持为仅行动倡议直到明确

### OpenSpec 不应做的事

OpenSpec 不应：

- 悄悄将所有权分配给用户启动所在的 repository
- 在所有消费者中复制 spec 化共享 spec
- 在没有选择拥有者的情况下称某物为 spec 化
- 在团队能够 planning 之前强制要求中央管理设置

---

## 共享契约创建用户体验

当用户描述可能的跨边界行为时，OpenSpec 应将其视为第一类 planning 时刻。

### 检测线索

可能需要共享契约的信号：

- 请求提到多个平台或 repository
- 请求提到"共享"、"通用"、"契约"、"相同行为"、"跨平台一致"
- 选定的范围包括客户端加后端
- 没有现有 spec 清晰地拥有所描述的行为

### 提示形态

在 `/opsx:propose` 或 `/opsx:explore` 期间，OpenSpec 应询问如下内容：

```text
这看起来像是跨多个范围共享的行为：
- web
- iOS
- Android
- backend

这是什么类型的产物？
- 一个范围内的本地变更
- 多个范围必须遵循的共享契约
- 暂时作为行动倡议笔记；所有权尚不明确
```

如果用户选择共享契约：

```text
spec 化共享契约应该放在哪里？
- 现有共享契约范围
- 现有域拥有者
- 创建新的共享契约范围
- 稍后决定，暂时保持为仅行动倡议
```

### 创建新的共享契约范围

如果用户选择"创建新的共享契约范围"，OpenSpec 应引导他们。

#### Monorepo

提示感觉：

```text
建议的新共享范围：
- openspec/specs/contracts/checkout
- openspec/specs/shared/checkout
- packages/contracts/checkout

谁应该拥有此契约的审查权？
```

然后 OpenSpec：

1. 在选定的共享范围中创建 spec 化共享 spec
2. 记录选定的消费者
3. 如果需要，在消费者变更/spec 中生成本地引用

#### 多 repository

提示感觉：

```text
尚无共享契约拥有者。

选择 spec 化契约应放在何处：
- 在现有契约 repository 中创建
- 稍后创建新的共享契约 repository；暂时保持为仅行动倡议
- 分配给现有域拥有者 repository
```

OpenSpec 应避免自动创建全新的 repository。它可以搭建计划并记录决策，但 repository 创建可能涉及组织敏感性，通常不属于 CLI 的范畴。

### 临时仅行动倡议 schema

如果所有权不明确，OpenSpec 应支持：

- 将共享行为存储在行动倡议 workspace 中作为草稿笔记
- 明确标记为非 spec 化
- 提醒用户在进行长期采用之前将其提升为 spec 化共享契约

这很重要，因为许多团队在探索过程中发现了共享契约的需求，但在知道如何治理之前。

---

## 跨团队规模的连贯用户体验

产品应该感觉像一个系统，而不是三个独立的功能。

### 不变的 workflow

无论环境如何，用户体验应始终简化为：

1. 从当前位置开始
2. 描述工作内容
3. 确认受影响的范围内
4. 让 OpenSpec 判断这是：
 - 仅本地
 - 单根内的多范围
 - 跨根协调
5. OpenSpec 在正确的位置创建产物
6. OpenSpec 告诉用户在哪里继续 planning，在哪里实现

### 按规模变化的因素

#### 个人 / 单 repository

- 入口：repository 根
- 可共享性：不相关
- 仅本地存储即可

#### 个人 / 临时多 repository

- 入口：本地协调 workspace
- 可共享性：可选
- 本地路径映射足够

#### 团队 / 协作多 repository

- 入口：共享协调 repository/workspace
- 可共享性：必需
- 稳定清单已提交，本地路径私有

#### 大型组织 / 跨团队行动倡议

- 入口：共享协调 repository/workspace
- 发起人/推动者明确
- 共享契约所有权明确
- 某些参与团队可能只在本地解析部分根

### 应保持一致的内容

以下内容不应随组织规模变化：

- spec 化 spec 与拥有者共存
- 本地代码变更与拥有者共存
- 共享契约需要一个 spec 化拥有者
- 协调数据不是 spec 化 spec 的来源
- 本地机器路径永远不是持久标识符
- 即使 planning 是协调的，实现仍然可以逐个根进行

如果这些不变量成立，那么在个人、团队和全组织范围内的用户体验将保持连贯。

---

## Agent 访问模型

跨根用户体验仅在 agent 实际能够看到相关根时才有效。

OpenSpec 应支持三个 agent 能力级别。

### 级别 1：强大的多根支持

工具可以显式地将多个目录附加到一个会话。

期望的用户体验：

- 用户打开协调 workspace
- OpenSpec 明确告诉用户要附加哪些根
- Agent 从所有附加的根读取

### 级别 2：单个 cwd 但对链接根的文件系统访问

工具从一个工作目录运行，但如果环境允许，仍然可以读取兄弟绝对路径。

期望的用户体验：

- 用户打开协调 workspace
- OpenSpec 将 agent 可读的绝对路径写入 workspace 指令
- Agent 可以直接读取那些根

### 级别 3：实际上单根

工具只能可靠地在单个 repository 内操作。

期望的用户体验：

- 协调 workspace 仅用于 planning
- OpenSpec 引导用户随后进入 repository 本地的实现会话
- `/opsx:apply` 在每个 repository 中单独运行

这必须作为第一类情况处理，而不是事后补救的退路。

---

## 需要保留的当前 OpenSpec 流程

今天的流程是：

1. 用户进入一个 repository
2. 用户运行 `openspec init`
3. 用户在该 repository 中打开 agent
4. 用户运行 `/opsx:explore` 或 `/opsx:propose`
5. OpenSpec 将变更存储在 `openspec/changes/<change>/`
6. `/opsx:apply` 在该 repository 内实现

对于单 repository 工作，这应保持完全相同的感受。

唯一的扩展是：

- 如果 OpenSpec 检测到跨根行动倡议，它会显式将 workflow 升级为协调 workspace 流程

---

## 旅程 1：单 repository，标准 OpenSpec 项目

### 起始状态

用户有一个 repository：

```text
~/work/acme-app/
```

他们进入 repository：

```bash
cd ~/work/acme-app
```

他们初始化 OpenSpec：

```bash
openspec init
```

OpenSpec 创建：

```text
openspec/
 specs/
 changes/
 config.yaml
```

他们在该 repository 内打开 Claude、Codex、Cursor 或其他 agent。

### planning

用户输入：

```text
/opsx:propose add-dark-mode
```

OpenSpec 应：

1. 检测到单一的本地项目
2. 检测到单一默认范围：repository
3. 创建一个 repository 本地变更
4. 仅读取本地项目配置和本地 spec
5. 生成本地 planning 产物

输出感觉：

```text
已创建 openspec/changes/add-dark-mode/
使用范围：repo

已生成：
- proposal.md
- specs/ui/spec.md
- design.md
- tasks.md

可以使用 /opsx:apply 进行实现
```

### 实现

用户输入：

```text
/opsx:apply
```

OpenSpec 读取：

- proposal
- specs
- design
- tasks

仅从这个 repository。

### archive

用户输入：

```text
/opsx:archive
```

OpenSpec 像今天一样在该 repository 中 archive 变更。

### 存储结果

- spec 差异存储在此 repository 中
- spec 化 spec 存储在此 repository 中
- 任务和设计存储在此 repository 中
- 未展示 workspace 概念

### 边缘情况

- repository 中有多个活跃变更：提示用户选择一个
- 缺少 spec 目录：如果当前 schema 行为允许则继续
- 用户从子目录运行：OpenSpec 应向上查找或明确告知从 repository 根目录运行

---

## 旅程 2：Monorepo，小团队，一个明显的范围

### 起始状态

用户有：

```text
~/work/platform/
```

内部：

```text
platform/
 openspec/
 apps/web/
 services/api/
 packages/ui/
```

用户进入 monorepo 根目录并在那里运行 agent。

### planning

用户输入：

```text
/opsx:propose add-invoice-filtering
```

OpenSpec 检测到这仍然是一个项目根，但有多个候选项。

如果用户的请求明确提到一个领域，OpenSpec 可以推断：

- `apps/web`

否则它会问：

```text
此变更影响哪个范围？
- apps/web
- services/api
- packages/ui
- shared/contracts
```

用户选择 `apps/web`。

### 预期行为

OpenSpec 应：

1. 在 `openspec/changes/add-invoice-filtering/` 下创建一个 monorepo 本地变更
2. 用 `apps/web` 标记该变更
3. 读取与 `apps/web` 相关的 spec
4. 避免将不相关的 monorepo 区域拉入上下文

### 存储结果

- monorepo 根中有一个变更
- 范围选择记录在变更元数据中
- 仅为选定区域生成差异 spec

### 为什么这很重要

用户不应因为他们碰巧在 monorepo 中就感觉在使用不同的产品。

---

## 旅程 3：Monorepo，跨范围变更

### 起始状态

同一个 monorepo：

```text
platform/
 openspec/
 apps/web/
 services/api/
 packages/contracts/
```

### planning

用户输入：

```text
/opsx:propose add-3ds-checkout
```

OpenSpec 检测可能受影响的范围内：

- `packages/contracts`
- `services/api`
- `apps/web`

它询问：

```text
这似乎影响多个范围。
应包含哪些范围？
[x] packages/contracts
[x] services/api
[x] apps/web
[ ] apps/admin
[ ] packages/ui
```

### 预期行为

OpenSpec 创建：

```text
platform/openspec/changes/add-3ds-checkout/
```

变更包括列出所有三个选定范围的范围元数据。

OpenSpec 读取：

- 共享契约 spec
- 计费/checkout 的 API spec
- web checkout spec

OpenSpec 默认忽略不相关的 spec。

### 实现

用户运行：

```text
/opsx:apply
```

OpenSpec 应：

1. 显示多个范围受影响
2. 相应地对任务进行排序
3. 如果 monorepo 仍被视为一个拥有根，则更新一个共享的任务产物

### 存储结果

- monorepo 根中有一个变更
- 多个范围路径的差异 spec
- 所有 spec 化 spec 仍保留在 monorepo 内

### 重要说明

这仍然不是协调 workspace 的情况，因为仍然只有一个拥有项目根。

---

## 旅程 4：行为类似多个 repository 的大型 Monorepo

### 为什么这个旅程存在

一些 monorepo 在操作上等同于多 repository 系统：

- 不同团队拥有不同领域
- 不同的发布节奏
- 许多开发者不应该编辑彼此的 planning 设置
- 跨团队工作是例外

这意味着 OpenSpec 不能假设：

- 一个 monorepo 根自动等于一个 planning 单元

### 起始状态

```text
platform/
 openspec/
 apps/web/
 apps/mobile/
 services/billing/
 services/orders/
 packages/contracts/
```

存在可选的范围标记：

```text
apps/web/openspec.scope.yaml
apps/mobile/openspec.scope.yaml
services/billing/openspec.scope.yaml
packages/contracts/openspec.scope.yaml
```

### planning 本地团队变更

Web 团队进入 monorepo 根目录，或一个能识别 repository 的子工具进入 web 区域。

用户输入：

```text
/opsx:propose add-checkout-loading-state
```

OpenSpec 检测到这仅限于 `apps/web`。

用户应该体验到与单范围变更完全相同的体验。

### planning 跨团队 monorepo 行动倡议

用户输入：

```text
/opsx:propose add-3ds
```

OpenSpec 检测到：

- `packages/contracts`
- `services/billing`
- `apps/web`
- 可能还有 `apps/mobile`

此时 OpenSpec 必须做出产品决策。

#### 推荐行为

如果所有受影响的范围都在一个拥有根下，并且用户对单一的 monorepo 本地变更感到满意，则继续使用一个根级别变更。

如果 monorepo 被配置或推断为行为像多个拥有的子项目，则提供升级到**协调型 monorepo 行动倡议**。

提示感觉：

```text
此 monorepo 有多个独立拥有的范围。

您希望如何 planning 此工作？
- 一个 monorepo 变更
- 带有链接范围变更的协调行动倡议
```

### 协调型 Monorepo 行动倡议

如果用户选择协调流程，OpenSpec 创建：

1. 一个中立的行动倡议 workspace
2. monorepo 根或范围拥有文件夹内的链接范围本地变更

这与多 repository 的概念流程相同，但所有根恰好位于同一个版本控制系统根内。

### 为什么这很重要

这防止了用户体验硬编码"monorepo 总是更简单"的假设。

这个假设对于这个功能所面向的企业风格团队来说是不成立的。

---

## 旅程 5：从某个 repository 内部开始的多 repository 工作

### 起始状态

用户位于：

```text
~/work/web-client
```

他们已经在使用 OpenSpec。

他们在 `web-client` 中打开 Claude 并输入：

```text
/opsx:propose add-3ds
```

在探索或提议生成过程中，发现工作也影响：

- `contracts`
- `billing-service`
- `ios-client`

### 关键用户体验要求

此时 OpenSpec 不应在 `web-client` 内部悄悄创建一个跨 repository 变更。

那会误导人，因为：

- 行动倡议不是由 `web-client` 拥有的
- agent 还没有其他 repository 根
- spec 化 spec 属于其他 repository

### 预期的 OpenSpec 行为

OpenSpec 中断默认的单 repository 流程并说：

```text
这项工作跨越多个拥有根：
- github.com/Fission-AI/contracts
- github.com/Fission-AI/billing-service
- github.com/Fission-AI/web-client
- github.com/Fission-AI/ios-client

对于跨 repository 工作，OpenSpec 建议创建一个协调 workspace。

建议位置：
~/work/openspec-workspaces/add-3ds

现在创建？
```

如果用户同意，OpenSpec 创建该 workspace。

如果用户想要其他位置，他们可以选择。

### 协调 workspace 创建

建议的 CLI 感觉：

```bash
openspec workspace create add-3ds --at ~/work/openspec-workspaces/add-3ds
```

OpenSpec 写入：

```text
~/work/openspec-workspaces/add-3ds/
 .openspec-workspace/
 workspace.yaml
 initiative.md
 links.yaml
 agents/
 claude.md
 codex.md
```

### repository 解析

OpenSpec 现在解析以下内容的本地路径：

- `github.com/Fission-AI/contracts`
- `github.com/Fission-AI/billing-service`
- `github.com/Fission-AI/web-client`
- `github.com/Fission-AI/ios-client`

使用：

1. 已知的本地注册表
2. git remote 扫描
3. 如果需要，用户确认

### Agent 交接

然后 OpenSpec 告诉用户：

```text
下一步：
1. 在 ~/work/openspec-workspaces/add-3ds 中打开你的编码 agent
2. 如果你的工具支持多根，附加这些根：
 - /Users/me/work/contracts
 - /Users/me/work/billing-service
 - /Users/me/work/web-client
 - /Users/me/work/ios-client

OpenSpec 已在此生成 workspace 指令：
.openspec-workspace/agents/claude.md
```

### 从 workspace planning

用户现在在协调 workspace 中启动 agent 并运行：

```text
/opsx:propose add-3ds
```

或者 OpenSpec 可能已经搭建了行动倡议并告诉 agent 继续。

### 存储结果

协调 workspace 存储**行动倡议级别的 planning 对象**：

- proposal.md
- design.md
- 行动倡议摘要
- 跨 repository 范围映射
- 所有权、里程碑、风险和依赖项
- 指向 repository 本地变更的链接
- Agent workspace 指令

每个 repository 存储自己的执行变更：

- `contracts/openspec/changes/add-3ds-contract/`
- `billing-service/openspec/changes/add-3ds-billing/`
- `web-client/openspec/changes/add-3ds-web/`
- `ios-client/openspec/changes/add-3ds-ios/`

这些 repository 本地变更是 repository 特定任务、差异 spec 和本地实现状态所在的地方。

### 为什么这很重要

这给了用户一个真实的答案：

- 我应该站在哪里？
- 变更存放在哪里？
- Agent 如何看到其他 repository？

答案是：

- 进行跨 repository planning 时站在协调 workspace 中
- 将 spec 化变更/spec 保留在它们的拥有者处

---

## 旅程 6：从中立位置开始的多 repository 工作

### 起始状态

用户已经知道工作是跨 repository 的。

他们从一个中立目录开始：

```bash
cd ~/work
```

他们运行：

```bash
openspec workspace create add-3ds --at ~/work/openspec-workspaces/add-3ds
```

或者一个未来的高级快捷方式：

```bash
openspec initiative new add-3ds
```

### OpenSpec 提示

OpenSpec 询问：

```text
涉及哪些 repository 或范围？
```

用户输入：

- `github.com/Fission-AI/contracts`
- `github.com/Fission-AI/billing-service`
- `github.com/Fission-AI/web-client`
- `github.com/Fission-AI/ios-client`

OpenSpec 解析本地克隆并写入 workspace 文件。

### Agent 设置

用户在其 agent 中打开协调 workspace。

OpenSpec 生成的 agent 指令包含：

- 行动倡议摘要
- 可用根
- 所有权映射
- 指导：spec 化 spec 编辑必须写回到拥有根

### planning 行为

当用户运行：

```text
/opsx:explore
```

或

```text
/opsx:propose add-3ds
```

agent 读取：

- workspace 行动倡议元数据
- 来自附加根的相关 spec
- 仅针对选定的 repository/范围

### 存储结果

与旅程 5 相同，但用户从未需要先从一个 repository 开始。

### 为什么这个旅程很重要

一些用户会故意希望行动倡议从一开始就存在于任何单个 repository 之外。

OpenSpec 应直接支持这一点。

---

## 旅程 6A：团队共享的多 repository 行动倡议

### 起始状态

一个团队知道工作跨越多个 repository，并将涉及多个人在多天或数周内完成。

他们创建或选择一个共享协调 repository，例如：

```text
~/work/openspec-initiatives/
```

或者一个团队拥有的 repository，如：

```text
github.com/Fission-AI/initiatives
```

在其内部，OpenSpec 创建：

```text
initiatives/
 add-3ds/
 .openspec-workspace/
 workspace.yaml
 initiative.md
 links.yaml
 agents/
 claude.md
 codex.md
```

### 提交的内容

团队提交：

- 行动倡议摘要
- 稳定的项目 ID
- 选定的范围
- 所有权决策
- 链接的 repository 本地变更 ID
- 发布和状态说明

### 保持本地的内容

每个团队成员将本地路径映射保留在共享 repository 之外，例如在 OpenSpec 本地配置/数据中：

- `github.com/Fission-AI/contracts` -> `/Users/alice/src/contracts`
- `github.com/Fission-AI/contracts` -> `/home/bob/work/contracts`

### 团队成员 workflow

每个团队成员：

1. 克隆或拉取共享协调 repository
2. 运行类似 `openspec workspace doctor` 或 `openspec workspace sync` 的命令
3. 将任何缺失的项目 ID 解析为本地克隆
4. 从共享协调 workspace 打开其 agent

### Agent 启动行为

OpenSpec 使用以下内容生成 agent 指令：

- 已提交的共享清单
- 本地路径覆盖

这意味着每个团队成员看到相同的行动倡议结构，但使用他们自己的有效文件系统路径。

### 为什么这很重要

这是"进入协调 workspace"的团队规模版本。

没有这种区分，这个说法对一个人来说听起来连贯，但在共享 planning 时就会崩溃。

---

## 旅程 6B：带有明确发起人的跨团队行动倡议

### 起始状态

工作跨越：

- 平台/共享契约
- 后端服务
- 多个客户端
- 多个团队

### 预期设置

OpenSpec 应支持在由发起或推动团队拥有的共享协调 repository 中创建行动倡议。

该发起人负责：

- 开启行动倡议
- 链接参与项目
- 跟踪行动倡议状态
- 保持所有权决策可见

但发起人并不自动拥有：

- 所有 spec
- 所有实现变更
- spec 化共享契约

### 示例

- 支付团队发起 `add-3ds`
- 契约 repository 拥有 spec 化 checkout 契约
- Web 团队拥有 web 实现变更
- iOS 团队拥有 iOS 实现变更
- 计费团队拥有后端实现变更

### 用户体验

当另一个团队成员打开共享协调 workspace 时，OpenSpec 应明确说明：

```text
行动倡议发起人：
- payments-platform

spec 化共享契约拥有者：
- contracts

参与拥有者：
- billing-service
- web-client
- ios-client
```

### 为什么这很重要

没有这个，"共享所有权"就会变得模糊，团队不知道他们读的是：

- 发起人拥有的计划
- 一个 spec 化契约
- 还是另一个团队的本地解释

---

## 旅程 7：仅部分 repository 被克隆时的多 repository planning

### 起始状态

用户希望 planning 影响以下内容的工作：

- contracts
- billing-service
- web-client
- ios-client

但本地只有这些：

- contracts
- web-client

### 预期行为

OpenSpec 仍应允许 planning。

它创建协调 workspace 并记录：

- `contracts` 和 `web-client` 的已解析根
- `billing-service` 和 `ios-client` 的未解析状态

提示感觉：

```text
本地已解析：
- contracts
- web-client

当前本地不可用：
- billing-service
- ios-client

planning 可以在部分上下文的情况下继续进行。
未解析根中的实现将保持待处理，直到被链接。
```

### Agent 行为

Agent 应：

- 使用已解析的 repository 进行具体 planning
- 明确提及未解析的 repository
- 避免假装读取了它们的 spec
- 如果需要，在行动倡议跟踪中生成待处理占位符

### 存储结果

协调 workspace 可能包含未解析的链接，例如：

```yaml
projects:
 - id: github.com/Fission-AI/contracts
 path: /Users/me/work/contracts
 status: resolved
 - id: github.com/Fission-AI/billing-service
 status: unresolved
 - id: github.com/Fission-AI/web-client
 path: /Users/me/work/web-client
 status: resolved
 - id: github.com/Fission-AI/ios-client
 status: unresolved
```

### 为什么这很重要

这使 planning 在环境不完整时仍然有用。

在这里阻塞 planning 会使功能变得脆弱。

这对大型团队也很重要，因为并非每个团队成员都会克隆或拥有每个参与 repository 的访问权限。

---

## 旅程 8：planning 期间如何读取 spec

这是最重要的行为规则之一。

OpenSpec 永远不应盲目地从所有根读取所有 spec。

### 单 repository

读取：

- 本地项目配置
- 与选定范围相关的本地 spec
- 仅在有用时读取本地变更历史

不读取：

- 默认情况下不相关的本地 spec

### Monorepo

读取：

- 根项目配置
- 选定范围的 spec
- 如果选定或引用，读取共享契约 spec

不读取：

- 不相关的应用/服务/包

### 多 repository

读取：

- 来自协调 workspace 的行动倡议元数据
- 已解析的附加根中的 spec
- 仅那些根中选定的范围
- 如果用户或 agent 明确选择打开，读取信息性引用

不读取：

- 来自未解析根的 spec
- 每个 repository 中的每个 spec
- 如果那会爆炸上下文，则不自动读取引用的 spec

### 信息性引用

引用应显示如下：

```text
相关引用：
- github.com/Fission-AI/contracts: openspec/specs/checkout/spec.md
- github.com/Fission-AI/web-client: openspec/specs/checkout/web/spec.md
```

Agent 可以将它们用作导航提示。

它们不是验证阻塞项。

### 共享契约读取顺序

当选定的变更涉及共享契约时，OpenSpec 应优先使用此读取顺序：

1. 行动倡议元数据（如果存在）
2. spec 化共享契约
3. 选定的消费者/本地 spec
4. repository 本地变更产物

这很重要，因为共享契约定义了边界级别的真理，而本地 spec 描述了每个消费者如何满足它们。

---

## 旅程 9：产物如何存储

这必须保持简单和确定性。

### 规则 1：spec 化 spec 与拥有者共存

示例：

- Checkout 契约 spec 位于 `contracts`
- Web checkout 行为位于 `web-client`
- iOS 行为位于 `ios-client`

### 规则 2：repository 本地变更与 repository 拥有者共存

示例：

- `contracts/openspec/changes/add-3ds-contract/`
- `web-client/openspec/changes/add-3ds-web/`

这些变更是每个拥有 repository 的执行产物。它们应携带 repository 特定的任务、差异 spec 和本地实现状态。

### 规则 3：行动倡议级 planning 存在于协调 workspace 中

示例：

- proposal.md
- design.md
- 行动倡议摘要
- 发布排序
- 跨 repository 假设
- 所有权、里程碑、风险和依赖项
- repository 本地变更之间的链接

### 规则 4：workspace 永不会成为 spec 化 spec 存储

协调 workspace 可以引用 spec 并总结它们。

它不应成为第二个 spec 事实来源。

### 规则 5：共享契约仅在所有权明确后才成为 spec 化

如果跨边界行为尚未分配 spec 化拥有者，OpenSpec 应将其存储为行动倡议级别的草稿材料，而不是假装它已经是 spec 化 spec。

### 规则 6：共享协调 workspace 存储稳定的协作数据，而非本地机器状态

如果协调 workspace 被提交供团队使用，它应包含：

- 稳定的项目 ID
- 链接的变更
- 所有权和行动倡议元数据

它不应包含：

- `/Users/...` 路径
- `C:\\...` 路径
- 特定机器的附加根状态

该信息属于本地覆盖数据。

---

## 旅程 10：跨根工作中的 `/opsx:apply`

实现用户体验必须对工具限制保持诚实。

### 情况 A：Agent 可以跨根工作

用户在协调 workspace 中。

他们运行：

```text
/opsx:apply
```

OpenSpec 响应：

```text
此行动倡议在以下位置有链接的变更：
- contracts
- billing-service
- web-client
- ios-client

选择应用 schema：
- 应用一个链接的变更
- 按建议顺序应用
```

推荐的默认值：

- 一次应用一个链接的变更

这使任务状态和实现上下文保持可管理。

### 情况 B：Agent 实际上是单根的

用户在协调 workspace 中并运行：

```text
/opsx:apply
```

OpenSpec 应该说：

```text
此行动倡议跨越多个 repository。
在您当前的工具中，实现必须按 repository 运行。

建议的下一步：
- 打开 /Users/me/work/contracts 并运行 /opsx:apply add-3ds-contract
```

### 为什么这很重要

跨 repository planning 和跨 repository 实现不是同一种能力。

用户体验不能假设所有 agent 都能同时做好两者。

---

## 旅程 10A：在 Monorepo 中创建共享契约

### 起始状态

用户在一个具有以下结构的 monorepo 中：

```text
platform/
 openspec/
 apps/web/
 apps/ios/
 apps/android/
 services/billing/
```

没有现有的 spec 化 `checkout` 共享契约。

### 用户请求

用户输入：

```text
/opsx:propose add-3ds-checkout
```

Agent 发现请求跨越：

- web
- iOS
- Android
- 计费后端

### 预期提示

```text
这看起来像是跨多个范围共享的跨边界行为。

OpenSpec 应将其视为：
- 一个共享契约
- 独立的本地变更
- 暂时作为行动倡议笔记
```

用户选择共享契约。

然后 OpenSpec 询问：

```text
spec 化共享契约应该放在哪里？
- openspec/specs/contracts/checkout
- openspec/specs/shared/checkout
- 暂时保持为仅行动倡议
```

### 预期的存储结果

OpenSpec 创建：

- 选定共享范围中的 spec 化共享契约
- monorepo 根下的 repository 本地变更
- 根据需要为选定的消费者范围创建本地差异 spec

### 为什么这很重要

这保持了跨边界行为的单一事实来源，而不是将相同逻辑分散到 web、iOS、Android 和后端 spec 中。

---

## 旅程 10B：在多 repository 环境中创建共享契约

### 起始状态

用户正在 planning 一个涉及以下内容的 checkout 行动倡议：

- `contracts`
- `web-client`
- `ios-client`
- `android-client`
- `billing-service`

没有现有的共享 checkout 契约。

### planning 流程

用户创建或进入一个协调 workspace。

他们运行：

```text
/opsx:propose add-3ds
```

OpenSpec 检测到这可能需要一个共享契约。

### 预期提示

```text
未找到此行为的 spec 化共享契约拥有者。

选择如何进行：
- 在现有契约 repository 中创建 spec 化契约
- 将契约分配给现有域拥有者 repository
- 暂时保持为仅行动倡议
```

如果用户选择现有契约 repository，OpenSpec：

1. 在该 repository 中为共享契约创建一个 repository 本地变更
2. 将消费者 repository 变更链接到它
3. 记录从消费者到 spec 化契约的引用

如果用户保持为仅行动倡议，OpenSpec：

1. 将草稿跨边界行为存储在行动倡议笔记中
2. 将其标记为非 spec 化
3. 警告长期消费者行为不应依赖于此，直到它被提升为拥有的共享契约

### 为什么这很重要

这避免了不良默认情况，即启动变更的应用团队意外成为跨组织契约的长期拥有者。

---

## 旅程 11：archive 跨根工作

### 单 repository 或简单 Monorepo

与今天相同：

```text
/opsx:archive
```

### 多 repository 行动倡议

用户在协调 workspace 中运行：

```text
/opsx:archive
```

OpenSpec 检查链接的 repository 变更：

- 已 archive
- 准备 archive
- 仍然活跃
- 未解析

提示感觉：

```text
行动倡议：add-3ds

链接变更状态：
- contracts/add-3ds-contract：已完成
- billing-service/add-3ds-billing：已完成
- web-client/add-3ds-web：活跃中
- ios-client/add-3ds-ios：未解析

archive 选项：
- 仅 archive 已完成的链接变更
- 将行动倡议标记为部分完成
- 等待所有链接变更完成
```

### 推荐行为

允许部分完成状态。

跨 repository 工作通常是异步完成的。

---

## 设置旅程

设置路径需要感觉轻量。

## 旅程 12：单 repository 用户的首次设置

### 步骤

1. `cd repo`
2. `openspec init`
3. 在 repository 中打开 agent
4. 运行 `/opsx:propose`

不展示 workspace 概念。

---

## 旅程 13：Monorepo 团队的首次设置

### 步骤

1. `cd monorepo`
2. `openspec init`
3. 可选地为主要拥有领域添加范围标记
4. 运行 `openspec update`
5. 在 monorepo 根中打开 agent

在 planning 期间，OpenSpec 在需要时询问范围选择。

不需要单独的 workspace 管理步骤。

---

## 旅程 14：多 repository 团队的首次设置

### 步骤

1. 每个 repository 独立运行 `openspec init`
2. 只有当跨 repository 工作出现时，用户才创建协调 workspace
3. 根据需要将 repository ID 链接到本地克隆
4. 用户打开 agent 在协调 workspace 中进行 planning

这很重要：

系统不应要求平台团队在所有真实工作开始之前预先注册每个 repository。

---

## Agent 指令要求

当 OpenSpec 创建协调 workspace 时，它应生成面向 agent 的文件。

最低内容：

1. 行动倡议摘要
2. 选定的范围
3. 拥有根和已解析路径
4. 未解析的根
5. 存储规则
6. 如果已知，当前工具的实现限制

### 示例 `claude.md`

```md
您正在处理行动倡议 `add-3ds`。

已解析的根：
- /Users/me/work/contracts
- /Users/me/work/web-client

未解析的根：
- github.com/Fission-AI/billing-service
- github.com/Fission-AI/ios-client

所有权：
- contracts 拥有共享 checkout 契约
- web-client 拥有 web checkout 行为

规则：
- spec 化 spec 必须在拥有根中编辑
- 行动倡议级别的笔记存放在此协调 workspace 中
- 跨 repository 引用仅为信息性
```

此文件应为任何受益于确定性启动上下文的受支持 agent 集成生成。

---

## 场景总结

### 快乐路径

1. 单 repository，一个变更
2. Monorepo，一个范围
3. Monorepo，多个范围
4. 大型 Monorepo，协调型行动倡议
5. 多 repository，所有根本地可用
6. 多 repository，部分本地可用

### 重要转换

1. 单 repository 请求升级为多 repository
2. Monorepo 请求升级为协调型 planning
3. planning workspace 移交给 repository 本地实现
4. archive 时的部分跨 repository 完成
5. 仅行动倡议的共享行为被提升为 spec 化共享契约

---

## 边缘情况

### 1. 用户在"错误"的 repository 中开始

示例：

- 用户在 `web-client` 中开始
- 工作实际上跨越 `contracts`、`web-client`、`ios-client`

预期行为：

- OpenSpec 建议创建协调 workspace
- 它不会将整个行动倡议埋在 `web-client` 内部

### 2. 用户希望行动倡议存储在其他地方

预期行为：

- 允许明确的路径选择
- 如果有用，记住最近的 workspace 位置

### 3. 两个本地克隆匹配同一个 repository 标识符

预期行为：

- 提示用户选择一个
- 可选地在本地保存首选映射

### 4. repository 标识符无法解析

预期行为：

- 存储为未解析
- 允许 planning 继续进行
- 仅对该根阻止实现

### 5. Monorepo 没有明确的范围元数据

预期行为：

- 从结构和 spec 推断可能的范围
- 让用户确认
- 提供稍后保存选择模型的选项

### 6. 范围选择过于宽泛

预期行为：

- 警告用户许多范围将被拉入 planning
- 建议缩小范围

### 7. 共享契约所有权不明确

预期行为：

- 需要一个 spec 化拥有者
- 其他范围/repository 可以引用它，而不是隐式共同拥有它

### 7A. 没有有意义的现有共享拥有者

预期行为：

- 让团队暂时将该行为保持为仅行动倡议
- 明确标记为草稿和非 spec 化
- 如果它开始表现得像长期契约，稍后提示升级

### 8. Agent 无法真正跨根工作

预期行为：

- 仅使用协调 workspace 进行 planning
- 引导用户进行逐个根的应用流程

### 9. workspace 变得过时

示例：

- repository 在磁盘上移动了
- repository 重命名了
- 远程 URL 变了

预期行为：

- `openspec workspace doctor` 或等效命令重新链接根
- 行动倡议元数据保持稳定，因为标识符是持久的，路径不是

### 10. 一个 repository 被 archive 或有意延迟

预期行为：

- 行动倡议可以保持部分完成
- 并非每个链接的根必须同时完成

### 11. 用户不希望在大型 monorepo 中进行管理员管理的设置

预期行为：

- 范围发现应该是本地和 delta 式的
- 设置不应需要中心团队先定义所有内容

### 12. 用户只想要一次临时的多 repository 工作

预期行为：

- 允许一次性的协调 workspace
- 不强制进行长期 workspace 管理

### 13. 团队希望共享一个协调 workspace

预期行为：

- 支持已提交的共享协调 repository 或 workspace
- 保持特定机器的解析数据本地化
- 让每个团队成员独立解析项目 ID

### 14. 跨团队行动倡议需要不同的所有权角色

预期行为：

- 区分行动倡议发起人和 spec 化共享契约拥有者
- 在 workspace 元数据和 agent 指令中使两者可见

---

## 此用户体验含义的产品决策

如果 OpenSpec 采用这些旅程，会随之产生几个设计结论。

### 1. 多 repository planning 需要一个第一类协调 workspace

没有这个，OpenSpec 无法真实回答用户应该站在哪里，或者跨 repository 行动倡议应该驻留在哪里。

### 2. repository 本地变更和 spec 化 spec 应留在拥有者处

没有这个，OpenSpec 会创建重复或误导的事实来源。

### 3. 大型 Monorepo 不能总是被视为简单的单根

OpenSpec 必须同时支持：

- 单根 monorepo 变更
- 协调型 monorepo 行动倡议

### 4. 发现和解析是不同的系统

OpenSpec 必须分开处理：

- 识别范围
- 为持久的项目标识符解析本地路径

### 5. Agent 启动上下文需要显式生成

跨根 planning 只有在此情况下才能可靠工作：OpenSpec 为 agent 写入确定性的 workspace 上下文。

### 6. v1 中引用应保持信息性

如果 OpenSpec 默认验证跨根引用，它实际上已经发布了一个依赖图系统。

那应该是一个后来的、可选的能力。

### 7. 共享契约创建需要引导式的所有权流程

没有这个，团队要么：

- 在 repository 间复制共享行为
- 意外分配所有权
- 或者完全避免创建跨边界 spec

OpenSpec 应帮助用户在以下选项中选择：

- 现有的共享拥有者
- 现有的域拥有者
- 新的共享契约范围
- 仅行动倡议草稿 schema

### 8. 共享协调需要两层存储模型

为了干净地支持团队和组织，OpenSpec 应区分：

- 已提交的共享行动倡议元数据
- 本地特定机器的路径解析

没有这种分离，用户体验要么：

- 无法扩展到单个用户之外，要么
- 将特定机器的状态泄漏到共享产物中

---

## 开放问题

这些旅程有意保留一些实现选择开放。

1. 协调 workspace 应始终在磁盘上对用户可见，还是可以可选地位于全局 OpenSpec 数据目录中？
2. Monorepo 协调型行动倡议应重用与多 repository 相同的 workspace 概念，还是使用更轻量的 repository 内变体？
3. OpenSpec 应支持嵌套的 `openspec/` 根，还是保持一个根并单独建模范围？
4. 表示选定范围和链接变更所需的最小元数据是什么？
5. 已提交的共享 workspace 状态和本地覆盖状态之间的确切格式划分是什么？
6. 哪些 agent 应接收生成的 workspace 指令，以什么格式？
7. 什么确切的 CLI 表面应创建和管理协调 workspace？

---

## 推荐的下一步

将这些旅程转化为具体的设计 proposal，涵盖：

1. 协调 workspace 文件格式
2. 范围元数据形状
3. repository 标识符和本地解析模型
4. 链接变更模型
5. 共享清单 vs 本地覆盖模型
6. 用于创建、附加、诊断、同步和 archive 流程的 CLI 命令
7. 为受支持的工具生成 agent 指令
