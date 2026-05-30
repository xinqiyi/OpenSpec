# workspace 重新实现方向

日期：2026-04-30

## 状态

本文档是来自 workspace POC 后续的历史产品方向。它对保留的 workspace setup、link、open、update、doctor 和智能体可见性决策仍然有用。

它不再定义持久的协调模型。当前权威是 `openspec/initiatives/context-store-and-initiatives/direction.md`，它锁定了以下边界：

```text
上下文存储同步真相。
集合塑造真相。
倡议协调工作。
workspace 打开本地视图。
Change 实现 repository 拥有的切片。
```

此处被取代的内容：workspace 作为持久的 planning 家园、workspace 级别 planning artifact 作为 spec 的共享跨 repository 计划、以及 workspace apply/verify/archive 作为下一个头等生命周期命令。

此处被推迟的内容：apply、verify、archive、分支/工作树编排、跨 repository 验证、依赖图强制执行和治理流程，直到存在倡议链接的 repository 本地 change。

新智能体入口点：首先阅读 `openspec/changes/workspace-reimplementation-roadmap/START_HERE.md`，然后返回本文档获取完整的产品方向。

本文档记录了基于从 workspace POC 中学到的经验，从头开始重新实现 OpenSpec workspace 支持的预期方向。

以下章节是历史的 POC 后续方向。仅将其用于经验教训和保留的本地视图行为。不要将后续的 workspace 生命周期章节视为活跃的实现指导。

重新实现应围绕真实用户通过 OpenSpec 的路径来排序：

```text
设置 workspace
 -> 链接 repository 或文件夹
 -> 打开 workspace
 -> 跨 repository 或文件夹探索
 -> 创建 proposal
 -> 应用一个 repository 切片
 -> 验证
 -> archive
```

目标不是重建每个 POC 机制。目标是按照用户自然创建、实现、验证和 archive 变更的顺序，一次获得一个用户可见的能力。

## 北极星

用户应该想到：

```text
我有一个多 repository 产品目标。
我设置了一个 OpenSpec workspace。
我用智能体打开它。
智能体可以看到链接的 repository 或文件夹。
我们探索直到范围清晰。
然后我们创建 proposal。
然后我们一次实现一个 repository 切片。
```

他们不应该想到：

```text
我需要创建一个 change 以便 repository 可见。
我需要物化 repository 本地 artifact。
我需要理解实现特定的 workspace 机制。
我需要独立于 proposal 文件管理目标元数据。
```

核心产品规则是：

```text
workspace 可见性不是变更承诺。
```

链接的 repository 或文件夹是 planning 上下文。创建 change 是一个 planning 承诺。应用 change 是一个实现 workflow。

## 构建顺序

### 1. workspace 设置和链接

首先使 workspace 设置变得简单可靠。

用户目标：

```text
创建一个 planning 家园并链接 OpenSpec 应该知道的 repository 或文件夹。
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

- workspace 元数据使用 `.openspec-workspace/`，而非 `.openspec/`。
- 保持 `changes/` 在 workspace 文件夹中可见。
- 首次发布仅保留 setup 作为唯一的公开创建路径；不暴露 `workspace create`。
- 使用 `workspace link` 和 `workspace relink`，而非 POC 时代的 `add-repo` 或 `update-repo`。
- 允许链接的 repository 或文件夹没有 repository 本地 `openspec/` 状态。
- 在共享 workspace 状态中保留稳定的链接名称，在机器本地状态中保留本地路径。
- 使 `doctor` 显示链接名称、已解析路径、存在时的 repository 本地 specs 路径以及建议的修复。

推迟：

- 智能体启动和 workspace 打开行为。
- 首选智能体提示。
- 所有者或交接元数据。
- workspace change 创建或目标选择。
- 分支。
- 工作树。
- Apply。
- Archive。
- 复杂的目标生命周期。

当用户可以设置 workspace、链接 repository 或文件夹、列出已知 workspace、重新链接本地路径并运行 `doctor` 以准确查看 OpenSpec 可以解析的内容时，即完成。

### 2. 打开 workspace

接下来使用户能够以期望的方式打开 workspace。

用户目标：

```text
用我的编码智能体打开这个多 repository planning 上下文。
```

预期界面：

```bash
openspec workspace open
openspec workspace open --agent codex
openspec workspace open --agent github-copilot
```

产品行为：

- `workspace open` 打开协调 workspace 加链接的 repository 或文件夹。
- repository 默认可见。
- Change 选择是可选焦点，而非 repository 访问的机制。
- `--agent` 默认应为单会话覆盖。持久化首选智能体需要显式的偏好设置操作。

对于 GitHub Copilot，生成或打开一个包含以下内容的 `.code-workspace` 文件：

```text
workspace folder
linked repo or folder A
linked repo or folder B
```

对于 Claude 和 Codex，通过智能体支持的机制附加链接的 repository 或文件夹目录。

推迟：

- `workspace open --change`。
- 会话内升级流程。
- 每个 change 的附件限制。

当打开 workspace 使智能体能够看到协调根目录和所有链接的 repository 或文件夹时，即完成。

### 3. 智能体指导和探索

然后使探索工作。

用户目标：

```text
告诉智能体一个粗略的产品目标，让它在创建 proposal 之前检查 repository。
```

预期用户提示：

```text
探索如何在登陆页面上提供 OpenSpec 文档。
查看所有链接的 repository 或文件夹，但暂不实现。
```

智能体行为：

- 理解自己处于 workspace schema。
- 检查链接的 repository 或文件夹。
- 解释可能受影响的 repository。
- 仅在需要时要求澄清。
- 在探索期间避免实现性编辑。

构建：

- workspace 级别 `AGENTS.md` 指导。
- workspace 会话中的正常 OpenSpec skill 和命令。
- 在 workspace 特定指导之上分层添加，而非替换正常的 `/explore`。

推迟：

- Proposal artifact 生成。
- 目标确认命令。
- 应用上下文提供者。

当用户可以打开 workspace 并在不创建虚拟 change 的情况下运行有用的跨 repository 探索时，即完成。

### 4. 创建 Proposal

仅在探索工作之后，构建 proposal 创建。

用户目标：

```text
现在我们了解了范围，把计划记录下来。
```

预期用户提示：

```text
为此变更创建 proposal。
定位实际受影响的 repository。
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

