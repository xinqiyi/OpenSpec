# 工作区探索

## 背景

在简化技能安装的过程中，我们识别出更深层次的问题，关于配置文件、配置和工作区应如何协同工作。本文档记录了我们已决定的内容、仍开放的问题以及需要研究的内容。

**更新：** 初步探索揭示，"工作区"主要不是关于配置分层——而是一个更基础的问题：**当工作跨越多个模块或多个仓库时，规范和变更应该放在哪里？**

---

## 第 1 部分：配置文件与配置（原始范围）

### 我们已决定的内容

#### 配置文件用户体验（简化版）

**之前（原始提案）：**
```
openspec profile set core|extended
openspec profile install <workflow>
openspec profile uninstall <workflow>
openspec profile list
openspec profile show
openspec config set delivery skills|commands|both
openspec config get delivery
openspec config list
```
8 个子命令，两个概念（配置文件 + 配置）

**之后（简化版）：**
```
openspec config profile          # 交互式选择器（交付方式 + 工作流）
openspec config profile core     # 预设快捷方式
openspec config profile extended # 预设快捷方式
```
1 个命令带预设，一个概念

#### 交互式选择器

```
$ openspec config profile

交付方式：[skills] [commands] [both]
                              ^^^^^^

工作流：（空格切换，回车保存）
[x] propose
[x] explore
[x] apply
[x] archive
[ ] new
[ ] ff
[ ] continue
[ ] verify
[ ] sync
[ ] bulk-archive
[ ] on-board
```

一个地方同时配置交付方式和工作流选择。

#### 为什么是"配置文件"（而非"工作流"）

配置文件作为抽象允许未来的可扩展性：
- 方法论捆绑（规范驱动、测试驱动）
- 用户创建的配置文件
- 可共享的配置文件
- 不同方法的不同技能/命令集

### 配置分层研究

我们研究了类似工具如何处理配置分层：

| 工具 | 模型 | 关键模式 |
|------|------|----------|
| **VSCode** | 用户 → 工作区 → 文件夹 | 对象合并，原语覆盖。工作区 = 仓库中已提交的 `.vscode/` |
| **ESLint（flat）** | 单根配置 | *有意取消了级联* - "复杂性呈指数级增长" |
| **Turborepo** | 根 + 包扩展 | 每个包的 `turbo.json` 带有 `extends: ["//"]` 用于覆盖 |
| **Nx** | 集成模式 vs 基于包 | 两种模式 - 共享根或每个包。从集成模式迁移困难。 |
| **pnpm** | 工作区文件定义包范围 | 包集根部的 `pnpm-workspace.yaml`。依赖可以共享或每个包独立 |
| **Claude Code** | 全局 + 项目 | `~/.claude/` 用于全局，`.claude/` 每个项目。无工作区跟踪。 |
| **Kiro** | 分布式每个根 | 每个文件夹有 `.kiro/`。聚合展示，无继承。 |

**ESLint 的关键洞察：** ESLint 团队在 flat 配置中明确移除了级联，因为级联是一个复杂性的噩梦。他们的新模型：根目录一个配置，使用 glob 模式定位子目录。

**配置文件/配置的建议：** 两层就够了。
- **全局** = 用户的默认设置（`~/.config/openspec/`）
- **项目** = 仓库级别的配置（`.openspec/` 或提交到仓库）

配置不需要"工作区"层。这与 Claude Code 的模型一致。

### 配置决策（针对本次变更）

保持简单：
1. 全局配置文件作为 `openspec init` 的默认值
2. `openspec init` 将当前配置文件应用于项目
3. 尚无工作区跟踪
4. 无现有项目的自动同步

这是明确的，且不妨碍未来功能。

---

## 第 2 部分：更深层次的问题（规范与变更组织）

### 真正的问题

工作区问题不是关于配置——而是关于**规范和变更存放在哪里**，当：

1. **Monorepo**：一个规范或变更可能跨越多个包/应用
2. **多仓库**：一个变更可能完全跨越多个仓库
3. **跨职能工作**：一个功能影响多个团队（后端、Web、iOS、Android）

