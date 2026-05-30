## 背景

目前，delta spec 仅在运行 `openspec archive` 时才会应用到主 spec。这捆绑了两个关注点：
1. 应用 spec 变更（delta → 主 spec）
2. archive 变更（移动到 archive 文件夹）

用户希望更灵活地提前同步 spec，特别是在迭代期间。archive 命令已经包含 `buildUpdatedSpec()` 中的合并逻辑。

## 目标 / 非目标

**目标：**
- 将 spec 同步与 archive 解耦
- 为 Agent 提供 `/opsx:sync` skill 以按需同步 spec
- 保持操作幂等（多次运行安全）

**非目标：**
- 跟踪 spec 是否已同步（无状态）
- 改变 archive 行为（它将继续应用 spec）
- 支持部分应用（所有 delta 一起同步）

## 决策

### 1. 重用现有的合并逻辑

**决策**：将 `buildUpdatedSpec()` 逻辑从 `ArchiveCommand` 提取到共享模块。

**理由**：archive 命令已经实现了 delta 解析和应用。与其重复，不如提取和重用。

**考虑的替代方案**：
- 在新命令中重复逻辑（被拒绝：维护负担）
- 让 sync 带标志调用 archive（被拒绝：耦合）

### 2. 无状态跟踪

**决策**：不跟踪 spec 是否已同步。每次调用读取 delta 和主 spec，进行合并。

**理由**：
- 幂等操作不需要状态
- 避免标志和实际情况之间的同步问题
- 更简单的实现和心智模型

**考虑的替代方案**：
- 在 `.openspec.yaml` 中跟踪 `specsSynced: true`（被拒绝：不必要的复杂性）
- 存储已同步 delta 的快照（被拒绝：过度设计）

### 3. Agent 驱动的方法（无 CLI 命令）

**决策**：`/opsx:sync` skill 完全由 Agent 驱动 - Agent 读取 delta spec 并直接编辑主 spec。

**理由**：
- 允许智能合并（添加场景而不复制整个需求）
- Delta 表示*意图*，而不是整体替换
- 更灵活和自然的编辑 workflow
- archive 仍然使用程序化合并（用于最终确定的变更）

### 4. archive 行为不变

**决策**：archive 继续在其流程中应用 spec。如果 spec 已经合并，操作是无操作的。

**理由**：向后兼容。不使用 `/opsx:sync` 的用户获得相同的体验。

## 风险 / 权衡

**[风险] 多个变更修改同一 spec**
→ 最后同步的胜出。与当前 archive 相同。用户应协调或使用顺序 archive。

**[风险] 用户同步 spec 后继续编辑 delta**
→ 再次运行 `/opsx:sync` 会重新合并。幂等设计处理了这种情况。

**[权衡] 无撤销机制**
→ 用户可以在需要时 `git checkout` 主 spec。显式撤销命令不在范围内。

## 实现方案

1. 将 spec 应用逻辑从 `ArchiveCommand.buildUpdatedSpec()` 提取到 `src/core/specs-apply.ts`
2. 在 `skill-templates.ts` 中添加 `/opsx:sync` 的 skill template
3. 在托管 skill 中注册 skill
