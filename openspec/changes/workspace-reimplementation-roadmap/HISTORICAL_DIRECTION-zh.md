# 工作区重新实现方向

日期：2026-04-30

## 状态

本文档是来自工作区 POC 后续的历史产品方向。它对保留的工作区 setup、link、open、update、doctor 和智能体可见性决策仍然有用。

它不再定义持久的协调模型。当前权威是 `openspec/initiatives/context-store-and-initiatives/direction.md`，它锁定了以下边界：

```text
上下文存储同步真相。
集合塑造真相。
倡议协调工作。
工作区打开本地视图。
Change 实现仓库拥有的切片。
```

此处被取代的内容：工作区作为持久的规划家园、工作区级别规划 artifact 作为规范的共享跨仓库计划、以及工作区 apply/verify/archive 作为下一个头等生命周期命令。

此处被推迟的内容：apply、verify、archive、分支/工作树编排、跨仓库验证、依赖图强制执行和治理流程，直到存在倡议链接的仓库本地 change。

新智能体入口点：首先阅读 `openspec/changes/workspace-reimplementation-roadmap/START_HERE.md`，然后返回本文档获取完整的产品方向。

本文档记录了基于从工作区 POC 中学到的经验，从头开始重新实现 OpenSpec 工作区支持的预期方向。

以下章节是历史的 POC 后续方向。仅将其用于经验教训和保留的本地视图行为。不要将后续的工作区生命周期章节视为活跃的实现指导。

重新实现应围绕真实用户通过 OpenSpec 的路径来排序：

```text
设置工作区
  -> 链接仓库或文件夹
  -> 打开工作区
  -> 跨仓库或文件夹探索
  -> 创建 proposal
  -> 应用一个仓库切片
  -> 验证
  -> 归档
```

目标不是重建每个 POC 机制。目标是按照用户自然创建、实现、验证和归档变更的顺序，一次获得一个用户可见的能力。

## 北极星

用户应该想到：

```text
我有一个多仓库产品目标。
我设置了一个 OpenSpec 工作区。
我用智能体打开它。
智能体可以看到链接的仓库或文件夹。
我们探索直到范围清晰。
然后我们创建 proposal。
然后我们一次实现一个仓库切片。
```

他们不应该想到：

```text
我需要创建一个 change 以便仓库可见。
我需要物化仓库本地 artifact。
我需要理解实现特定的工作区机制。
我需要独立于 proposal 文件管理目标元数据。
```

核心产品规则是：

```text
工作区可见性不是变更承诺。
```

链接的仓库或文件夹是规划上下文。创建 change 是一个规划承诺。应用 change 是一个实现工作流。

## 构建顺序

### 1. 工作区设置和链接

首先使工作区设置变得简单可靠。

用户目标：

```text
创建一个规划家园并链接 OpenSpec 应该知道的仓库或文件夹。
```

预期界面：

```bash
openspec workspace setup
openspec workspace setup --no-interactive --name platform --link /path/to/api --link web=/path/to/web
openspec workspace list
openspec workspace ls
openspec workspace link /path/to/api
openspec workspace link api-service /path/to/api
openspec workspace relink api /new/path/to/api
openspec workspace doctor
```

预期结果：

```text
workspace-folder/
  changes/
  .openspec-workspace/
    workspace.yaml
    local.yaml
```

产品决策：

- 工作区元数据使用 `.openspec-workspace/`，而非 `.openspec/`。
- 保持 `changes/` 在工作区文件夹中可见。
- 首次发布仅保留 setup 作为唯一的公开创建路径；不暴露 `workspace create`。
- 使用 `workspace link` 和 `workspace relink`，而非 POC 时代的 `add-repo` 或 `update-repo`。
- 允许链接的仓库或文件夹没有仓库本地 `openspec/` 状态。
- 在共享工作区状态中保留稳定的链接名称，在机器本地状态中保留本地路径。
- 使 `doctor` 显示链接名称、已解析路径、存在时的仓库本地 specs 路径以及建议的修复。

推迟：

- 智能体启动和工作区打开行为。
- 首选智能体提示。
- 所有者或交接元数据。
- 工作区 change 创建或目标选择。
- 分支。
- 工作树。
- Apply。
- Archive。
- 复杂的目标生命周期。

