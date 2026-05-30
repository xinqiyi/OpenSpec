# 上下文存储与计划方案方向

本文档记录了工作空间/计划方案讨论中提出的建议方向。主要的转变是"工作空间"不应再作为持久的共享 planning 对象。持久的共享对象是同步的上下文存储，而计划方案是其中的一个定制集合。

## 核心模型

```text
Context Store
 = synced shared content container

Collection
 = mounted content system inside a store

Initiatives
 = first major collection for cross-team implementation context

Workspace
 = local working view over context stores and repos

Change
 = repo/team-owned implementation plan
```

清晰规则：

```text
Context stores sync truth.
Collections shape truth.
Initiatives coordinate work.
Workspaces open local views.
Changes implement repo-owned slices.
```

## 锁定产品边界

工作空间到计划方案的转变现已成为未来协调工作的产品边界：

- 工作空间是可重新生成的、本机本地的工作视图。它映射上下文存储、计划方案、项目、repository 和文件夹到当前用户可以打开的路径。
- 上下文存储是共享文件的持久同步容器。
- 计划方案是跨团队或跨 repository 实现上下文的持久协调对象。
- repository 本地变更仍然是执行工作的 repository 或团队拥有的实现计划。

这取代了旧模型中工作空间级别的 `changes/` 树拥有跨 repository 工作的 spec 共享计划。现有的工作空间 planning 行为可以作为 Beta 或遗留基础设施保留，但不应指导新的生命周期设计。

工作空间路线图处理：

- 保留 setup、link、relink、list、open、update 和 doctor。
- 保留链接的 repository 和文件夹可见，以便在变更存在之前进行探索。
- 保留工作空间本地 agent 指南作为本地视图设置，由 `workspace update` 刷新。
- 推迟工作空间的 apply、verify 和 archive，直到计划方案可以链接到 repository 拥有的 OpenSpec 变更。
- 推迟分支/工作树编排、多 repository apply、强跨 repository 验证和依赖图强制执行。

## agent 优先用户体验

计划方案的主要用户体验预计是 agent 驱动的：

```text
Using initiative billing-launch, explore the API work and create a proposal.
```

用户不需要知道每个命令。OpenSpec 应暴露小的、结构化的 CLI 原语，供 agent 用于：

- 在已注册的上下文存储中找到目标计划方案
- 从上下文存储读取 spec 的计划方案文件
- 创建或链接 repository 本地的 OpenSpec 变更
- 使用工作空间状态获取本地 repository 和文件夹视图
- 尊重编辑边界，而不是将每个打开的文件夹视为可编辑

因此，CLI 是 agent 的工具界面，而不是完整的用户 workflow。作为第一个切片，优先选择显式的、机器可读的命令，如 `initiative show --json`、`new change --initiative ...` 和工作空间本地视图命令，而非宽泛的交互式流程。

spec 的计划方案上下文应保留在上下文存储中。repository 本地变更应引用计划方案，而不是检入计划方案内容的复制快照。如果 agent 需要紧凑的上下文包，OpenSpec 可以从实时计划方案上下文中生成作为命令输出的内容。

## 上下文存储

上下文存储是共享/同步的文件文件夹。它与内容无关。它不需要知道什么是计划方案。

示例：

```text
acme-context/
 initiatives/
 decisions/
 api-catalog/
 playbooks/
```

第一个后端应为 Git：

```text
create/update/delete files
 -> commit
 -> push
 -> other users pull
 -> local views update
```

但应用程序应通过存储抽象与后端交互，而不是直接与 Git 交互，以便后端以后可以演变为云数据库。

## 后端

后端为上下文存储提供持久化和同步。

示例：

- `git` 后端：本地克隆、pull、commit、push、watch
- `cloud` 后端：数据库记录、订阅、托管同步
- `memory` 后端：测试和本地原型

后端应暴露通用的文件/对象操作：

```text
read
write
delete
list
sync
watch
```

