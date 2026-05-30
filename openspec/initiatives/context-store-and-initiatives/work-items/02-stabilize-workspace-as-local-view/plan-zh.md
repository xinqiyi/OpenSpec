# 将 workspace 稳定为本地视图

## 状态

在当前本地视图稳定化切片中已完成。剩余的 workspace
planning/apply/verify/archive 行为保持推迟，直到存在与 initiative 关联的
repository 本地变更。

## 真相来源

从 `../direction.md` 开始。

相关模型是：

```text
上下文存储同步真相。
集合塑造真相。
Initiative 协调工作。
workspace 打开本地视图。
变更实现 repository 拥有的切片。
```

## 目标

保持 workspace setup、link、relink、list、open、update 和 doctor 的实用性，同时
明确 workspace 是可重新生成的机器本地视图，而非
持久化的协调对象。

## 商定的指导方向

生成的 workspace 指导应按所有权引导 agent：

- 使用 workspace 打开协调工作的本地视图。
- 使用 initiative 进行持久的跨团队或跨 repository 意图、决策、
 需求和协调上下文。
- 使用 repository 本地的 OpenSpec 变更为由 repository 或
 团队拥有的实现计划。
- 使用链接的 repository 和文件夹来检查上下文、了解所有权，
 并在拥有工作的地方进行编辑。
- 保持 workspace 本地文件专注于本地路径、开启器状态、agent 设置
 和其他特定于机器的视图状态。
- 使用 OpenSpec workspace 命令，而不是手动编辑
 `.openspec-workspace/*.yaml`。
- 如果 workspace 包含遗留或 Beta workspace 级别的 planning 文件，将其
 视为兼容性上下文，除非用户明确要求使用该 Beta
 流程。

## 不再强化的指导

不要告诉 agent 使用 workspace 级别的 `changes/` 作为协调工作的
planning 归宿。这会强化已被取代的模型——即 workspace 级别的
`changes/` 树拥有 spec 的共享跨 repository 计划。

现有的 workspace planning 行为可以作为 Beta 或遗留基础设施保留，
但不应引导新的生命周期设计。

## 可能的 repository 切片

- 在 `src/core/workspace/open-surface.ts` 中重新措辞生成的 workspace 指导。
- 更新针对性的指导测试。
- 使 `workspace update` 刷新已有 workspace 的指导块。
- 保持 spec 不变，直到行为变更有意更新它们。

## 结项

已实现：

- 生成的 workspace 指导现在按所有权引导工作
- `workspace update` 刷新 workspace 本地指导/开放表面文件和
 受管理的 agent skill
- workspace planning 操作上下文将 Beta workspace artifact 视为
 "workspace 本地"兼容性上下文
- 实时文档将 workspace 描述为本地视图，而非持久化的 planning 归宿

已推迟：

- 正常的 doctor 已安装 skill 清单
- workspace apply、verify 和 archive
- 与 initiative 关联的 repository 本地变更编排