当用户可以设置工作区、链接仓库或文件夹、列出已知工作区、重新链接本地路径并运行 `doctor` 以准确查看 OpenSpec 可以解析的内容时，即完成。

### 2. 打开工作区

接下来使用户能够以期望的方式打开工作区。

用户目标：

```text
用我的编码智能体打开这个多仓库规划上下文。
```

预期界面：

```bash
openspec workspace open
openspec workspace open --agent codex
openspec workspace open --agent github-copilot
```

产品行为：

- `workspace open` 打开协调工作区加链接的仓库或文件夹。
- 仓库默认可见。
- Change 选择是可选焦点，而非仓库访问的机制。
- `--agent` 默认应为单会话覆盖。持久化首选智能体需要显式的偏好设置操作。

对于 GitHub Copilot，生成或打开一个包含以下内容的 `.code-workspace` 文件：

```text
workspace folder
linked repo or folder A
linked repo or folder B
```

对于 Claude 和 Codex，通过智能体支持的机制附加链接的仓库或文件夹目录。

推迟：

- `workspace open --change`。
- 会话内升级流程。
- 每个 change 的附件限制。

当打开工作区使智能体能够看到协调根目录和所有链接的仓库或文件夹时，即完成。

### 3. 智能体指导和探索

然后使探索工作。

用户目标：

```text
告诉智能体一个粗略的产品目标，让它在创建 proposal 之前检查仓库。
```

预期用户提示：

```text
探索如何在登陆页面上提供 OpenSpec 文档。
查看所有链接的仓库或文件夹，但暂不实现。
```

智能体行为：

- 理解自己处于工作区模式。
- 检查链接的仓库或文件夹。
- 解释可能受影响的仓库。
- 仅在需要时要求澄清。
- 在探索期间避免实现性编辑。

构建：

- 工作区级别 `AGENTS.md` 指导。
- 工作区会话中的正常 OpenSpec 技能和命令。
- 在工作区特定指导之上分层添加，而非替换正常的 `/explore`。

推迟：

- Proposal artifact 生成。
- 目标确认命令。
- 应用上下文提供者。

当用户可以打开工作区并在不创建虚拟 change 的情况下运行有用的跨仓库探索时，即完成。

### 4. 创建 Proposal

仅在探索工作之后，构建 proposal 创建。

用户目标：

```text
现在我们了解了范围，把计划记录下来。
```

预期用户提示：

```text
为此变更创建 proposal。
定位实际受影响的仓库。
```

首选 artifact 形态：

```text
changes/integrate-docs/
  proposal.md
  design.md
  tasks.md
  specs/
    openspec/
      docs-conventions/spec.md
    landing/
      docs-routing/spec.md
```

关键工作流规则：

```text
/explore 可能让目标未知。
/propose 可能发现目标。
/propose 必须在说准备 apply 之前确认目标。
```

目标应尽可能由 proposal artifact 本身表示。如果有 `specs/landing/...`，则 `landing` 在范围内。避免使用单独的必填 `targets: [...]` 元数据列表作为活跃的可信源。

推迟：

- 仓库本地物化。
- 工作树选择。
- 多仓库实现。
- Archive。

当用户可以探索，然后创建带有仓库范围 specs 和 tasks 的工作区 proposal 时，即完成。

### 5. 状态

在实现之前，使状态变得出色。

用户目标：

```text
我们在哪里，涉及哪些仓库，这个准备好实现了吗？
```

预期界面：

```bash
openspec status
openspec status --change integrate-docs
```

人类可读输出应回答：

```text
Change: integrate-docs
范围：openspec, landing
Proposal：存在
Design：存在
Tasks：存在
准备 apply：是/否
```

状态还应捕捉结构性错误：

- `specs/` 下的未知仓库文件夹。
- 缺少 tasks。
- 未确认受影响的仓库。
- 链接的仓库或文件夹路径缺失。

当智能体和用户在 apply 之前可以信任状态时，即完成。

### 6. 应用一个仓库切片

现在才构建 `/apply`。

用户目标：

