# 探索倡议托管的目标绑定变更 artifact——证据

## 初步研究笔记

- 当前产品方向表明上下文存储同步共享事实，倡议协调工作，repository 本地变更拥有实现 planning。
- 路线图第 8 项目前假设 repository 本地变更链接到倡议。
- 现有的 planning 家园行为区分了 repository 本地和 workspace planning 家园，但没有上下文存储支持的变更家园。
- 新的 artifact workflow 命令已在某些地方消费已解析的 planning 路径，这可能成为未来变更家园解析的有用接缝。
- 较旧的命令界面仍然假设本地 OpenSpec 项目下的 `openspec/changes/`，并且在进行任何实现切片之前需要显式审计。

## 初步框架

可配置的变更家园是一个产品边界问题，而不仅仅是路径变更。上下文存储托管的 artifact 在验证、应用、archive 或 spec 同步可以安全运行之前，仍然需要明确的目标 repository 或 spec 根目录。

未来的探索应保留"变更家园"作为内部解析器语言，并围绕倡议托管的 planning artifact、目标绑定变更、实现目标和可编辑根目录使用更清晰的产品语言。

## agent 优先团队 UX 研究

日期：2026-05-23。

探索的问题：

```text
对于使用上下文存储、倡议、workspace 和 repository 本地变更的团队来说，
出色的 agent 优先开发者体验是什么样的？
```

### 外部 schema 笔记

- Linear 将倡议用作更高级别的协调对象，对项目进行分组并展示健康状态、所有权和活跃项目汇总。
- Jira planning 通常在多团队 planning 中，在史诗或其他子工作项之上使用倡议。
- GitLab 路线图展示跨组或项目的更高级别史诗和里程碑。
- GitHub Projects 强调与问题和 repository 工作保持连接的灵活 planning。

这些 schema 指向一种常见的划分：

```text
更高级别对象 = 协调和汇总
执行项 = 更接近团队、项目、repository 或问题拥有的工作
```

OpenSpec 应保持这种分离，同时使 agent 交接比人类项目管理工具更精确。

### 清晰的思维模型

来自研究的最强思维模型：

```text
倡议 = 共享的协调事实
Workspace = 倡议 + repository 之上的本地视角
repository 变更 = 可执行的实现计划
```

扩展的产品规则：

```text
上下文存储记住。
倡议协调。
Workspace 打开。
repository 本地变更实现。
```

关键不变性：

```text
工作身份不是存储位置。
存储位置不是编辑权限。
```

这为 agent 保持三个决策的分离：

- 用户在谈论什么工作？
- planning artifact 应存放在哪里？
- 现在可以编辑哪些文件或 repository？

### 建议的 artifact 类型

repository 上下文：

```text
openspec/changes/<change-id>/
```

用于 repository 拥有的实现计划。repository 本地变更可以通过可移植元数据引用倡议：

```yaml
initiative:
 store: platform
 id: billing-launch
```

Workspace 上下文：

```text
<store>/initiatives/<initiative-id>/work-items/<work-id>/
```

用于在 repository 所有权或实现目标明确之前的共享倡议 planning。这些应称为倡议工作项、planning 简报或 proposal，而不是可执行的 OpenSpec 变更，直到第 18 项为上下文存储支持的变更定义完整生命周期。

Workspace 本地变更：

```text
<workspace>/changes/<change-id>/
```

保留作为遗留或测试版兼容性，除非用户显式选择 workspace planning 流程。

### agent 优先 UX 场景

单一 repository 团队：

- 用户要求 agent 从 repository 内部创建 proposal。
- agent 解析倡议（如果已命名）。
- agent 创建一个链接到该倡议的 repository 本地变更。
- Apply、validate、sync 和 archive 保持 repository 本地。

单体 repository：

- 一个 repository 本地变更可以覆盖多个包或能力。
- agent 可能需要领域或包的提示。
- repository 仍然是实现所有者；领域澄清范围但不成为单独的变更家园。

多 repository 平台：

- Workspace 打开共享的倡议上下文加上本地 repository 克隆。
- 倡议协调平台成果。
- 当实现所有权已知时，每个拥有 repository 获得自己的链接 repository 本地变更。
- Workspace 状态应报告可用的本地 repository、缺失的本地路径和编辑边界。