它不应包含计划方案特定的行为。

## 集合

集合是上下文存储内部挂载的内容系统。它类似于插件，但"集合"是面向用户的术语。

每个集合拥有：

- 文件夹命名空间
- 内容模型
- template
- 验证/规则
- 可选的 agent 指南
- 可选的 UI 视图

示例：

```text
context-store/
 initiatives/ # Initiative collection
 decisions/ # Decision collection
 api-catalog/ # API catalog collection
```

核心应强制集合只能在其挂载内写入。

## 计划方案集合

计划方案集合是第一个面向企业的集合。

计划方案是共享的、agent 可消费的实现上下文，用于协调的成果。它可以跨越团队、repository、服务、API、合约和能力。

默认结构：

```text
initiatives/
 launch-billing-flow/
 initiative.yaml
 requirements.md
 design.md
 contracts/
 decisions.md
 questions.md
 tasks.md
```

这描述了上下文存储中运行时计划方案集合的结构。此路线图文件夹可能仍然包含旧的 `.initiative.yaml` 进度元数据，而计划方案本身正被用于管理迁移；该旧追踪器不是新的上下文存储计划方案应复制的模型。

默认结构应为企业设计合作定制化，但集合系统应允许以后的其他结构。

## 计划方案职责

计划方案应拥有与实现相关的共享上下文：

- 产品/项目意图
- 已采纳的需求
- 高级技术协调
- 能力和所有权映射
- API/事件/schema 合约
- 依赖假设
- 决策和开放问题
- 工作空间可读的上下文，用于 repository 本地实现工作

计划方案不应试图成为 Jira 或 Confluence 的全部替代。聚焦定位是：

```text
OpenSpec 存储约定的实现上下文。
Jira 追踪工作。
Confluence 存储宽泛的文章。
GitHub/GitLab 存储代码。
```

## 计划方案与变更范围

一个计划方案可以跨越一个或多个 OpenSpec 变更。

这些变更可以位于：

- 与计划方案相同的 repository 中
- 不同的 repository 中
- 以后在多个上下文存储或 OpenSpec 根目录中

计划方案存储共享的协调上下文。工作空间视图可以将该上下文与本地 repository 和 repository 拥有的变更关联起来，而无需将计划方案存储与本机检出链接关联。

这使得分组与存储分离：

```text
Initiative = shared grouping/context
Change = execution artifact
Workspace = local opened view of initiative + repos
```

## 工作空间

工作空间是本地工作视图，不是真相来源。

它可以映射上下文存储和项目标识符到本地路径，配置开启器，并启动编码 agent，使其能够看到正确的文件夹。

工作空间可以通过解析以下内容来打开一个计划方案：

- 计划方案的上下文存储
- 本地选择的 repository 本地变更
- 参与 repository 的本地检出路径

持久的工作空间记录应保持小巧和私有。它记录本次运行时的本地视图选择，而不是生成的 agent 文件或共享的计划方案内容。

```text
getGlobalDataDir()/workspaces/<workspace-name>/
 workspace.yaml
```

工作空间名称是本地标识。工作空间记录可以选择性地存储选定的上下文存储和计划方案，以及到本地路径和开启器偏好的稳定链接名称。计划方案引用是记录内的数据，而不是路径段。

打开工作空间会在管理工作空间根目录下物化开启器特定的运行时文件。这些文件可以包含生成的 agent 指南、skill 和编辑器工作空间文件。机器可读的上下文通过 JSON 命令输出返回。这些是重新生成的本地支持，不是真相来源。

```text
private local view record
 -> generated runtime files
 -> opener-specific launch
 -> initiative context + selected local repos/folders
```

工作空间应可重新生成且特定于运行时。它们不应是计划方案内容、检入的协作状态、分支、工作树、克隆或实现进度的 spec 归属。

## repository 变更

repository 本地变更仍然是团队拥有的实现计划。

工程团队应能够将相关的计划方案上下文拉入 repository 并创建链接的 OpenSpec 变更。