### 当前 OpenSpec 架构

OpenSpec 目前假定：
- 每个仓库一个 `openspec/`，始终在根目录
- CLI 不向上查找目录——期望你已在根目录
- 变更可以涉及任何规范（无范围限制）
- 单个配置适用于所有内容
- 项目中无"范围"或"边界"概念

```
openspec/
├── specs/
│   ├── auth/spec.md           # 按域组织的规范
│   ├── payments/spec.md
│   └── checkout/spec.md
├── changes/
│   └── add-oauth/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/             # 差异规范（可以涉及多个）
│           ├── auth/spec.md
│           └── checkout/spec.md
└── config.yaml
```

**这对单项目仓库运行良好。** 但是遇到以下情况呢：
- 有 50+ 个包的大型 monorepo？
- 多仓库微服务？
- 跨越多个团队的跨职能功能？

### Checkout/支付示例

想象一个支付系统，具有：
- **后端计费团队**：拥有支付处理
- **Web 团队**：拥有 Web checkout 用户体验
- **iOS 团队**：拥有 iOS checkout 用户体验
- **Android 团队**：拥有 Android checkout 用户体验
- **跨领域**：所有客户端必须遵循的支付*契约*

**问题：**
- 共享支付契约规范放在哪里？
- 平台特定的 checkout 规范放在哪里？
- 如果 iOS 规范"扩展"了共享契约，如何表达？
- 当契约变化时，下游规范如何更新？
- 谁拥有什么？

### 核心张力

```
                    范围
                      │
         窄            │            宽
    （团队/模块）      │       （跨领域）
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    │  "我们团队的   │   "共享         │
    │   checkout     │    checkout     │
    │   行为"        │    契约"        │
    │                 │                 │
────┼─────────────────┼─────────────────┼──── 所有权
    │                 │                 │
    │  容易：         │  困难：         │
    │  一个团队，     │  多个利益       │
    │  一个规范       │  相关方         │
    │                 │                 │
    └─────────────────┴─────────────────┘
```

---

## 第 3 部分：其他领域如何解决这个问题

### 研究中的模式

| 领域 | 共享内容 | 特定内容 | 它们如何连接 |
|--------|-------------|----------------|------------------|
| **Protobuf** | 根目录的 `common/` | 每个服务的 `domain/service/` | 从 common 导入 |
| **设计系统** | 设计令牌、组件名称、API | 平台实现 | "相同属性，不同渲染" |
| **DDD** | 共享内核 | 有界上下文 | 上下文映射定义关系 |
| **RFC** | 跨领域 RFC | 团队范围的 RFC | 不同的审查流程 |
| **OpenAPI** | 基础模式 | 每个服务规范 | `$ref` 引用共享定义 |

### Protobuf Monorepo 模式

```
proto/
├── common/              # 共享、低变动类型
│   └── money.proto
│   └── address.proto
├── billing/             # 领域特定
│   └── service.proto
└── checkout/
    └── service.proto    # 从 common/ 导入
```

**关键洞察：** "大多数工程组织应将其 proto 文件保存在一个仓库中。心智开销保持恒定，而不是随组织规模增长。"

### 设计系统模式（Booking.com、Uber）

> "组件在 iOS 和 Android 之间看起来可能相当不同，因为它们使用原生应用设计标准，但仍然是代码中**完全相同的属性**。这就是使属性如此强大的原因——它是每个组件的**单一事实来源**。"

**关键洞察：** 共享规范定义*契约*（属性、行为）。平台规范定义*实现细节*（在该平台上如何呈现/工作）。

### DDD 有界上下文

> "一个上下文，一个团队。清晰的所有权避免误解。"

**关键洞察：** 规范应有清晰的所有权。跨领域关注点使用"共享内核"模式——需要协调才能变更的显式共享代码/规范。

---

## 第 4 部分：OpenSpec 的三种模型

### 模型 A：扁平根（当前）

