# workspace 重新实现路线图

此变更是跨多个会话和分支重新实现 workspace 支持的连续性层。

## 当前状态

此路线图是历史性的，已被 `openspec/initiatives/context-store-and-initiatives/` 重新定义。新智能体应使用倡议方向作为产品权威，并将此路线图用作 POC 教训和保留的本地视图行为的参考。

保留：

- workspace setup、link、relink、list、open、update 和 doctor
- 链接的 repository 和文件夹作为本地 planning 上下文
- workspace 本地 skill 作为本地智能体指导
- POC 仅作为研究材料

取代：

- workspace 作为持久的共享 planning 家园
- workspace 级别 planning artifact 作为 spec 的跨 repository 计划
- workspace change planning 作为长期可信源

推迟：

- workspace apply、verify 和 archive 作为头等生命周期命令
- 分支/工作树编排、强跨 repository 验证和依赖图强制执行

除非后续的倡议链接 repository 变更设计明确重新激活，否则不要从此路线图中接取下一个未完成的扁平同级变更。

新智能体的根入口点：`START_HERE.md`。

此历史路线图正在实现的用户旅程是：

```text
创建 workspace
 -> 添加 repository
 -> 使用智能体上下文打开 workspace
 -> planning 跨 repository 变更
 -> 实现一个 repository 切片
 -> 验证并 archive
```

POC 分支仅为参考材料：

```text
workspace-poc @ 79a45ac043f414e63d13e08b9da83b135cb20a39
```

使用它来理解行为、测试和经验教训。不要将其合并或默认保留其架构。该分支的完整源方向文档已记录在 `HISTORICAL_DIRECTION.md` 中。

新智能体在实现任何切片之前应阅读 `POC_REFERENCE_GUIDE.md`。该指南解释了如何检查固定的 POC 提交、为每个切片读取哪些文件，以及将哪些发现带回 OpenSpec artifact。

## 历史变更顺序

原始扁平同级变更为：

1. `workspace-foundation`
2. `workspace-create-and-register-repos`
3. `workspace-open-agent-context`
4. `workspace-change-planning`
5. `workspace-agent-guidance`
6. `workspace-apply-repo-slice`
7. `workspace-verify-and-archive`

OpenSpec 目前将活跃的 change 发现为 `openspec/changes/` 下的直接子目录，change 名称是 kebab-case 标识符。这些变更仍然是有用的参考 artifact，但它们不再是直接的实现队列。

## 依赖说明

`workspace-foundation` 建立了存储、根检测和命名模型。每个后续切片应基于该模型构建，而不是重新定义 workspace 元数据。

`workspace-create-and-register-repos` 创建 workspace 并使链接的 repository 或文件夹在 change 存在之前可见。链接项可以是完整 repository、monorepo 模块或仅 planning 文件夹。这保留了产品规则：workspace 可见性不是变更承诺。

`workspace-open-agent-context` 向智能体提供 workspace 位置、链接的 repository 或文件夹、活跃的 change 和选定的 change 范围。

`workspace-change-planning` 创建了 beta workspace 级别 planning 承诺并识别了目标 repository 切片。在倡议方向下，此模型是遗留或过渡性的，而非持久的共享计划。

`workspace-agent-guidance` 使 workspace 本地 workflow skill 有意识地使用 planning 模型：检查链接的上下文，以目标和已知受影响区域播种 workspace 变更，并将链接的 repository 保留为只读 planning 上下文，直到 apply 选择编辑根目录。

`workspace-apply-repo-slice` 推迟到倡议链接的 repository 本地 change 定义实现交接时。

`workspace-verify-and-archive` 推迟到倡议状态和链接的 repository 本地 change 生命周期存在时。

## 会话交接提示

在未来的实现会话开始时使用此提示：

```text
继续 context-store-and-initiatives 方向。首先阅读
openspec/initiatives/context-store-and-initiatives/direction.md 和
openspec/initiatives/context-store-and-initiatives/roadmap.md。使用
openspec/changes/workspace-reimplementation-roadmap/START_HERE.md、
openspec/changes/workspace-reimplementation-roadmap/README.md、
openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md、
openspec/changes/workspace-reimplementation-roadmap/POC_REFERENCE_GUIDE.md 以及
workspace-poc at 79a45ac043f414e63d13e08b9da83b135cb20a39 仅作为历史
参考材料。保留有用的本地视图 workspace 行为，但不要在倡议链接的
repository 本地 change 存在之前实现 workspace apply、verify 或 archive。
```

## 分支指导

每个同级变更可以在其自己的分支或 PR 上实现。将对后续切片有影响的决策记录在此 README 或相关的 proposal 中，以便未来会话不依赖于聊天历史。
