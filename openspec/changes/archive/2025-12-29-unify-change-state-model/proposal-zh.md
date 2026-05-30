# 提案：统一变更状态模型

## 问题陈述

两个缺陷导致处理变更时行为不一致：

### 缺陷 1：空变更在视图中显示为"已完成"

```typescript
// view.ts 第 90 行
if (progress.total === 0 || progress.completed === progress.total) {
  completed.push({ name: entry.name });  // 错误：total === 0 ≠ 已完成
}
```

结果：`openspec new change foo && openspec view` 将 `foo` 显示为"已完成"，而它实际上没有内容。

### 缺陷 2：制品工作流命令找不到脚手架变更

```typescript
// item-discovery.ts - getActiveChangeIds()
const proposalPath = path.join(changesPath, entry.name, 'proposal.md');
await fs.access(proposalPath);  // 仅返回包含 proposal.md 的变更
```

结果：`openspec status --change foo` 报"未找到"，即使目录存在。

## 根本原因

系统混淆了两个不同的概念：

| 概念 | 问题 | 权威来源 |
|---------|----------|-----------------|
| **规划进度** | 所有规范文档是否已创建？ | 文件存在性（ArtifactGraph） |
| **实施进度** | 编码工作是否完成？ | 任务复选框（tasks.md） |

## 建议的解决方案

### 修复 1：为 view 命令添加"草稿"状态

保留活跃/已完成及其现有含义，但修复缺陷：

| 状态 | 条件 | 含义 |
|-------|----------|---------|
| **草稿** | 无 tasks.md 或 `tasks.total === 0` | 仍在规划中 |
| **活跃** | `tasks.total > 0` 且 `completed < total` | 实施中 |
| **已完成** | `tasks.total > 0` 且 `completed === total` | 完成 |

### 修复 2：制品工作流使用目录存在性

更新 `validateChangeExists()` 以检查目录是否存在，而非检查 `proposal.md` 是否存在。这允许制品工作流引导用户创建他们的第一个制品。

### 保留现有的发现函数

`getActiveChangeIds()` 继续需要 `proposal.md`，以保持与验证和其他命令的向后兼容。

## 变更内容

| 命令 | 之前 | 之后 |
|---------|--------|-------|
| `openspec view` | 空 = "已完成" | 空 = "草稿" |
| `openspec status --change X` | 需要 proposal.md | 在任何目录上工作 |
| `openspec validate X` | 需要 proposal.md | 不变（仍然需要） |

## 破坏性变更

### 最小破坏性变更

1. **`openspec view` 输出**：空变更从"已完成"部分移至新的"草稿"部分

### 非破坏性

- 活跃/已完成语义不变（仍然基于任务）
- `getActiveChangeIds()` 不变
- `openspec validate` 不变
- 已归档变更不受影响

## 不在范围内

- 合并基于任务和基于制品的进度（它们服务于不同目的）
- 更改"已完成"的含义（它保持 = 所有任务已完成）
- 向 view 命令添加制品进度（单独的增强）
- Shell 标签补全用于制品工作流命令（尚未注册）

## 相关命令分析

| 命令 | 使用 `getActiveChangeIds()` | 应包含脚手架？ | 需要变更？ |
|---------|-----------------------------|-----------------------------|----------------|
| `openspec view` | 否（直接读取目录） | 是 → 草稿部分 | **是** |
| `openspec list` | 否（直接读取目录） | 是（显示"无任务"） | 否 |
| `openspec status/next/instructions` | 是 | 是 | **是** |
| `openspec validate` | 是 | 否（无法验证空内容） | 否 |
| `openspec show` | 是 | 否（无内容可显示） | 否 |
| 标签补全 | 是 | 未来增强 | 否 |

## 成功标准

1. `openspec new change foo && openspec view` 将 `foo` 显示在"草稿"部分
2. `openspec new change foo && openspec status --change foo` 正常工作
3. 所有任务已完成的变更仍显示为"已完成"
4. 所有现有测试通过