示例：

```text
repo/
 openspec/
 changes/
 add-billing-api/
 .openspec.yaml
 proposal.md
 design.md
 specs/
 tasks.md
```

本地变更应在元数据中引用计划方案，例如：

```yaml
initiative:
 store: platform
 id: billing-launch
```

此元数据是持久的 repository 上下文，应被检入。它不应包含机器本地路径。当 agent 需要共享上下文时，应从已注册的上下文存储中读取计划方案的 spec 文件。

## 概念间的关系

```text
Context Store
 contains Collections

Collection
 defines structure/rules for a mounted folder

Initiative Collection
 defines initiatives/

Initiative
 coordinates one shared outcome

Workspace
 opens local views of context stores and repos

Repo Change
 implements one team's/repo's part of an initiative
```

端到端流程：

```text
Product/program/architect creates initiative
 -> initiative syncs through context store
 -> engineers open local workspace
 -> repo team pulls relevant initiative context
 -> repo team creates linked OpenSpec change
 -> repo team implements locally
 -> workspace view surfaces local progress alongside initiative context
```

## 本地 API 方向

应用程序应使用依赖注入：

```ts
const store = createStore({
 id: "acme-context",
 backend: gitBackend({
 remote: "git@github.com:acme/context.git",
 localPath: "~/.openspec/stores/acme-context",
 autoSync: true,
 }),
 collections: [
 initiativeCollection({ mount: "initiatives" }),
 ],
});
```

用法：

```ts
const initiatives = store.collection("initiatives");

await initiatives.create({ id: "launch-billing-flow" });
await initiatives.update("launch-billing-flow", patch);
await store.sync();
```

重要的分离：

```text
Git backend knows Git.
Store knows sync/lifecycle/events.
Collection knows content structure.
Initiative collection knows initiatives.
```

## UI 方向

UI 在核心层应与内容无关：

- 浏览文件夹/文件
- 编辑 Markdown/YAML
- 预览内容
- 搜索
- 显示差异/历史
- 同步状态

集合可以添加更丰富的视图：

- 计划方案状态视图
- 合约表格
- 所有者/依赖图
- 链接的 repository 变更视图

UI 应无论挂载了哪些集合都能正常工作。

## 开放问题

- 第一个具体的上下文存储命令界面是什么？
- 存储应该叫 `context`、`store`，还是更面向产品的名称？
- 企业上下文存储默认应位于何处：客户 GitHub、OpenSpec 管理的 Git，还是以后托管的云？
- 非技术用户如何编辑 Git 后端内容而不感受到 Git？
- 在冲突处理变得棘手之前，最小的自动同步行为是什么？
- 计划方案合约如何升级为 spec 的拥有者 repository 合约？
- 链接的 repository 变更如何向计划方案报告状态而不变成 Jira？
- monorepo 应该如何映射能力、文件夹和 repository 本地变更？
- 第一个 repository 变更链接命令应该叫什么？
- 链接变更存在后，哪些计划方案进度/状态信号是有用的？

## 建议的下一步方向

在初始存储、集合和计划方案创建/列出基础工作之后，按此顺序构建后续切片：

1. 围绕创建/列出、验证、template 以及显式推迟 read/update/delete 策略，协调计划方案 MVP。
2. 添加最小上下文存储用户体验，用于 setup、registration、listing 和 doctoring。
3. 添加 agent 优先的计划方案发现，使用 `initiative show --json` 和已注册存储查找。
4. 添加 repository 本地变更元数据和 agent 友好的 `--initiative` 创建/链接流程。
5. 拒绝独立的 `initiative resolve`；本地路径映射属于工作空间，不属于计划方案命令。
6. 一旦 show/link 语义存在，让工作空间可以打开计划方案感知的本地视图。
7. 添加本地到计划方案的上用户体验。
8. 在实际使用塑造需求后，强化团队共享协调、同步、冲突指导和进度状态。