```
openspec/
├── specs/
│   ├── checkout-contract/    # 共享契约
│   ├── checkout-web/         # Web 特定
│   ├── checkout-ios/         # iOS 特定
│   ├── checkout-android/     # Android 特定
│   ├── billing/              # 后端
│   └── ...（根级别 50+ 个规范）
└── changes/
```

**优点：**
- 简单的心智模型
- 所有规范在一个地方
- 无嵌套复杂性

**缺点：**
- 规模大时变得笨重（50+ 个目录）
- 无清晰的所有权信号
- 难以看出哪些规范相关
- 命名约定变得关键（`checkout-*`）

### 模型 B：嵌套规范（域 → 平台）

```
openspec/
├── specs/
│   ├── checkout/
│   │   ├── spec.md              # 共享契约（"接口"）
│   │   ├── web/spec.md          # Web 实现规范
│   │   ├── ios/spec.md          # iOS 实现规范
│   │   └── android/spec.md      # Android 实现规范
│   └── billing/
│       └── spec.md
└── changes/
```

**优点：**
- 清晰层级（共享在顶层，特定嵌套）
- 相关规范放在一起
- 视觉上更好地扩展
- 所有权可以遵循结构

**缺点：**
- 更复杂的规范引用（`checkout/web` vs `checkout`）
- 需要定义继承/扩展语义
- iOS 规范是"扩展"了基础规范，还是仅仅引用它？

**开放问题：** "扩展"是什么意思？
```yaml
# checkout/ios/spec.md
extends: ../spec.md   # 继承所有需求？
requirements:
  - System SHALL support Apple Pay  # 添加到基础？
```

### 模型 C：分布式规范（靠近代码）

```
monorepo/
├── services/
│   └── billing/
│       └── openspec/specs/billing/spec.md
├── clients/
│   ├── web/
│   │   └── openspec/specs/checkout/spec.md
│   ├── ios/
│   │   └── openspec/specs/checkout/spec.md
│   └── android/
│       └── openspec/specs/checkout/spec.md
└── openspec/           # 根级别用于跨领域
    ├── specs/
    │   └── checkout-contract/spec.md   # 共享契约
    └── changes/        # 跨领域变更放在哪里？
```

**优点：**
- 规范靠近它们描述的代码
- 团队自然拥有自己的规范
- 也适用于多仓库（每个仓库有自己的 `openspec/`）

**缺点：**
- 跨领域规范尴尬（它们去哪里？）
- 跨越多个 `openspec/` 目录的变更 = ???
- 需要"工作区"概念来聚合
- 需要管理多个 `openspec/` 根

### 模型 D：混合（每个项目内模型 B + 项目间模型 C）

每个项目使用一个 `openspec/` 根，但允许在该根内嵌套规范以实现清晰的所有权和共享契约。
对于多仓库工作，使用工作区清单协调多个项目，而不复制规范化规范。

**Monorepo 形态（单个项目，嵌套规范）：**
```
repo/
└── openspec/
    ├── specs/
    │   ├── contracts/
    │   │   └── checkout/spec.md
    │   ├── billing/
    │   │   └── spec.md
    │   └── checkout/
    │       ├── web/spec.md
    │       ├── ios/spec.md
    │       └── android/spec.md
    └── changes/
        └── add-3ds/
            ├── proposal.md
            ├── design.md
            ├── tasks.md
            └── specs/
                ├── contracts/checkout/spec.md
                ├── billing/spec.md
                ├── checkout/web/spec.md
                ├── checkout/ios/spec.md
                └── checkout/android/spec.md
```

**多仓库形态（多个项目 + 工作区协调）：**
```
~/work/
├── contracts/
│   └── openspec/
│       ├── specs/checkout/spec.md
│       └── changes/add-3ds-contract/
├── billing-service/
│   └── openspec/
│       ├── specs/billing/spec.md
│       └── changes/add-3ds-billing/
├── web-client/
│   └── openspec/
│       ├── specs/checkout/spec.md
│       └── changes/add-3ds-web/
├── ios-client/
│   └── openspec/
│       ├── specs/checkout/spec.md
│       └── changes/add-3ds-ios/
└── payments-workspace/
    └── .openspec-workspace/
        ├── workspace.yaml
        └── initiatives/add-3ds/links.yaml
```

