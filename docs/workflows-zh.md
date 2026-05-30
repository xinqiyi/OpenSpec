# 工作流

本指南介绍 OpenSpec 的常见工作流模式及其适用场景。有关基本设置，请参阅[快速入门](getting-started.md)。有关命令参考，请参阅[命令](commands.md)。

## 理念：行动，而非阶段

传统工作流强制你经历各个阶段：规划，然后实现，然后完成。但实际工作并非如此规整。

OPSX 采用不同的方法：

```text
传统方式（阶段锁定）：

  规划 ────────► 实现 ────────► 完成
      │                    │
      │   "不能回退"        │
      └────────────────────┘

OPSX（流动式行动）：

  proposal ──► specs ──► design ──► tasks ──► implement
```

**关键原则：**

- **行动，而非阶段** - 命令是你可以做的事情，而不是你被困住的阶段
- **依赖关系是使能器** - 它们展示什么是可能的，而不是下一步必须做什么

> **自定义：** OPSX 工作流由定义产物序列的 schema 驱动。有关创建自定义 schema 的详细信息，请参阅[自定义](customization.md)。

## 两种模式

### 默认快速路径（`core` 配置）

新安装默认使用 `core`，提供：
- `/opsx:propose`
- `/opsx:explore`
- `/opsx:apply`
- `/opsx:sync`
- `/opsx:archive`

典型流程：

```text
/opsx:propose ──► /opsx:apply ──► /opsx:sync ──► /opsx:archive
```

### 扩展/完整工作流（自定义选择）

如果你想要显式的 scaffold 和构建命令（`/opsx:new`、`/opsx:continue`、`/opsx:ff`、`/opsx:verify`、`/opsx:bulk-archive`、`/opsx:onboard`），可以通过以下命令启用：

```bash
openspec config profile
openspec update
```

## 工作流模式（扩展模式）

### 快速功能

当你清楚要构建什么并且只需执行时：

```text
/opsx:new ──► /opsx:ff ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

**对话示例：**

```text
你：/opsx:new add-logout-button

AI：已创建 openspec/changes/add-logout-button/
    准备创建：proposal

你：/opsx:ff

AI：正在创建所有规划产物...
    ✓ proposal.md
    ✓ specs/
    ✓ design.md
    ✓ tasks.md
    准备实施！

你：/opsx:apply

AI：正在逐项完成任务...
    ✓ 在页头添加了注销按钮
    ✓ 实现了会话清除
    ✓ 添加了确认对话框
    所有任务完成！

你：/opsx:archive

AI：✓ 已合并 specs
    ✓ 已归档变更
```

**最佳适用于：** 中小型功能、错误修复、直接了当的变更。

### 探索型

当需求不明确或需要先进行调查时：

```text
/opsx:explore ──► /opsx:new ──► /opsx:continue ──► ... ──► /opsx:apply
```

**对话示例：**

```text
你：/opsx:explore

AI：你想探索什么？

你：我想提高页面加载性能，但我不确定瓶颈在哪里。

AI：让我帮你调查...
    [分析打包大小，识别慢查询，审查组件渲染模式]

    我发现三个主要瓶颈：
    1. 大型未优化的图片
    2. ProductList 中的同步数据获取
    3. 上下文变更导致的重复渲染

    你想先处理哪一个？

你：我们先解决数据获取的问题。

你：/opsx:new optimize-product-list-fetching

AI：已创建变更。准备创建：proposal

你：/opsx:continue

AI：基于我们的探索创建 proposal...
    [根据调研结果编写 proposal]

    准备创建：specs, design
    接下来想创建哪个？

你：/opsx:continue

AI：正在创建 specs...
```

**最佳适用于：** 性能优化、调试、架构决策、需求不明确。

### 并行变更

同时处理多个变更：

```text
变更 A：/opsx:new ──► /opsx:ff ──► /opsx:apply（进行中）
                                         │
                                    上下文切换
                                         │
变更 B：/opsx:new ──► /opsx:ff ──────► /opsx:apply
```

**对话示例：**

```text
你：我正在处理 add-dark-mode，但被拉去修一个 bug

你：/opsx:new fix-login-redirect

AI：已创建 openspec/changes/fix-login-redirect/