中央架构团队：

- 架构师可以更新倡议需求、设计、契约、决策和问题，而不拥有实现。
- agent 应提供起草共享倡议上下文或在创建 repository 本地变更之前询问拥有 repository 的选项。

所有权未知：

- agent 不应创建实现变更。
- 它应添加或更新倡议级别的问题，或返回目标选项并请求 repository 或领域决策。

队友入职：

```text
克隆或注册上下文存储。
运行 context-store doctor。
打开或解析倡议。
通过 workspace 映射链接本地 repository。
要求 agent 从倡议继续。
```

### 理想的 agent JSON 块

agent 需要跨 create、status、instructions、resolve 和 list 的稳定路由词汇：

```json
{
 "workTarget": {
 "kind": "repo-change | initiative-work-item | workspace-change",
 "id": "add-billing-api",
 "root": "/absolute/path",
 "storePath": "initiatives/billing-launch/work-items/add-billing-api"
 },
 "initiativeLink": {
 "store": "platform",
 "id": "billing-launch",
 "root": "/absolute/store/initiatives/billing-launch"
 },
 "invocationContext": {
 "kind": "repo | workspace",
 "root": "/absolute/current/context"
 },
 "actionContext": {
 "mode": "implementation-ready | planning-only | target-selection-required",
 "sourceOfTruth": "repo | context-store | workspace-local",
 "allowedEditRoots": [],
 "requiresTargetSelection": true,
 "constraints": [
 "Use resolved output paths from the CLI.",
 "Do not infer editable repos from the current working directory."
 ]
 },
 "nextCommands": {}
}
```

重要的字段是：

- `workTarget`：agent 正在操作的对象。
- `initiativeLink`：spec 的共享协调上下文（如果存在）。
- `invocationContext`：命令运行的位置。
- `actionContext`：agent 可以编辑什么。
- `nextCommands`：agent 应运行的后续命令，而不是自行发明路径。

### 生命周期规则

- 当 repository 是允许的编辑根目录时，repository 本地变更是实现就绪的。
- 倡议工作项在它们选择或链接 repository 本地实现变更之前仅用于 planning。
- Workspace 本地变更是兼容性 artifact，不是首选的新共享 planning 模型。
- Apply、archive、repo spec sync 和 repo delta validation 应保持 repository 本地，直到上下文存储支持的变更生命周期被显式设计。
- 如果 `allowedEditRoots` 为空或需要目标选择，agent 应在编辑实现文件之前停止。

### 需要设计的边界情况

- 相同倡议 ID 存在于多个存储中。
- 某些注册的存储不可读或不同步。
- 一个 workspace 可以看到 repository 路径，但用户尚未将其选择为编辑目标。
- 终端在 workspace 内部，但计划的工作属于一个链接的 repository。
- 终端在一个链接的 repository 内部，但用户首先想要共享的倡议 planning。
- 一个 repository 本地变更引用了当前机器上未注册的倡议存储。
- 一个上下文存储工作项使用了另一位队友没有的 schema。
- 一个变更 ID 同时作为 repository 本地变更和倡议工作项存在。
- 一个中央团队编辑倡议上下文，而实现团队编辑链接的 repository 本地变更。

### 研究的建议方向

保持第 8 项范围狭窄：

- 向 repository 本地变更添加倡议元数据。
- 添加 `new change <id> --initiative <store>/<initiative> --json`。
- 使用 `initiative show` 加上 workspace/repository 上下文作为 agent 交接骨干。
- 在第 8 项中不实现上下文存储支持的 OpenSpec 变更。

使用第 18 项决定更大的模型：

- 倡议工作项是否应成为一级 artifact。
- "变更家园"是否保持为内部语言。
- 上下文存储托管的工作如何绑定到 repository 目标、spec、验证、应用、archive 和同步。
- skill 和生成的指导如何教导 agent 信任 CLI JSON 而不是硬编码路径或当前工作目录假设。

## 目标绑定重构子 agent

日期：2026-05-23。

探索的问题：

