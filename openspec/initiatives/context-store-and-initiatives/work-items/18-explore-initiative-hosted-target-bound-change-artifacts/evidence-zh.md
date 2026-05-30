# 探索倡议托管的目标绑定变更工件——证据

## 初步研究笔记

- 当前产品方向表明上下文存储同步共享事实，倡议协调工作，仓库本地变更拥有实现规划。
- 路线图第 8 项目前假设仓库本地变更链接到倡议。
- 现有的规划家园行为区分了仓库本地和 workspace 规划家园，但没有上下文存储支持的变更家园。
- 新的工件工作流命令已在某些地方消费已解析的规划路径，这可能成为未来变更家园解析的有用接缝。
- 较旧的命令界面仍然假设本地 OpenSpec 项目下的 `openspec/changes/`，并且在进行任何实现切片之前需要显式审计。

## 初步框架

可配置的变更家园是一个产品边界问题，而不仅仅是路径变更。上下文存储托管的工件在验证、应用、归档或规范同步可以安全运行之前，仍然需要明确的目标仓库或规范根目录。

未来的探索应保留"变更家园"作为内部解析器语言，并围绕倡议托管的规划工件、目标绑定变更、实现目标和可编辑根目录使用更清晰的产品语言。

## 代理优先团队 UX 研究

日期：2026-05-23。

探索的问题：

```text
对于使用上下文存储、倡议、workspace 和仓库本地变更的团队来说，
出色的代理优先开发者体验是什么样的？
```

### 外部模式笔记

- Linear 将倡议用作更高级别的协调对象，对项目进行分组并展示健康状态、所有权和活跃项目汇总。
- Jira 规划通常在多团队规划中，在史诗或其他子工作项之上使用倡议。
- GitLab 路线图展示跨组或项目的更高级别史诗和里程碑。
- GitHub Projects 强调与问题和仓库工作保持连接的灵活规划。

这些模式指向一种常见的划分：

```text
更高级别对象 = 协调和汇总
执行项       = 更接近团队、项目、仓库或问题拥有的工作
```

OpenSpec 应保持这种分离，同时使代理交接比人类项目管理工具更精确。

### 清晰的思维模型

来自研究的最强思维模型：

```text
倡议     = 共享的协调事实
Workspace = 倡议 + 仓库之上的本地视角
仓库变更   = 可执行的实现计划
```

扩展的产品规则：

```text
上下文存储记住。
倡议协调。
Workspace 打开。
仓库本地变更实现。
```

关键不变性：

```text
工作身份不是存储位置。
存储位置不是编辑权限。
```

这为代理保持三个决策的分离：

- 用户在谈论什么工作？
- 规划工件应存放在哪里？
- 现在可以编辑哪些文件或仓库？

### 建议的工件类型

仓库上下文：

```text
openspec/changes/<change-id>/
```

用于仓库拥有的实现计划。仓库本地变更可以通过可移植元数据引用倡议：

```yaml
initiative:
  store: platform
  id: billing-launch
```

Workspace 上下文：

```text
<store>/initiatives/<initiative-id>/work-items/<work-id>/
```

用于在仓库所有权或实现目标明确之前的共享倡议规划。这些应称为倡议工作项、规划简报或提案，而不是可执行的 OpenSpec 变更，直到第 18 项为上下文存储支持的变更定义完整生命周期。

Workspace 本地变更：

```text
<workspace>/changes/<change-id>/
```

保留作为遗留或测试版兼容性，除非用户显式选择 workspace 规划流程。

### 代理优先 UX 场景

单一仓库团队：

- 用户要求代理从仓库内部创建提案。
- 代理解析倡议（如果已命名）。
- 代理创建一个链接到该倡议的仓库本地变更。
- Apply、validate、sync 和 archive 保持仓库本地。

单体仓库：

- 一个仓库本地变更可以覆盖多个包或能力。
- 代理可能需要领域或包的提示。
- 仓库仍然是实现所有者；领域澄清范围但不成为单独的变更家园。

多仓库平台：

- Workspace 打开共享的倡议上下文加上本地仓库克隆。
- 倡议协调平台成果。
- 当实现所有权已知时，每个拥有仓库获得自己的链接仓库本地变更。
- Workspace 状态应报告可用的本地仓库、缺失的本地路径和编辑边界。

中央架构团队：

- 架构师可以更新倡议需求、设计、契约、决策和问题，而不拥有实现。
- 代理应提供起草共享倡议上下文或在创建仓库本地变更之前询问拥有仓库的选项。

所有权未知：

- 代理不应创建实现变更。
- 它应添加或更新倡议级别的问题，或返回目标选项并请求仓库或领域决策。

队友入职：

```text
克隆或注册上下文存储。
运行 context-store doctor。
打开或解析倡议。
通过 workspace 映射链接本地仓库。
要求代理从倡议继续。
```

### 理想的代理 JSON 块

代理需要跨 create、status、instructions、resolve 和 list 的稳定路由词汇：

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

- `workTarget`：代理正在操作的对象。
- `initiativeLink`：规范的共享协调上下文（如果存在）。
- `invocationContext`：命令运行的位置。
- `actionContext`：代理可以编辑什么。
- `nextCommands`：代理应运行的后续命令，而不是自行发明路径。