你：/opsx:ff

AI：✓ 已创建规划产物

你：/opsx:apply

AI：正在处理 fix-login-redirect...
    [实施修复]
    所有任务完成！

你：/opsx:archive

AI：✓ 已归档 fix-login-redirect

你：让我们回到暗色模式

你：/opsx:apply add-dark-mode

AI：正在恢复 add-dark-mode...
    从任务 2.3 继续：更新 Header...
```

**最佳适用于：** 并行工作流、紧急中断、团队协作。

当你有多项已完成变更时，使用 `/opsx:bulk-archive`：

```text
你：/opsx:bulk-archive

AI：发现 3 项已完成的变更：
    - add-dark-mode（所有任务完成）
    - fix-login-redirect（所有任务完成）
    - update-footer（所有任务完成）

    正在检查 spec 冲突...
    ⚠ add-dark-mode 和 update-footer 都涉及 specs/ui/

    正在检查代码库以解决冲突...
    两项变更均已实施。将按时间顺序应用。

    归档所有 3 项变更？

你：是的

AI：✓ 已归档 add-dark-mode
    ✓ 已归档 fix-login-redirect
    ✓ 已归档 update-footer
    Specs 已按顺序合并：add-dark-mode → update-footer
```

批量归档检测多个变更是否涉及相同的 specs，并通过检查实际实施情况来解决冲突。

### 完成变更

推荐的完成流程：

```text
/opsx:apply ──► /opsx:verify ──► /opsx:archive
                    │                 │
              验证实施         提示同步
                               如果需要
```

#### 验证：检查你的工作

`/opsx:verify` 从三个维度验证实施是否与产物匹配：

```text
你：/opsx:verify

AI：正在验证 add-auth...

    完整性
    ✓ tasks.md 中的所有 12 项任务均已检查
    ✓ specs 中的所有需求都有对应的代码
    ⚠ 场景"不活动超时"未测试

    正确性
    ✓ 实施符合 spec 意图
    ✓ 已处理场景中的边界情况
    ✓ 错误状态符合 spec 定义

    一致性
    ✓ 设计决策已反映在代码结构中
    ✓ 命名约定与 design.md 一致
    ⚠ 设计提到"事件驱动"但实施使用了轮询

    摘要
    ─────────────────────────────
    严重问题：0
    警告：2
    可归档：是（带有警告）

    建议：
    1. 为会话超时场景添加测试
    2. 考虑按设计重构为事件驱动，或更新 design.md
```

**验证检查的内容：**

| 维度 | 验证内容 |
|-----------|------------------|
| 完整性 | 所有任务完成，所有需求已实施，场景已覆盖 |
| 正确性 | 实施符合 spec 意图，边界情况已处理 |
| 一致性 | 设计决策已反映在代码中，模式一致 |

验证不会阻止归档，但会暴露你可能想要先处理的问题。

#### 归档：最终确定变更

`/opsx:archive` 完成变更并将其移至归档：

```text
你：/opsx:archive

AI：正在归档 add-auth...

    产物状态：
    ✓ proposal.md 存在
    ✓ specs/ 存在
    ✓ design.md 存在
    ✓ tasks.md 存在（12/12 任务完成）

    Delta specs：尚未同步到主目录
    → 是否现在同步？

你：是的

AI：✓ 已将 specs 同步到 openspec/specs/auth/spec.md
    ✓ 已移至 openspec/changes/archive/2025-01-24-add-auth/

    变更已成功归档。
