# 上下文存储项目根与 Schema 驱动的倡议

## 状态

根据手动 beta 测试实际情况提出。

此工作项将当前的"倡议创建写入完整的硬编码六文件包"模型替换为类似项目的上下文存储根和迭代的、schema 驱动的倡议产物流程。

## 真实依据

从 `../../direction.md` 开始，并保留当前边界：

```text
上下文存储同步真实信息。
集合塑造真实信息。
倡议协调工作。
workspace 打开本地视图。
变更实现 repository 拥有的切片。
```

手动 beta 测试证据：agent 可以创建当前的 MVP 倡议形态，但生成的 `requirements.md`、`design.md`、`decisions.md`、`questions.md` 和 `tasks.md` 会引发过早的、未经审阅的 planning 内容。

## 为何存在

`openspec initiative create` 当前从硬编码的 TypeScript 常量和 `TBD` template 创建看起来完整的 planning 包。这使 MVP 具象化，但对于真实的倡议工作来说，它是错误的默认行为。

倡议是面向 PM、设计师、架构师和 agent 的高级共享 planning 界面。它们应捕获意图、已审阅的需求、设计方向、待解决的问题和决策，随着这些产物变得真实而记录。它们不应仅仅因为文件夹存在就创建看起来已完成但实际上空白的或虚假的文档。

更广泛的产品形态是，上下文存储应像一个在 `openspec init` 之后的 repository 一样，感觉像一个 OpenSpec 根：它可以拥有本地 OpenSpec 配置和项目本地 schema。区别在于生命周期：上下文存储是共享的上下文根，而非实现 repository。

## 产品模型

`openspec init` 之后的 repository：

```text
repo/
 openspec/
 config.yaml
 schemas/
 changes/
 specs/
```

设置后的上下文存储：

```text
context-store/
 .openspec-store/
 store.yaml
 openspec/
 config.yaml
 schemas/
 initiatives/
```

上下文存储内的 `openspec/` 目录用于 OpenSpec 配置和 schema 解析。它本身不会使上下文存储成为可执行的实现 planning 家园。

## 目标

- 让上下文存储携带 OpenSpec 配置，包括默认的倡议 schema。
- 让上下文存储在 `openspec/schemas/` 下携带项目本地 schema。
- 将硬编码的倡议文件创建替换为 schema 驱动的产物模型。
- 使 `initiative create` 默认精简且安全。
- 让 agent 通过状态和指令输出一步一步地增长倡议产物。
- 保持现有的六文件 MVP 倡议可读。
- 保持 repository 本地变更作为默认的实现产物。

## 非目标

- 不要使上下文存储托管的可执行变更成为此切片的一部分。这仍然是 Item 18。
- 不要添加跨 repository 的 apply、archive、validation 或 spec-sync 编排。
- 不要使 workspace 本地产物成为共享 planning 的真实依据。
- 不要自动迁移现有倡议。
- 除非后续的 UX 决策明确选择，否则默认不要将 AI 工具运行时文件安装到上下文存储中。

## 默认倡议形态

新的倡议创建应创建一个外壳，而非整个计划：

```text
initiatives/<id>/
 initiative.yaml
 brief.md
```

`brief.md` 是一个种子文档，而非已审阅需求或设计的完成标记。它应包含标题、摘要和简短的"当前理解"章节，无 `TBD` 占位符。

已审阅的 planning 产物稍后通过倡议 schema 创建。

默认内置 schema，概念上：

```yaml
name: product-initiative
version: 1
description: 面向 PM、设计师、架构师和 agent 的高级倡议 planning
usage: initiative
artifacts:
 - id: requirements
 generates: requirements.md
 description: 产品意图、目标、非目标、需求和待解决的问题
 template: requirements.md
 requires: []

 - id: design
 generates: design.md
 description: 产品、UX 和架构方向，包含约束和权衡
 template: design.md
 requires:
 - requirements
```

不要在默认倡议 schema 中包含 `tasks.md`。实现任务属于 repository 本地变更。协调任务、workflow、决策日志和问题日志可以是单独的后备 schema 或显式产物，等待使用 schema 更加清晰后再行添加。

## UX 方向

存储设置应使存储具有足够的项目特性以支持 schema：

```bash
openspec context-store setup team-context --init-git
```

预期创建的形态：

```text
team-context/
 .openspec-store/store.yaml
 openspec/config.yaml
 initiatives/
```

首选的配置方向：

```yaml
initiative_schema: product-initiative
```

这避免重载现有 repository 本地的 `schema` 字段（当前含义为"默认变更 schema"）。如果实现选择复用 `schema`，文档和 JSON 输出必须显式说明上下文存储的作用域。

然后倡议创建保持小巧：

```bash
openspec initiative create agent-trace-hooks \
 --store team-context \
 --title "Agent Trace Hooks" \
 --summary "探索轻量级捕获 agent 跟踪事件和钩子结果。"
```

预期的下一步操作：

```bash
openspec initiative status team-context/agent-trace-hooks --json
openspec initiative instructions requirements team-context/agent-trace-hooks --json
```

agent 仅在对话中有足够已审阅内容时才编写 `requirements.md`。`design.md` 在需求存在后变得就绪。

## 技术方法

重用产物图原语，但添加倡议特定的加载器，而不是强制倡议通过 `loadChangeContext`。

当前可重用的部分：

- `src/core/artifact-graph/graph.ts`
- `src/core/artifact-graph/state.ts`
- `src/core/artifact-graph/outputs.ts`
- `src/core/artifact-graph/resolver.ts`
- `src/core/artifact-graph/instruction-loader.ts` template 加载
- `src/core/project-config.ts`

新的倡议特定部分：

