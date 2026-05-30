# 工作区重新实现路线图

此变更是跨多个会话和分支重新实现工作区支持的连续性层。

## 当前状态

此路线图是历史性的，已被 `openspec/initiatives/context-store-and-initiatives/` 重新定义。新智能体应使用倡议方向作为产品权威，并将此路线图用作 POC 教训和保留的本地视图行为的参考。

保留：

- 工作区 setup、link、relink、list、open、update 和 doctor
- 链接的仓库和文件夹作为本地规划上下文
- 工作区本地技能作为本地智能体指导
- POC 仅作为研究材料

取代：

- 工作区作为持久的共享规划家园
- 工作区级别规划 artifact 作为规范的跨仓库计划
- 工作区 change planning 作为长期可信源

推迟：

- 工作区 apply、verify 和 archive 作为头等生命周期命令
- 分支/工作树编排、强跨仓库验证和依赖图强制执行

除非后续的倡议链接仓库变更设计明确重新激活，否则不要从此路线图中接取下一个未完成的扁平同级变更。

新智能体的根入口点：`START_HERE.md`。

此历史路线图正在实现的用户旅程是：

```text
创建工作区
  -> 添加仓库
  -> 使用智能体上下文打开工作区
  -> 规划跨仓库变更
  -> 实现一个仓库切片
  -> 验证并归档
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

`workspace-foundation` 建立了存储、根检测和命名模型。每个后续切片应基于该模型构建，而不是重新定义工作区元数据。

`workspace-create-and-register-repos` 创建工作区并使链接的仓库或文件夹在 change 存在之前可见。链接项可以是完整仓库、monorepo 模块或仅规划文件夹。这保留了产品规则：工作区可见性不是变更承诺。

`workspace-open-agent-context` 向智能体提供工作区位置、链接的仓库或文件夹、活跃的 change 和选定的 change 范围。

`workspace-change-planning` 创建了 beta 工作区级别规划承诺并识别了目标仓库切片。在倡议方向下，此模型是遗留或过渡性的，而非持久的共享计划。

`workspace-agent-guidance` 使工作区本地工作流技能有意识地使用规划模型：检查链接的上下文，以目标和已知受影响区域播种工作区变更，并将链接的仓库保留为只读规划上下文，直到 apply 选择编辑根目录。

`workspace-apply-repo-slice` 推迟到倡议链接的仓库本地 change 定义实现交接时。

`workspace-verify-and-archive` 推迟到倡议状态和链接的仓库本地 change 生命周期存在时。

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
参考材料。保留有用的本地视图工作区行为，但不要在倡议链接的
仓库本地 change 存在之前实现工作区 apply、verify 或 archive。
```

## 分支指导

每个同级变更可以在其自己的分支或 PR 上实现。将对后续切片有影响的决策记录在此 README 或相关的 proposal 中，以便未来会话不依赖于聊天历史。
