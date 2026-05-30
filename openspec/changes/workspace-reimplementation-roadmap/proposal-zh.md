## 为什么

workspace 支持需要重新实现为用户可见的 workflow，而不是作为概念验证的直接移植继续推进。

状态：此路线图现在是历史参考。活跃的产品方向是 context-store-and-initiatives 倡议，其中倡议协调持久的跨 repository 工作，workspace 打开本地视图，repository 本地 change 拥有实现。保留 workspace setup/open/update/doctor 基础设施，但在存在倡议链接的 repository 本地 change 之前，不要将 workspace apply、verify 或 archive 视为下一个发布序列。

用户应该能够说他们有一个多 repository 产品目标，创建 workspace，添加相关 repository，用智能体打开该 workspace，planning 变更，一次实现一个 repository 切片，验证它并 archive 它。POC 分支捕获了有用的行为和发现，但其实现应保持为参考材料而非基础架构。

此路线图还需要在多个会话和分支中存活。当前 OpenSpec change 发现将活跃 change 视为 `openspec/changes/` 下的扁平直接子目录，change 名称是 kebab-case 标识符而非嵌套路径。因此，此变更是一个扁平的 planning 容器，包含同级 proposal 变更，而非嵌套子变更。

参考材料：

- `workspace-poc` at `79a45ac043f414e63d13e08b9da83b135cb20a39`
- 该分支上的 `WORKSPACE_REIMPLEMENTATION_DIRECTION.md`
- 该分支上的 `WORKSPACE_POC_FOLLOWUP_NOTES.md`

## 变更内容

添加一个轻量级路线图，将 workspace 支持重新实现为一组扁平的 OpenSpec 同级变更：

- `workspace-foundation`
- `workspace-create-and-register-repos`
- `workspace-open-agent-context`
- `workspace-change-planning`
- `workspace-agent-guidance`
- `workspace-apply-repo-slice`
- `workspace-verify-and-archive`

每个同级变更拥有实际用户旅程中的一个步骤。依赖关系目前记录在 proposal 散文中。当变更堆叠元数据落地时，此路线图可以迁移到显式的 `parent` 和 `dependsOn` 元数据。

预期顺序为：

```text
workspace-foundation
 -> workspace-create-and-register-repos
 -> workspace-open-agent-context
 -> workspace-change-planning
 -> workspace-agent-guidance
 -> workspace-apply-repo-slice
 -> workspace-verify-and-archive
```

## 能力

### 新能力

- `workspace-reimplementation-roadmap`：协调跨多个扁平 OpenSpec 变更的 workspace 重新实现计划。

### 修改的能力

- `openspec-conventions`：澄清此 workspace 工作在嵌套或堆叠变更元数据受支持之前使用扁平同级变更。

## 影响

- 此 PR 中仅为 planning。
- 未来的变更将影响 workspace 元数据、workspace CLI 流程、智能体上下文构建、workspace change planning、workspace 本地智能体指导、repository 切片应用、验证和 archive 行为。
- 此路线图 proposal 不引入任何运行时行为变更。
