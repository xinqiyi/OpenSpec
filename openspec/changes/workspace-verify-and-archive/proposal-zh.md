## 为什么

状态：已被上下文存储和倡议方向推迟。每个 repository 的进度可见性仍然重要，但 verify/archive 应围绕倡议状态和链接的 repository 本地 OpenSpec 变更重新设计，而不是围绕 workspace 拥有的最终 archive 状态。在此链接存在之前，不要将其作为一等公民的 workspace 生命周期命令实现。

剩余部分保留了原始的 workspace verify/archive 方向以供后续参考。在倡议和与倡议链接的 repository 本地变更存在后，这项工作仍预计会发挥作用；它不是当前立即关注的重点。

用户需要知道跨 repository 的 workspace 变更是否完成，而无需将所有 repository 的进展扁平化为一个模糊的完成状态。

期望的生命周期是：

```text
验证每个 repository 切片。
查看哪些切片已完成或仍开放。
在适当时 archive repository 本地结果。
当跨 repository 目标完成时 archive workspace 变更。
```

验证和 archive 应使用户的跨 repository 状态更清晰，而不是强迫他们推理内部 artifact 的位置。

## 变更内容

添加 workspace 感知的验证和 archive 行为：

- 验证 workspace 级别的变更结构和目标 repository 状态
- 显示每个 repository 切片的进度
- 在需要时支持 repository 本地的 archive 工作
- 当协调目标完成时支持显式的 workspace 级别 archive
- 避免将部分 repository 完成视为完整 workspace 完成

planning 依赖：

- 依赖于 `workspace-apply-repo-slice`。

## 能力

### 新能力

- `workspace-verify-archive`：验证和 archive workspace 变更，具有每个 repository 的进度可见性。

### 修改的能力

- `cli-archive`：添加 workspace 感知的 archive 语义。
- `opsx-verify-skill`：添加 workspace 验证指导。
- `opsx-archive-skill`：添加 workspace archive 指导。

## 影响

- workspace 状态、验证和 archive 行为。
- 每个 repository 切片完成报告。
- workspace 级别的硬完成标记或等效的 archive 状态。
- 测试部分完成、最终 workspace archive 以及与独立 repository 本地 archive 流程的兼容性。