```

如果 specs 尚未同步，归档会提示。它不会阻止不完整的任务，但会给出警告。

## 何时使用什么

### `/opsx:ff` 与 `/opsx:continue`

| 情况 | 使用 |
|-----------|-----|
| 需求明确，准备构建 | `/opsx:ff` |
| 正在探索，想逐步审查每一步 | `/opsx:continue` |
| 想在 specs 之前迭代 proposal | `/opsx:continue` |
| 时间紧迫，需要快速推进 | `/opsx:ff` |
| 复杂变更，想要控制 | `/opsx:continue` |

**经验法则：** 如果你能预先描述完整范围，使用 `/opsx:ff`。如果你在过程中逐步明确，使用 `/opsx:continue`。

### 何时更新与何时重新开始

一个常见问题：什么时候更新现有变更是可以的，什么时候应该开始新的变更？

**更新现有变更时：**

- 相同意图，执行上有所调整
- 范围缩小（先做 MVP，其余后续处理）
- 基于学习的修正（代码库与预期不符）
- 基于实施发现的设计调整

**开始新变更时：**

- 意图发生根本性改变
- 范围扩展到完全不同的工作
- 原有变更可以单独标记为"完成"
- 打补丁反而会造成更多混乱而非澄清

```text
                     ┌─────────────────────────────────────┐
                     │     这是同一项工作吗？              │
                     └──────────────┬──────────────────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          意图相同？      重叠超过 50%？     原有变更能否
          问题相同？      范围相同？         "完成"而无需
                 │                  │          这些改动？
                 │                  │                  │
       ┌────────┴────────┐  ┌──────┴──────┐   ┌───────┴───────┐
       │                 │  │             │   │               │
      是               否  是           否  否              是
       │                 │  │             │   │               │
       ▼                 ▼  ▼             ▼   ▼               ▼
    更新              新变更 更新        新变更 更新         新变更
```

**示例："添加暗色模式"**

- "还需要支持自定义主题" → 新变更（范围扩展）
- "系统偏好检测比预期更难" → 更新（相同意图）
- "我们先发布切换开关，稍后添加偏好设置" → 更新，然后归档，然后新变更

## 最佳实践

### 保持变更聚焦

每个变更一个逻辑工作单元。如果你在做"添加功能 X 并重构 Y"，考虑分成两个独立的变更。

**为什么重要：**
- 更易于审查和理解
- 更清晰的归档历史
- 可以独立发布
- 需要时回滚更简单

### 对不明确的需求使用 `/opsx:explore`

在提交变更之前，探索问题空间：

```text
你：/opsx:explore

AI：你想探索什么？

你：我们应该如何处理 API 的速率限制？

AI：让我调查你当前的设置和选项...
    [研究代码库，考虑模式]

    我看到我们可以采用三种方法：
    1. 基于中间件（简单，每个端点）
    2. 基于 Redis（可扩展，共享状态）
    3. 基于令牌桶（公平，复杂）

    你当前的栈建议使用 #1 或 #2。你的规模如何？
```

探索在你创建产物之前理清思路。

### 归档前验证

使用 `/opsx:verify` 检查实施是否与产物匹配：

```text
你：/opsx:verify

AI：正在验证 add-dark-mode...

    ✓ tasks.md 中的所有任务均已检查
    ✓ specs 中的需求均有对应代码
    ✓ 设计决策已反映在实施中

    可归档！
```

在关闭变更之前发现不匹配。

### 清晰命名变更

好的命名让 `openspec list` 更有用：

```text
好的：                          避免：
add-dark-mode                  feature-1
fix-login-redirect             update
optimize-product-query         changes
implement-2fa                  wip
```

## 命令快速参考

有关完整的命令详情和选项，请参阅[命令](commands.md)。

| 命令 | 用途 | 何时使用 |
|---------|---------|-------------|
| `/opsx:propose` | 创建变更 + 规划产物 | 快速默认路径（`core` 配置） |
| `/opsx:explore` | 思考想法 | 需求不明确，需要调研 |
| `/opsx:new` | 启动变更 scaffold | 扩展模式，明确的产物控制 |
| `/opsx:continue` | 创建下一个产物 | 扩展模式，逐步创建产物 |
| `/opsx:ff` | 创建所有规划产物 | 扩展模式，范围明确 |
| `/opsx:apply` | 实施任务 | 准备编写代码 |
| `/opsx:verify` | 验证实施 | 扩展模式，归档前 |
| `/opsx:sync` | 合并 delta specs | 扩展模式，可选 |
| `/opsx:archive` | 完成变更 | 所有工作完成 |
| `/opsx:bulk-archive` | 归档多个变更 | 扩展模式，并行工作 |

## 下一步

- [命令](commands.md) - 完整的命令参考及选项
- [概念](concepts.md) - 深入了解 specs、产物和 schema
- [自定义](customization.md) - 创建自定义工作流