`workspace.yaml` 列出项目/根。`links.yaml` 将一个跨领域行动倡议映射到每个项目的变更。
规范化规范保留在拥有仓库中；工作区数据仅为协调元数据。

**优点：**
- 清晰的所有权边界（一个项目拥有自己的规范和变更）
- 共享契约可以有专门的拥有者仓库（不作为事实来源的复制）
- 用一个心智模型适用于 monorepo 和多仓库
- 避免继承复杂性（关系可以作为显式引用开始）
- 从当前模型逐步迁移的路径

**缺点：**
- 需要新的工作区用户体验用于跨仓库协调
- 跨仓库功能工作创建多个变更 ID 需要管理
- 需要契约所有权和行动倡议链接的约定
- 一些用户可能期望一个全局的"超级变更"而不是链接的每个项目变更
- 工具必须支持主规范和变更差异中的嵌套规范路径

---

## 第 5 部分：多仓库考虑因素

对于多仓库设置，模型 C（或模型 D 的协调部分）几乎是不可避免的：

```
~/work/
├── billing-service/
│   └── openspec/specs/billing/
├── web-client/
│   └── openspec/specs/checkout/
├── ios-client/
│   └── openspec/specs/checkout/
└── contracts/                    # 用于共享规范的专用仓库？
    └── openspec/specs/
        └── checkout-contract/
```

### 多仓库的问题

1. **共享规范放在哪里？**
   - 专用的"contracts"仓库？
   - 在每个仓库中复制（漂移风险）？
   - 一个仓库是"事实来源"，其他引用它？

2. **跨仓库变更放在哪里？**
   - 在其中一个仓库中？（感觉不对——所有权有偏）
   - 在一个单独的"工作区"仓库中？
   - 在 `~/.config/openspec/workspaces/my-platform/changes/` 中？

3. **变更如何传播？**
   - 对 `checkout-contract` 的变更影响所有客户端仓库
   - 我们需要显式的依赖跟踪吗？
   - 还是这是"带外"的（团队手动协调）？

### "工作区"对多仓库可能意味着什么

如果我们添加工作区支持，它可以是：

> **工作区是可以一起操作的 OpenSpec 根的集合。**

```yaml
# ~/.config/openspec/workspaces.yaml（或类似）
workspaces:
  my-platform:
    roots:
      - ~/work/billing-service
      - ~/work/web-client
      - ~/work/ios-client
      - ~/work/contracts
    shared_context: |
      All services use TypeScript.
      API contracts follow OpenAPI 3.1.
```

这将支持：
1. **跨仓库变更**：创建跟踪跨多个根的差异的变更
2. **聚合规范视图**：查看跨工作区的所有规范
3. **共享上下文**：适用于所有根的上下文/规则

---

## 第 6 部分：关键设计问题

### 1. 规范应该是层级化的吗（带继承）？

**方案 A：无继承，纯组织**
- 嵌套目录纯粹是组织性的
- 每个规范独立
- 关系是隐式的（命名）或手动记录的

**方案 B：显式继承**
```yaml
# checkout/ios/spec.md
extends: ../spec.md
requirements:
  - System SHALL support Apple Pay  # 添加到基础
```
- 子规范继承父需求
- 可以添加、覆盖或扩展
- 更强大但也更复杂

**方案 C：无继承的引用**
```yaml
# checkout/ios/spec.md
references:
  - ../spec.md  # "参见"但无继承
requirements:
  - System SHALL implement checkout per checkout-contract
  - System SHALL support Apple Pay
```
- 显式引用用于文档
- 无自动继承
- 更简单的语义

### 2. "共享内核"放在哪里？

