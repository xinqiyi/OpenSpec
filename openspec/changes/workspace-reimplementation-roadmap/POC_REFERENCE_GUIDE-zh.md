# workspace POC 参考指南

本指南适用于从头开始的新会话、对 workspace POC 没有先前上下文的新智能体。

根入口点：`START_HERE.md`。

目标不是继续 POC。目标是在从当前基线保留或替换特定行为之前，将其用作研究材料。

当前产品权威位于 `openspec/initiatives/context-store-and-initiatives/`。在该方向下，workspace setup/open/update/doctor 行为仍然是可用的本地视图基础设施。workspace 级别的 apply、verify 和 archive 研究将推迟，直到存在倡议关联的 repository 本地 change。

## 参考点

使用此精确提交作为稳定参考：

```text
workspace-poc @ 79a45ac043f414e63d13e08b9da83b135cb20a39
```

不要仅依赖移动的分支名称。不要将此提交合并到实现分支中。除非后续 proposal 明确决定保留某个小片段，否则不要从中 cherry-pick。

## POC 试图证明什么

从用户旅程开始：

```text
创建 workspace
 -> 添加 repository
 -> 用智能体打开 workspace
 -> 跨 repository 探索
 -> 创建 proposal
 -> 应用一个 repository 切片
 -> 验证
 -> archive
```

如果 POC 有助于回答以下问题，它就是有用的：

- workspace schema 工作时，用户体验如何？
- 哪些 CLI 界面使 workflow 更易于理解？
- 哪些测试捕捉到了真实的产品期望？
- 哪些实现选择是捷径，不应保留？
- 哪些术语在产品形态更清晰后变得具有误导性？

## 首先阅读的文件

在实现之前，从 POC 提交中阅读这些文件：

```text
WORKSPACE_REIMPLEMENTATION_DIRECTION.md
WORKSPACE_POC_FOLLOWUP_NOTES.md
docs/workspace.md
docs/workspace-demo.md
docs/cli.md
src/commands/workspace.ts
src/core/workspace/open.ts
test/commands/workspace/open.test.ts
test/core/workspace/open.test.ts
test/cli-e2e/workspace/workspace-open-cli.test.ts
```

可选的更深层上下文：

```text
workspace-poc-explorer.html
workspace-poc-phase-playground.html
copilot-session-d4e9c61e-readable.md
copilot-session-d4e9c61e-timeline.md
```

可选文件是历史研究辅助工具。用于理解 POC 如何演化，而非作为实现需求。

## 如何安全地检查 POC

推荐方法：使用单独的工作树或直接从固定提交读取文件。

直接读取示例：

```bash
git show 79a45ac043f414e63d13e08b9da83b135cb20a39:WORKSPACE_REIMPLEMENTATION_DIRECTION.md
git show 79a45ac043f414e63d13e08b9da83b135cb20a39:src/commands/workspace.ts
git diff origin/main...79a45ac043f414e63d13e08b9da83b135cb20a39 --stat
```

单独工作树示例：

```bash
git worktree add ../openspec-workspace-poc 79a45ac043f414e63d13e08b9da83b135cb20a39
```

保持实现分支基于当前目标分支。POC 工作树仅用于阅读和运行测试。

## 带回什么

在实现一个切片之前，带回一个简短的 POC 发现记录：

```text
<切片> 的 POC 发现：

需要保留的用户行为：
- ...

值得迁移的测试或示例：
- ...

需要避免的实现捷径：
- ...

开放的设计问题：
- ...
```

将持久的发现记录在相关的 OpenSpec proposal 或设计 artifact 中。不要将重要决策仅留在聊天记录中。

## 切片特定阅读

### `workspace-foundation`

重点关注：

- workspace 文件夹结构
- 元数据目录命名
- 本地状态与已提交状态
- 稳定的 workspace 名称语义

阅读：

```text
WORKSPACE_REIMPLEMENTATION_DIRECTION.md
WORKSPACE_POC_FOLLOWUP_NOTES.md
docs/workspace.md
src/commands/workspace.ts
```

带回：

- 值得保留的存储模型
- 元数据命名决策
- 与 repository 本地 `openspec/` 的任何兼容性风险

### `workspace-create-and-register-repos`

重点关注：

- 用户如何创建 workspace
- repository 或文件夹如何链接
- `doctor` 或等效的状态输出应解释什么
- POC 的 `create`/`add-repo` 行为如何映射到目标的 `setup`/`link`/`relink`/`doctor` 流程
- 仅 planning repository 和 monorepo 模块与可实现 repository 本地 OpenSpec 项目有何不同

阅读：

```text
docs/workspace.md
docs/workspace-demo.md
src/commands/workspace.ts
test/commands/workspace/setup.test.ts
```

带回：

- 预期命令
- 预期文件
- 对错误路径、重复 workspace 名称、缺失路径、仅 planning 链接和重复链接名称的验证行为

### `workspace-open-agent-context`

重点关注：

- 智能体接收什么上下文
- 链接的 repository 或文件夹如何变为可见
- 单会话智能体选择应如何工作
- 什么是稳定指导，什么是动态启动上下文

阅读：

```text
WORKSPACE_POC_FOLLOWUP_NOTES.md
src/commands/workspace.ts
src/core/workspace/open.ts
test/commands/workspace/open.test.ts
test/core/workspace/open.test.ts
test/cli-e2e/workspace/workspace-open-cli.test.ts
```

带回：

- 启动上下文需求
- 需要保留的智能体特定行为
- 应成为稳定指令的提示或指导文本

### `workspace-change-planning`

重点关注：

- 何时 repository 范围成为 planning 承诺
- 目标是否应从 artifact 推断
- 如何安排 proposal、design、tasks 和 specs

阅读：

```text
WORKSPACE_REIMPLEMENTATION_DIRECTION.md
docs/workspace.md
docs/workspace-demo.md
```

带回：

- 要使用的 artifact 形态
- 应如何确认目标
- 哪些 POC 目标元数据想法应避免或推迟

### `workspace-apply-repo-slice`

重点关注：

- 术语决策：apply 意味着实现
- 智能体实现一个 repository 切片需要什么上下文
- 为什么物化不应成为用户面对的契约

阅读：

```text
WORKSPACE_REIMPLEMENTATION_DIRECTION.md
WORKSPACE_POC_FOLLOWUP_NOTES.md
```

带回：

- 标准化的 apply 上下文形态
- 用户面对的 apply 契约
- 任何应被明确拒绝的 POC 物化行为

### `workspace-verify-and-archive`

重点关注：

- 部分 repository 完成与完整 workspace 完成
- 验证应如何报告差距
- archive 应如何避免强制 repository 本地 planning 副本

阅读：

```text
WORKSPACE_REIMPLEMENTATION_DIRECTION.md
docs/workspace-demo.md
```

带回：

- 最小可用的验证行为
- archive 前提条件
- repository 切片完成与 workspace 硬完成状态之间的区别

## 基本原则

- 将 POC 视为证据，而非遗产。
- 在保留代码之前先保留用户可见的经验教训。
- 优先使用当前 repository schema 而非 POC 独有的抽象。
- 一次实现一个用户可见的步骤。
- 当 POC 的教训改变后续切片时，更新此路线图。