```text
鉴于中央与 repository 本地变更存储之间的产品张力，第 18 项在实现工作开始前应如何重构？
```

三个子 agent 从产品语义、agent 优先 UX 和生命周期/实现角度审查了第 18 项。

### 产品语义发现

- 可见的工作项不应被框架化为通用的可配置存储。那会使困难的问题听起来像路径管道。
- 更精确的产品问题是：倡议托管的 artifact 在绑定到目标 repository 或 spec 根目录后，能否成为可执行的 OpenSpec 变更。
- repository 本地变更仍然是默认的可执行实现 artifact。
- 倡议托管的 artifact 从仅 planning 的工作项、简报或 proposal 开始。
- "变更家园"可以保持为内部解析器语言，但不应是主要的面向用户概念。

建议的命名：

```text
探索倡议托管的目标绑定变更 artifact
```

### agent 优先 UX 发现

agent 需要稳定的 CLI 输出，将 artifact 与 agent 可以编辑的内容分开：

```text
计划位于：repository 本地 OpenSpec | 倡议上下文
可编辑目标：选定的 repository 路径 | 尚无
链接的倡议：platform/billing-launch
```

命令应报告结构化的操作上下文，而不是让生成的 skill 推断路径：

```json
{
 "workTarget": {
 "kind": "repo-change | initiative-work-item | initiative-hosted-change",
 "id": "add-billing-api",
 "root": "/absolute/path"
 },
 "initiativeLink": {
 "store": "platform",
 "id": "billing-launch"
 },
 "implementationTarget": {
 "kind": "repo",
 "id": "billing-api",
 "specRoot": "openspec"
 },
 "actionContext": {
 "mode": "implementation-ready | planning-only | target-selection-required | unsupported",
 "sourceOfTruth": "repo | context-store | workspace-local",
 "allowedEditRoots": [],
 "constraints": [
 "Use CLI-reported paths.",
 "Do not infer editable repos from the current working directory."
 ]
 },
 "nextCommands": {}
}
```

如果 `allowedEditRoots` 为空，agent 应在编辑实现文件之前停止。如果需要目标选择，命令应返回后续步骤选项，而不是静默创建模糊的实现变更。

### 生命周期和实现发现

本地代码仍然有强烈的 repository 本地假设：

- `src/core/planning-home.ts` 将 planning 家园建模为 `repo | workspace`。
- `src/commands/workflow/new-change.ts` 从当前 planning 家园解析存储，尚未暴露 `--initiative` 或 `--json`。
- `src/commands/validate.ts` 从 `process.cwd()/openspec/...` 验证变更和 spec。
- `src/core/archive.ts` 通过读取 `openspec/changes`、将 delta 应用到 `openspec/specs` 并将变更移入 `openspec/changes/archive` 来进行 archive。
- `src/core/artifact-graph/types.ts` 元数据尚未建模倡议链接、目标 repository 身份、artifact 家园或编辑边界。
- 生成的 skill 和 workflow template 仍然包含 repository 本地路径假设，如 `openspec/changes/<name>/`。

这些在当前 repository 本地模型中不是 bug。它们是倡议托管的可执行变更是生命周期设计而不是小型路径开关的证据。

### 更新的建议

保持第 8 项范围狭窄：

- 创建或链接带有倡议元数据的 repository 本地变更。
- 为 agent 交接添加 JSON 输出。
- 在第 8 项中不实现上下文存储托管可执行变更。

使用第 18 项回答更大的问题：

- 在实现目标已知之前存在什么倡议托管 artifact？
- 什么目标元数据让共享 artifact 可以升级为可执行变更？
- 本地 workspace 和注册表映射如何将目标 repository 身份解析为机器本地路径？
- 哪些生命周期命令应拒绝、移交给 repository 本地变更，或直接针对已解析的目标操作？
- 命令和 skill 输出应如何教导 agent 信任 CLI 报告的路径、编辑根目录和后续命令？

通过/不通过标准：

```text
在 create/link、show/status/list/instructions、validate、apply、archive、
spec sync、workspace resolution、generated skills 和 JSON output 都共享
一个目标解析模型之前，不要实现倡议托管可执行变更。
```