**方案 A：根级别（模型 B）**
- `openspec/specs/checkout/spec.md` 是共享内核
- 平台规范嵌套在其下

**方案 B：专用区域**
- `openspec/specs/_shared/checkout-contract/spec.md`
- 或 `openspec/specs/_contracts/checkout/spec.md`
- 显式的"共享"命名空间

**方案 C：单独的仓库（适用于多仓库的模型 C）**
- 一个专用的 `contracts` 或 `specs` 仓库
- 其他仓库引用它

### 3. "工作区" vs "项目"是什么？

如果我们引入工作区：

| 概念 | 定义 |
|---------|------------|
| **项目** | 单个 OpenSpec 根（一个 `openspec/` 目录） |
| **工作区** | 可以一起操作的项目集合 |

工作区将支持：
- 跨项目聚合规范查看
- 跨项目变更
- 跨项目共享上下文

**问题：** 我们需要显式的工作区跟踪，还是只需要临时的多根（如 Claude Code 的 `/add-dir`）？

### 4. OpenSpec 需要理解依赖关系吗？

如果 `checkout-web` 依赖于 `checkout-contract`：
- OpenSpec 应该知道这种关系吗？
- 对 `checkout-contract` 的变更应警告下游规范吗？
- 还是依赖跟踪"超出范围"？

**权衡：**
- 有依赖跟踪：更强大，自动传播警告
- 无依赖跟踪：更简单，团队自己管理依赖

### 5. 对于跨领域工作，变更应如何工作？

**对于 monorepo（模型 B）：**
- 一个变更，`specs/` 中的多个差异规范
- 今天已经有效

**对于多仓库（模型 C）：**
- 方案 A：引用多个仓库变更的一个"工作区变更"
- 方案 B：每个仓库中引用其他变更的独立变更
- 方案 C：变更始终在一个仓库中，引用其他仓库中的规范

---

## 第 7 部分："出色"是什么样的？

基于研究，团队喜欢：

1. **一个查看的地方**（Protobuf："心智开销保持恒定"）
2. **清晰的所有权**（DDD："一个上下文，一个团队"）
3. **带本地扩展的共享契约**（设计系统："相同属性，不同渲染"）
4. **自动一致性**（设计系统："设计令牌作为基础"）
5. **低认知负荷**（不应过多考虑组织方式）

### 可能的北极星

**雄心勃勃：**
> OpenSpec 自动理解你的仓库结构，检测跨领域规范，并帮助你创建流向正确位置的变更。

**更简单：**
> 你按你想要的方式组织规范。OpenSpec 就是能工作。

**实用：**
> 嵌套规范用于组织。显式依赖用于跨领域。没有魔法。

---

## 第 8 部分：可能的推进路径

### 针对本次变更（simplify-skill-installation）

现在不解决规范组织问题。将范围保持为：
1. 配置文件用户体验简化
2. `openspec init` 改进
3. 尚无工作区跟踪

### 未来：规范组织变更

一个单独的变更来探索和实现：

1. **决定模型 A、B、C 或 D（混合）**
2. **决定继承语义**（或无）
3. **更新规范解析**以处理嵌套
4. **更新变更差异**以处理嵌套规范

### 未来：多仓库 / 工作区变更

如果需要，一个单独的变更用于：

1. **定义工作区概念**
2. **实现工作区跟踪**（或临时多根）
3. **跨仓库变更**
4. **跨仓库共享上下文**

---

## 第 9 部分：规范哲学（行为优先、轻量级、与 Agent 对齐）

### OpenSpec 中的规范是什么？

对于 OpenSpec，规范应被视为边界上的**可验证行为契约**：
- 用户、集成者或操作者可以观察和依赖的内容
- 可以通过测试、检查或显式审查验证的内容
- 即使内部实现发生变化也应保持稳定的内容

### 规范中应包含和不应包含的内容

**应包括：**
- 可观察的行为和结果
- 接口/数据契约（输入、输出、错误条件）
- 对外部重要的非功能约束（隐私、安全、可靠性）
- 下游消费者依赖的兼容性保证

