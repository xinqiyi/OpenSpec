# 上下文存储与计划方案

本计划方案是上下文存储、集合、计划方案、工作空间和 repository 本地变更的产品意图来源。

在继续工作空间或计划方案工作之前，请从这里开始。

## 阅读顺序

1. `direction.md` 解释产品模型和原则。
2. `roadmap.md` 列出有序的路线图。
3. `tasks.md` 显示计划方案范围内的进展。
4. `decisions.md` 记录已采纳的决策。
5. `questions.md` 追踪未解决的问题。
6. `work-items/<id>/` 包含一个路线图项的执行记录。

## 边界

计划方案产物承载产品意图和路线图决策。OpenSpec spec 描述代码背后的当前行为契约。

在行为随实现切片改变之前，不要为未来意图重写 spec。

当前产品边界为：

```text
Context stores sync truth.
Collections shape truth.
Initiatives coordinate work.
Workspaces open local views.
Changes implement repo-owned slices.
```