关键 workflow 规则：

```text
/explore 可能让目标未知。
/propose 可能发现目标。
/propose 必须在说准备 apply 之前确认目标。
```

目标应尽可能由 proposal artifact 本身表示。如果有 `specs/landing/...`，则 `landing` 在范围内。避免使用单独的必填 `targets: [...]` 元数据列表作为活跃的可信源。

推迟：

- repository 本地物化。
- 工作树选择。
- 多 repository 实现。
- Archive。

当用户可以探索，然后创建带有 repository 范围 specs 和 tasks 的 workspace proposal 时，即完成。

### 5. 状态

在实现之前，使状态变得出色。

用户目标：

```text
我们在哪里，涉及哪些 repository，这个准备好实现了吗？
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

- `specs/` 下的未知 repository 文件夹。
- 缺少 tasks。
- 未确认受影响的 repository。
- 链接的 repository 或文件夹路径缺失。

当智能体和用户在 apply 之前可以信任状态时，即完成。

### 6. 应用一个 repository 切片

现在才构建 `/apply`。

用户目标：

```text
为一个 repository 实现计划的切片。
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
复制 planning 文件
物化 repository 本地 OpenSpec 状态
首次创建 proposal 文件
```

智能体行为：

1. 向 OpenSpec 请求 apply 上下文。
2. 读取 proposal、design、tasks 和相关 specs。
3. 确认目标 repository 检出。
4. 仅编辑该 repository。
5. 更新 workspace tasks。
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

- 一次应用多个 repository。
- 自动创建分支。
- 工作树管理。
- repository 本地 OpenSpec 镜像。

当一个 repository 切片可以从中心 workspace 计划实现时，即完成。

### 7. 验证

然后构建验证。

用户目标：

```text
检查已实现的 repository 切片是否满足计划。
```

预期提示：

```text
/verify integrate-docs for landing
```

行为：

- 读取与 `/apply` 相同的标准化上下文。
- 检查实现检出。
- 检查该 repository 的 tasks 和 specs。
- 运行 repository 验证。
- 清晰报告差距。

默认行为应验证一个 repository 切片。全局 workspace 验证可以稍后实现。

当用户可以对照中心 workspace 计划验证一个已实现的 repository 切片时，即完成。

### 8. archive

archive 是第一个完整循环中的最后一步。

用户目标：

```text
变更已完成。将其移出活跃 planning。
```

预期提示：

```text
/archive integrate-docs
```

行为：

- 要求所有目标 repository 切片已完成或明确接受。
- archive workspace change。
- 除非 OpenSpec 稍后确定 repository 本地 archive 很重要，否则不要求 repository 本地 planning 副本。

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
1. 我能设置 workspace 吗？
2. 我能看到我链接的 repository 或文件夹吗？
3. 我的智能体能探索它们吗？
4. 我们能捕获 proposal 吗？
5. 状态能告诉我们它是否准备好了吗？
6. 智能体能否实现一个 repository 切片？
7. 我们能验证它吗？
8. 我们能 archive 它吗？
```

避免从内部抽象开始，除非它们对下一个用户可见的能力是必需的。

不要从以下内容开始：

- 目标元数据机制。
- 物化。
- 适配器抽象。
- 分支编排。
- 工作树编排。
- 多 repository apply。

这些可能以后重要，但它们不应定义第一个重新实现路径。

## 历史产品形态

这是较旧的 workspace 产品形态。此处保留是为了使 POC 的经验教训保持可理解，但它已被 context-store-and-initiatives 方向取代，用于持久协调。

历史持久产品模型是：

```text
workspace = planning 家园
links = planning 可见的 repository 或文件夹
proposal = 限定范围的 planning 承诺
repo slice = 计划中的一个受影响 repository 或文件夹
branch/worktree = 实现检出
/apply = 实现一个选定的 repository 切片
```

当前持久产品模型是：

```text
context store = 同步的共享真相
initiative = 持久协调对象
workspace = 本地打开的视图
repo change = repository 拥有的实现计划
```

历史用户旅程是：

```text
打开 workspace。
让智能体探索。
范围清晰时创建 proposal。
一次实现一个 repository 切片。
验证。
archive。
```