**应避免：**
- 内部实现细节（类名、库选择、控制流）
- 可以在不影响行为的情况下更改的工具机制
- 逐步执行计划（属于任务/设计）

### 保持严谨度与风险成比例（避免官僚主义）

使用渐进式严谨：

1. **轻量规范（大多数变更的默认值）**
   - 简短的行为要点、清晰的范围和验收检查
2. **完整规范（仅适用于高风险或跨边界工作）**
   - 针对 API 破坏、迁移、安全/隐私或跨团队/仓库变更的更深入契约细节

这保持了日常使用的轻量性，同时在故障代价高昂的情况下保留了清晰度。

### 人类探索 -> Agent 编写的规范

OpenSpec 通常是由 agent 从人类探索编写。为了使其可靠：

- 人类提供意图、约束和探索中的示例
- Agent 将其转换为简洁、行为优先的需求和场景
- Agent 将实现细节保留在设计/任务中，而非规范中
- 验证检查强制执行结构和可测试性

简而言之：人类塑造意图；agent 生成一致、可验证的契约。

### 此哲学应在何处落地

为了避免在探索笔记中丢失，将其编纂在：
1. `docs/concepts.md` 用于面向人类的框架
2. `openspec/specs/openspec-conventions/spec.md` 用于规范性规范约定
3. `openspec/specs/docs-agent-instructions/spec.md` 用于 agent 指令编写规则

---

## 第 10 部分：设计决策（2026 年 4 月）