```text
为一个仓库实现计划的切片。
```

预期用户提示：

```text
/apply integrate-docs for landing
```

产品契约：

```text
/apply 意味着实现。
```

它不意味着：

```text
复制规划文件
物化仓库本地 OpenSpec 状态
首次创建 proposal 文件
```

智能体行为：

1. 向 OpenSpec 请求 apply 上下文。
2. 读取 proposal、design、tasks 和相关 specs。
3. 确认目标仓库检出。
4. 仅编辑该仓库。
5. 更新工作区 tasks。
6. 运行相关检查。

这可能在内部需要一个标准化的上下文命令，但那是支撑性机制：

```json
{
  "mode": "workspace",
  "change": "integrate-docs",
  "target": "landing",
  "implementationRoot": "/repos/openspec-landing",
  "contextFiles": [
    "changes/integrate-docs/proposal.md",
    "changes/integrate-docs/design.md",
    "changes/integrate-docs/tasks.md",
    "changes/integrate-docs/specs/landing/docs-routing/spec.md"
  ],
  "allowedEditRoots": [
    "/repos/openspec-landing"
  ],
  "tasksFile": "changes/integrate-docs/tasks.md"
}
```

推迟：

- 一次应用多个仓库。
- 自动创建分支。
- 工作树管理。
- 仓库本地 OpenSpec 镜像。

当一个仓库切片可以从中心工作区计划实现时，即完成。

### 7. 验证

然后构建验证。

用户目标：

```text
检查已实现的仓库切片是否满足计划。
```

预期提示：

```text
/verify integrate-docs for landing
```

行为：

- 读取与 `/apply` 相同的标准化上下文。
- 检查实现检出。
- 检查该仓库的 tasks 和 specs。
- 运行仓库验证。
- 清晰报告差距。

默认行为应验证一个仓库切片。全局工作区验证可以稍后实现。

当用户可以对照中心工作区计划验证一个已实现的仓库切片时，即完成。

### 8. 归档

归档是第一个完整循环中的最后一步。

用户目标：

```text
变更已完成。将其移出活跃规划。
```

预期提示：

```text
/archive integrate-docs
```

行为：

- 要求所有目标仓库切片已完成或明确接受。
- 归档工作区 change。
- 除非 OpenSpec 稍后确定仓库本地归档很重要，否则不要求仓库本地规划副本。

当用户可以完成完整生命周期时，即完成：

```text
workspace setup
  -> link repos or folders
  -> open
  -> explore
  -> propose
  -> apply repo A
  -> apply repo B
  -> verify
  -> archive
```

## 实现纪律

只构建下一个用户可见的步骤。

序列应保持基于以下问题：

```text
1. 我能设置工作区吗？
2. 我能看到我链接的仓库或文件夹吗？
3. 我的智能体能探索它们吗？
4. 我们能捕获 proposal 吗？
5. 状态能告诉我们它是否准备好了吗？
6. 智能体能否实现一个仓库切片？
7. 我们能验证它吗？
8. 我们能归档它吗？
```

避免从内部抽象开始，除非它们对下一个用户可见的能力是必需的。

不要从以下内容开始：

- 目标元数据机制。
- 物化。
- 适配器抽象。
- 分支编排。
- 工作树编排。
- 多仓库 apply。

这些可能以后重要，但它们不应定义第一个重新实现路径。

## 历史产品形态

这是较旧的工作区产品形态。此处保留是为了使 POC 的经验教训保持可理解，但它已被 context-store-and-initiatives 方向取代，用于持久协调。

历史持久产品模型是：

```text
workspace = 规划家园
links = 规划可见的仓库或文件夹
proposal = 限定范围的规划承诺
repo slice = 计划中的一个受影响仓库或文件夹
branch/worktree = 实现检出
/apply = 实现一个选定的仓库切片
```

当前持久产品模型是：

```text
context store = 同步的共享真相
initiative = 持久协调对象
workspace = 本地打开的视图
repo change = 仓库拥有的实现计划
```

历史用户旅程是：

```text
打开工作区。
让智能体探索。
范围清晰时创建 proposal。
一次实现一个仓库切片。
验证。
归档。
```