- 一个上下文存储 OpenSpec 根辅助工具，将存储根视为 `projectRoot` 用于配置和 schema 查找
- 一个以 `context-store/initiatives/<id>/` 为根的倡议产物上下文加载器
- 镜像 repository 本地产物 workflow 但返回倡议特定字段的倡议 `status` 和 `instructions` 命令
- 一个仅写入 `initiative.yaml` 和 `brief.md` 的精简 `initiative create` 路径

不要不修改地使用现有的 repository planning 家园解析器。一旦上下文存储包含 `openspec/config.yaml`，当前的"最近的 `openspec/` 文件夹意味着 repository planning 家园"启发式方法可能意外使上下文存储看起来像实现 repository。此项工作必须：

- 教导 planning 家园解析检测 `.openspec-store/store.yaml`，并为实现命令返回或拒绝"上下文存储"类型，或
- 显式拒绝从上下文存储根运行 `openspec new change`，直到 Item 15 定义了目标绑定的可执行变更。

## Schema 与配置兼容性

优先选择下一版本安全的配置路径：

- 将 `initiative_schema` 添加到项目配置，或等效的集合特定配置字段。
- 继续使用现有的 `schema` 作为默认的 repository 本地变更 schema。
- 如有需要，在现有 `metadata` 中存储每个倡议的 schema 覆盖。
- 避免向 `initiative.yaml` 添加新的顶层 `schema` 字段，直到倡议元数据版本化被设计。

原因：`initiative.yaml` 当前是严格的，且版本化为 `version: 1`。添加顶层字段会使旧的 CLI 拒绝新的倡议。现有的 `metadata` 可以携带向前兼容的字段而不破坏旧的读取器。

Schema 命名空间需要一个显式决策：

- 要么向 schema 文件添加 `usage: change | initiative` 鉴别器并相应过滤命令，或
- 在复用相同产物图格式的同时使用单独的倡议 schema 命名空间。

最简单的面向用户模型仍然是 `openspec/schemas/`，但命令必须避免将 `product-initiative` 列为有效的 repository 本地变更 workflow。

## JSON 契约

`initiative create --json` 应报告外壳和下一步操作：

```json
{
 "context_store": {
 "id": "team-context",
 "root": "/path/to/store"
 },
 "initiative": {
 "id": "agent-trace-hooks",
 "root": "/path/to/store/initiatives/agent-trace-hooks",
 "metadata_path": "/path/to/store/initiatives/agent-trace-hooks/initiative.yaml",
 "schema": "product-initiative"
 },
 "created_files": [
 "initiative.yaml",
 "brief.md"
 ],
 "next_commands": {
 "status": "openspec initiative status team-context/agent-trace-hooks --json",
 "requirements": "openspec initiative instructions requirements team-context/agent-trace-hooks --json"
 },
 "status": []
}
```

`initiative status --json` 应包含：

- 上下文存储标识和根
- 倡议标识、根、元数据路径和选定的 schema
- 按产物 id 键化的产物路径
- 产物状态：`done`、`ready`、`blocked`
- 后续步骤
- 声明此为共享 planning 上下文而非可编辑实现目标的操作上下文

`initiative instructions --json` 应包含：

- 解析后的输出路径
- 现有的输出路径
- schema 指令
- template 内容
- 依赖关系和解锁条件
- 存储配置上下文/规则（如支持）

## 发布风险与迁移

如果作为精简的、叠加的层级实现，这是兼容的：

- 现有的六文件倡议仍然可读，因为列表/显示仅需要 `initiative.yaml`。
- 现有的可选 Markdown 文件可以保留在旧的倡议文件夹中。
- 新的状态/指令可以忽略选定 schema 之外的文件。
- 如果 schema 数据保留在 `metadata` 或存储配置中而非新的严格顶层字段，旧的 CLI 仍然可以读取新的倡议。

高风险区域：

- 上下文存储获得 `openspec/config.yaml` 后的 planning 家园检测。
- 断言六文件 MVP 倡议形态的测试和文档。
- 如果倡议 schema 与变更 schema 共享相同命名空间，schema 列表和自动补全。
- 仍然告诉 agent 在创建后编辑每个生成的倡议 Markdown 文件的 agent 指导。

## 测试与文档接触点

可能需要更新或添加的测试：

- `test/core/collections/initiatives/schema.test.ts`
- `test/core/collections/initiatives/templates.test.ts`
- `test/core/collections/initiatives/operations.test.ts`
- `test/commands/initiative.test.ts`
- `test/commands/context-store.test.ts`
- `test/commands/artifact-workflow.test.ts`
- 具有 `openspec/config.yaml` 的上下文存储根的 planning 家园测试
- 如果添加了 schema 使用过滤，schema 列出/补全测试

可能需要更新的文档：

- `docs/workspaces-beta/agent-cli-playbook.md`
- `docs/workspaces-beta/user-guide.md`
- `docs/cli.md`
- 如果添加了 `usage` 或 `initiative_schema`，schema 文档
- `openspec/initiatives/context-store-and-initiatives/work-items/05-ship-initiative-mvp/` 附带说明 MVP 形态已被此工作项取代

## 完成条件

- 新的上下文存储拥有 OpenSpec 配置，并且可以解析项目本地的倡议 schema。
- `initiative create` 仅创建精简的倡议外壳。
- agent 可以使用倡议状态/指令迭代地创建高级 planning 产物。
- `openspec new change` 不会仅因为存储有 `openspec/config.yaml` 而将上下文存储误认为是普通的实现 repository。
- 现有的 MVP 倡议继续可以列出和显示。
- 文档将倡议产物描述为已审阅的、迭代的上下文，而非需要立即填写的文件。