根据真实的多仓库用例评估上述模型后（参见 [#725](https://github.com/Fission-AI/OpenSpec/issues/725)），我们收敛到以下设计方向。

### 核心洞察

工作区本身不是持久的东西。对于大型团队，持久的规划对象是**行动倡议或计划**，而仓库本地规范和变更仍然是每个仓库拥有的执行产物。参与某个功能的一组仓库通常是功能范围的，并随时间变化，因此一个必须在工作开始前配置的静态工作区清单会产生不符合团队实际工作方式的仪式。

### 决策：采用带惰性工作区的模型 D

选择第 4 部分的模型 D（混合），但使工作区清单**可选且惰性，而非先决条件**。

- **每个仓库保留自己的规范化 `openspec/`** —— 基础存储模型不变。
- **跨根工作可以通过协调工作区中的行动倡议进行协调** —— 这是当工作不再干净地局限于单个仓库时共享规划所在的地方。
- **"工作区"是对链接仓库和链接变更的派生或显式协调视图** —— 不是用户必须事先注册的东西。
- **仅在有人显式想要可重用的跨仓库捆绑时才持久化工作区清单** —— 这是一个选择加入的便利，而非要求。

### 决策：行动倡议优先的规划与链接的仓库本地变更

对于较大的多团队工作，以仓库为中心的规划是错误的初级抽象。团队和仓库是同一工作的多对多方面。OpenSpec 应将**行动倡议/计划**视为第一类规划对象，然后将仓库本地变更链接到它。

这尤其重要，因为当前的变更捆绑了：

- `proposal.md`
- `design.md`
- `tasks.md`
- 差异规范
- `.openspec.yaml`

这种捆绑形态对于仓库本地工作效果良好，但当一项工作跨越多个仓库或团队时就变得尴尬。在这种情况下，一个单一的仓库本地变更试图同时扮演两个角色：

- 共享规划对象
- 仓库特定的执行产物

这两者应该分开。

首选的模型是：

```text
coordination workspace /
  .openspec-workspace/
    workspace.yaml
    initiatives/
      add-3ds/
        initiative.yaml
        proposal.md
        design.md
        links.yaml

repo-A/
  openspec/
    changes/
      add-3ds-api/
        .openspec.yaml
        tasks.md
        specs/

repo-B/
  openspec/
    changes/
      add-3ds-web/
        .openspec.yaml
        tasks.md
        specs/
```

行动倡议持有共享规划层：

- 提议/意图
- 共享设计和权衡
- 参与团队
- 受影响的仓库
- 里程碑、风险和依赖项
- 指向仓库本地变更的链接

每个仓库本地变更为该仓库持有执行层：

- 仓库特定任务
- 差异规范
- 本地实现状态
- 可选的本地笔记（应随该仓库工作一起归档）

跨仓库链接仍然重要，但它应挂在行动倡议和仓库本地变更上：

```yaml
# billing-service/openspec/changes/add-3ds/.openspec.yaml
schema: spec-driven
created: 2026-04-12
initiative: add-3ds
links:
  - project: github.com/fission/web-client
    change: add-3ds-checkout
  - project: github.com/fission/ios-client
    change: add-3ds-checkout
```

每个仓库仍持有自己的变更及其自己的差异。跨仓库工作被表示为一个行动倡议加上 N 个链接的单仓库变更。这优于单一的超级变更，因为：
- 共享规划有一个真实的家
- 每个仓库的变更经历自己的归档周期
- 不需要在差异规范中解析跨仓库文件路径
- 团队可以以不同的速度推进（Web 在 iOS 之前发布）

对于小的单仓库工作，仓库本地变更作为计划和执行的捆绑可能仍然"足够好"。行动倡议优先的拆分在工作变得跨团队、跨模块、跨仓库或以其他方式需要大量协调时才重要。

### 决策：稳定的项目标识符，而非路径

跨仓库链接必须使用**稳定的项目标识符**，而不是文件系统路径。

- **规范化形式：** 标准化的 `host/org/repo` 元组（例如 `github.com/fission/web-client`）。
- **编写简写：** CLI 接受 `org/repo`（例如 `fission/web-client`）并从当前仓库的 remote 推断 host。
- **相对路径永远不是持久标识符。** 它们只能作为缓存的本地解析结果存在。

### 决策：离线优先的解析

CLI 使用离线优先的链将项目标识符解析为本地路径：

1. **显式路径** — 为当前运行传入的路径（例如 CLI 标志、临时多根）。
2. **本地 OpenSpec 仓库注册表** — `~/.config/openspec/` 或 `~/.local/share/openspec/` 中的持久映射（参见 `src/core/global-config.ts`）。
3. **父目录扫描** — 扫描已知父目录，查找其 remote 与目标标识符匹配的 git checkout。
4. **未解析** — 如果未找到本地路径，保持目标未解析并继续使用部分工作区。CLI 不得失败。

注册表是逐步填充的：当 CLI 发现克隆（通过扫描或用户提示），它会持久化该映射以供将来解析。注册表还存储"已知扫描根"（例如 `~/work/`），因此扫描会随时间改进，无需预先配置。

### 决策：仅信息性引用（v1）

规范级别的跨仓库引用是**仅文档的指针**：

```yaml
# web-client/openspec/specs/checkout/spec.md frontmatter
references:
  - project: github.com/fission/contracts-service
    spec: checkout-contract
```

- CLI **不会**因为引用的跨仓库规范缺失或未解析而验证失败。
- CLI **确实**在规划、查看或应用变更时将引用展示给人类和 agent。
- 更强的保证（例如，过时警告、跨仓库验证）是稍后通过 `lint`、`doctor` 或功能标志添加的选择加入层，而非基线行为。

这避免了在用例证明必要之前意外将 OpenSpec 提交到完整的依赖图系统。

### 决策：共享契约的显式拥有者仓库

当一个规范不能映射到单个实现仓库时（例如，共享 API 契约）：

- **一个仓库必须是显式拥有者。** 这可以是一个专用的"契约"仓库，或者是自然成为事实来源的仓库。
- **其他仓库引用拥有者仓库的规范**，通过信息性引用（见上文）。
- **没有默认的"纯规范仓库"模式。** 过于激进地将规范所有权与代码所有权分离会使 agent 执行变得尴尬并分散责任。

### Monorepo 与多仓库总结

| 关注点 | Monorepo | 多仓库 |
|---------|----------|------------|
| **规范组织** | 一个 `openspec/` 内的嵌套规范（模型 B） | 每个仓库有自己的 `openspec/` |
| **跨领域规范** | 嵌套在 `contracts/` 或 `shared/` 目录下 | 专用拥有者仓库，其他引用它 |
| **规划对象** | 简单工作可选行动倡议，大型跨团队工作有用 | 行动倡议是主要的协调对象 |
| **变更** | 一个或多个仓库本地变更可以实现一个行动倡议 | 链接的每个仓库变更实现一个行动倡议 |
| **关系** | 引用（v1 无继承） | 项目标识符链接，仅信息性 |
| **工作区** | 通常不需要，但可以为复杂工作托管行动倡议规划 | 协调工作区托管行动倡议规划；可选的清单供重用 |

### 实现路径

1. **定义行动倡议产物** — 为协调工作区中的共享规划添加行动倡议格式。
2. **扩展变更元数据** — 让仓库本地变更指向一个行动倡议和链接的兄弟变更。
3. **扩展规范元数据** — 为跨仓库规范指针添加 `references` 字段。
4. **构建项目解析** — 实现离线优先的解析链和本地注册表。
5. **构建行动倡议和链接视图** — 解析和显示行动倡议图加上链接的仓库本地变更的命令。
6. **支持临时多根** — "为此运行添加这些目录"或"从此行动倡议的链接派生根"。
7. **可选的工作区清单** — 仅在团队展示重用模式后添加保存的工作区。

嵌套规范（单个仓库内的模型 B）是干净 monorepo 支持的前提条件，应首先解决，如 #662 所述。

---

## 总结

| 问题 | 状态 | 备注 |
|----------|--------|-------|
| 配置文件用户体验 | 已决定 | `openspec config profile` 带预设 |
| 配置分层 | 已决定 | 两层：全局 + 项目（无工作区层） |
| 规范组织 | **方向已定** | 每个仓库嵌套规范，共享契约的显式拥有者仓库，跨仓库上下文的引用 |
| 规范哲学 | 方向已定 | 行为优先契约，渐进严谨，与 agent 对齐的编写 |
| 规范继承 | **已决定** | 仅引用，v1 无继承 |
| 行动倡议/规划模型 | **方向已定** | 较大工作的行动倡议优先规划，仓库本地变更作为执行产物 |
| 多仓库支持 | **方向已定** | 共享行动倡议下的链接每个仓库变更；工作区是协调，而非规范化执行存储 |
| 依赖跟踪 | **已决定** | v1 超出范围；引用仅为信息性 |
| 跨仓库解析 | **已决定** | 带本地注册表的离线优先解析链 |
| 共享契约 | **已决定** | 需要显式拥有者仓库；无默认的纯规范仓库模式 |

### 关键洞察

"工作区"问题实际上是两个独立的问题：
1. **配置/配置文件范围** → 通过全局 + 项目解决（不需要工作区）
2. **计划与执行组织** → 方向已定：行动倡议协调，仓库本地变更实现，工作区保持为协调层

这些应是具有独立探索的独立变更。

---

## 参考文献

- [VSCode Settings Precedence](https://code.visualstudio.com/docs/configure/settings)
- [ESLint Flat Config in Monorepos Discussion](https://github.com/eslint/eslint/discussions/16960)
- [Turborepo Package Configurations](https://turborepo.dev/docs/reference/package-configurations)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Claude Code Settings](https://code.claude.com/docs/en/settings)
- [Kiro Multi-Root Workspaces](https://kiro.dev/docs/editor/multi-root-workspaces/)
- [DDD Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
- [Protobuf Monorepo Patterns](https://www.lesswrong.com/posts/xts8dC3NeTHwqYgCG/keep-your-protos-in-one-repo)
- [Booking.com Multi-Platform Design System](https://booking.design/how-we-built-our-multi-platform-design-system-at-booking-com-d7b895399d40)
- [InnerSource RFC Patterns](https://patterns.innersourcecommons.org/p/transparent-cross-team-decision-making-using-rfcs)