### 生命周期规则

- 当仓库是允许的编辑根目录时，仓库本地变更是实现就绪的。
- 倡议工作项在它们选择或链接仓库本地实现变更之前仅用于规划。
- Workspace 本地变更是兼容性工件，不是首选的新共享规划模型。
- Apply、archive、repo spec sync 和 repo delta validation 应保持仓库本地，直到上下文存储支持的变更生命周期被显式设计。
- 如果 `allowedEditRoots` 为空或需要目标选择，代理应在编辑实现文件之前停止。

### 需要设计的边界情况

- 相同倡议 ID 存在于多个存储中。
- 某些注册的存储不可读或不同步。
- 一个 workspace 可以看到仓库路径，但用户尚未将其选择为编辑目标。
- 终端在 workspace 内部，但计划的工作属于一个链接的仓库。
- 终端在一个链接的仓库内部，但用户首先想要共享的倡议规划。
- 一个仓库本地变更引用了当前机器上未注册的倡议存储。
- 一个上下文存储工作项使用了另一位队友没有的 schema。
- 一个变更 ID 同时作为仓库本地变更和倡议工作项存在。
- 一个中央团队编辑倡议上下文，而实现团队编辑链接的仓库本地变更。

### 研究的建议方向

保持第 8 项范围狭窄：

- 向仓库本地变更添加倡议元数据。
- 添加 `new change <id> --initiative <store>/<initiative> --json`。
- 使用 `initiative show` 加上 workspace/仓库上下文作为代理交接骨干。
- 在第 8 项中不实现上下文存储支持的 OpenSpec 变更。

使用第 18 项决定更大的模型：

- 倡议工作项是否应成为一级工件。
- "变更家园"是否保持为内部语言。
- 上下文存储托管的工作如何绑定到仓库目标、规范、验证、应用、归档和同步。
- 技能和生成的指导如何教导代理信任 CLI JSON 而不是硬编码路径或当前工作目录假设。

## 目标绑定重构子代理

日期：2026-05-23。

探索的问题：

```text
鉴于中央与仓库本地变更存储之间的产品张力，第 18 项在实现工作开始前应如何重构？
```

三个子代理从产品语义、代理优先 UX 和生命周期/实现角度审查了第 18 项。

### 产品语义发现

- 可见的工作项不应被框架化为通用的可配置存储。那会使困难的问题听起来像路径管道。
- 更精确的产品问题是：倡议托管的工件在绑定到目标仓库或规范根目录后，能否成为可执行的 OpenSpec 变更。
- 仓库本地变更仍然是默认的可执行实现工件。
- 倡议托管的工件从仅规划的工作项、简报或提案开始。
- "变更家园"可以保持为内部解析器语言，但不应是主要的面向用户概念。

建议的命名：

```text
探索倡议托管的目标绑定变更工件
```

### 代理优先 UX 发现

代理需要稳定的 CLI 输出，将工件与代理可以编辑的内容分开：

```text
计划位于：仓库本地 OpenSpec | 倡议上下文
可编辑目标：选定的仓库路径 | 尚无
链接的倡议：platform/billing-launch
```

命令应报告结构化的操作上下文，而不是让生成的技能推断路径：

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

如果 `allowedEditRoots` 为空，代理应在编辑实现文件之前停止。如果需要目标选择，命令应返回后续步骤选项，而不是静默创建模糊的实现变更。

### 生命周期和实现发现

本地代码仍然有强烈的仓库本地假设：

- `src/core/planning-home.ts` 将规划家园建模为 `repo | workspace`。
- `src/commands/workflow/new-change.ts` 从当前规划家园解析存储，尚未暴露 `--initiative` 或 `--json`。
- `src/commands/validate.ts` 从 `process.cwd()/openspec/...` 验证变更和规范。
- `src/core/archive.ts` 通过读取 `openspec/changes`、将增量应用到 `openspec/specs` 并将变更移入 `openspec/changes/archive` 来进行归档。
- `src/core/artifact-graph/types.ts` 元数据尚未建模倡议链接、目标仓库身份、工件家园或编辑边界。
- 生成的技能和工作流模板仍然包含仓库本地路径假设，如 `openspec/changes/<name>/`。

这些在当前仓库本地模型中不是 bug。它们是倡议托管的可执行变更是生命周期设计而不是小型路径开关的证据。

### 更新的建议

保持第 8 项范围狭窄：

- 创建或链接带有倡议元数据的仓库本地变更。
- 为代理交接添加 JSON 输出。
- 在第 8 项中不实现上下文存储托管可执行变更。

使用第 18 项回答更大的问题：

- 在实现目标已知之前存在什么倡议托管工件？
- 什么目标元数据让共享工件可以升级为可执行变更？
- 本地 workspace 和注册表映射如何将目标仓库身份解析为机器本地路径？
- 哪些生命周期命令应拒绝、移交给仓库本地变更，或直接针对已解析的目标操作？
- 命令和技能输出应如何教导代理信任 CLI 报告的路径、编辑根目录和后续命令？

通过/不通过标准：

```text
在 create/link、show/status/list/instructions、validate、apply、archive、
spec sync、workspace resolution、generated skills 和 JSON output 都共享
一个目标解析模型之前，不要实现倡议托管可执行变更。
```
