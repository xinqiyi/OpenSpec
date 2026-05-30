## 为什么

`generateApplyInstructions` 函数硬编码检查 `spec-driven` 的 artifact（`proposal.md`、`specs/`、`design.md`、`tasks.md`）。如果用户选择不同的 schema（如 `tdd`），apply 指令将毫无意义——它检查的是该 schema 中不存在的文件。

这阻碍了实验性 workflow 正确支持多个 schema。

## 变更内容

**范围：实验性 artifact workflow**（`openspec instructions apply`）

**依赖：** `add-per-change-schema-metadata`（用于了解变更使用哪个 schema）

- 使 `generateApplyInstructions` 从 schema 读取 artifact 定义
- 根据 schema 动态确定哪些 artifact 存在
- 定义变更何时变为"可实现"（参见下方设计决策）
- 生成适合 schema 的上下文文件和指令

## 设计决策：变更何时可被实现？

这是关键问题。不同的方案：

### 方案 A：在 schema 中显式声明 `apply` artifact

添加一个字段来标记哪个 artifact 是"实现门控"：

```yaml
artifacts:
 - id: tasks
 generates: tasks.md
 apply: true # ← 此 artifact 触发 apply schema
```

**优点：** 显式、灵活
**缺点：** 需要维护的额外字段，如果有多个 artifact 是 `apply: true` 怎么办？

### 方案 B：叶子 artifact 是可实现的

没有依赖项（无其他 artifact 依赖它们）的 artifact 是 apply 目标。

- `spec-driven`：`tasks` 是叶子 → apply = 执行任务
- `tdd`：`docs` 是叶子 → 但这对于 TDD 来说没有意义……

**优点：** 无需额外 schema 字段，从图中推导
**缺点：** 不符合 TDD 语义（实现是动作，而非文档）

### 方案 C：Schema 级别的 `apply_phase` 定义

在 schema 中添加一个顶级字段：

```yaml
name: spec-driven
apply_phase:
 requires: [tasks] # apply 之前必须存在
 tracks: tasks.md # 带有复选框的文件用于跟踪
 instruction: "完成任务，边做边标记完成"
```

```yaml
name: tdd
apply_phase:
 requires: [tests] # 实现前必须有测试
 tracks: null # 无复选框跟踪——只需让测试通过
 instruction: "运行测试，实现直到通过，重构"
```

**优点：** 完全灵活，schema 控制自己的 apply 语义
**缺点：** 更复杂的 schema 格式

### 方案 D：基于约定的匹配（artifact ID 匹配）

如果 artifact ID 是 `tasks` 或 `implementation`，则它是 apply 目标。

**优点：** 简单，无需 schema 变更
**缺点：** 脆弱，不适用于自定义 schema

### 方案 E：所有 artifact 完成 → apply 可用

当所有 schema artifact 事务存在时，apply 可用。实现是用户在 planning 后所做的任何事情。

**优点：** 简单，无需 schema 变更
**缺点：** 无法指导"apply"对不同 workflow 的含义

---

## 决策：在 schema.yaml 中添加 `apply` 块

在 schema 定义中添加顶级 `apply` 字段：

```yaml
name: spec-driven
version: 1
description: 默认 OpenSpec workflow

artifacts:
 # ... 现有 artifact ...

apply:
 requires: [tasks] # apply 前必须存在的 artifact
 tracks: tasks.md # 带有复选框进度的文件（可选）
 instruction: | # 显示给 agent 的指导
 阅读上下文文件，完成待处理任务，边做边标记完成。
 如果遇到阻塞或需要澄清，请暂停。
```

```yaml
name: tdd
version: 1
description: 测试驱动开发 workflow

artifacts:
 # ... 现有 artifact ...

apply:
 requires: [tests] # 实现前必须有测试
 tracks: null # 无复选框跟踪
 instruction: |
 运行测试查看失败。实现最小代码以通过每个测试。
 重构，同时保持测试通过。
```

**关键属性：**
- `requires`：在 apply 可用之前必须存在的 artifact ID 数组
- `tracks`：带有复选框的文件路径（相对于变更目录），如果无跟踪则为 `null`
- `instruction`：apply 阶段的自定义指导

**回退行为：** 没有 `apply` 块的 schema 默认使用"所有 artifact 必须存在"

## 能力

### 被修改的能力
- `cli-artifact-workflow`：Apply 指令变为 schema 感知

## 影响

- **受影响的代码**：`src/commands/artifact-workflow.ts`（generateApplyInstructions）
- **Schema 格式**：可能需要新的 `apply_phase` 字段
- **现有 Schema**：需要为 `spec-driven` 和 `tdd` 添加 apply_phase
- **向后兼容**：没有 apply_phase 的 schema 可以使用默认行为
