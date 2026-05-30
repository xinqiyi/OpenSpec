# 设计：统一变更状态模型

## 概述

此变更修复了两个缺陷，对现有系统的干扰最小：

1. **视图缺陷**：空变更被错误地显示为"已完成"
2. **制品 workflow 缺陷**：命令在脚手架变更上失败

## 关键设计决策：两个系统，两个目的

基于任务和基于制品的系统服务于**不同目的**，应共存：

| 系统 | 目的 | 使用者 |
|--------|---------|---------|
| **任务进度** | 跟踪实施工作 | `openspec view`、`openspec list` |
| **制品进度** | 跟踪 planning/spec 工作 | `openspec status`、`openspec next` |

我们不合并这些系统。相反，我们修复每个系统以在其领域内正确工作。

## 变更 1：修复 View 命令

### 当前逻辑（有缺陷）

```typescript
// view.ts 第 90 行
if (progress.total === 0 || progress.completed === progress.total) {
 completed.push({ name: entry.name });
}
```

问题：`total === 0` 表示"尚未定义任务"，而非"所有任务已完成"。

### 新逻辑

```typescript
if (progress.total === 0) {
 draft.push({ name: entry.name });
} else if (progress.completed === progress.total) {
 completed.push({ name: entry.name });
} else {
 active.push({ name: entry.name, progress });
}
```

### 视图输出变更

**之前：**
```
已完成的变更
─────────────────
 ✓ add-feature （所有任务已完成 - 正确）
 ✓ test-workflow （无任务 - 错误）
```

**之后：**
```
草稿变更
─────────────────
 ○ test-workflow （尚无任务）

活跃变更
─────────────────
 ◉ add-scaffold [████░░░░] 3/7 任务

已完成的变更
─────────────────
 ✓ add-feature （所有任务已完成）
```

## 变更 2：修复制品 workflow 发现

### 当前逻辑（有缺陷）

```typescript
// artifact-workflow.ts - validateChangeExists()
const activeChanges = await getActiveChangeIds(projectRoot);
if (!activeChanges.includes(changeName)) {
 throw new Error(`变更 '${changeName}' 未找到...`);
}
```

问题：`getActiveChangeIds()` 需要 `proposal.md`，但制品 workflow 应在空目录上工作以帮助创建第一个制品。

### 新逻辑

```typescript
async function validateChangeExists(changeName: string, projectRoot: string): Promise<string> {
 const changePath = path.join(projectRoot, 'openspec', 'changes', changeName);

 // 直接检查目录是否存在，而非检查 proposal.md
 if (!fs.existsSync(changePath) || !fs.statSync(changePath).isDirectory()) {
 // 列出可用变更以提供有用的错误消息
 const entries = await fs.promises.readdir(
 path.join(projectRoot, 'openspec', 'changes'),
 { withFileTypes: true }
 );
 const available = entries
 .filter(e => e.isDirectory() && e.name !== 'archive' && !e.name.startsWith('.'))
 .map(e => e.name);

 if (available.length === 0) {
 throw new Error('未找到变更。使用以下命令创建：openspec new change <name>');
 }
 throw new Error(`变更 '${changeName}' 未找到。可用的：\n ${available.join('\n ')}`);
 }

 return changeName;
}
```

### 行为变更

```bash
# 之前
$ openspec new change foo
$ openspec status --change foo
错误：变更 'foo' 未找到。

# 之后
$ openspec new change foo
$ openspec status --change foo
变更：foo
进度：0/4 个制品完成

[ ] proposal
[-] specs（被 proposal 阻塞）
[-] design（被 proposal 阻塞）
[-] tasks（被 specs、design 阻塞）
```

## 保持不变的内容

1. **`getActiveChangeIds()`** - 仍需要 `proposal.md`（由 validate、show 使用）
2. **`getArchivedChangeIds()`** - 不变
3. **活跃/已完成语义** - 仍基于任务复选框
4. **验证** - 仍需要 `proposal.md` 才能有内容可验证

## 文件变更

| 文件 | 变更 |
|------|--------|
| `src/core/view.ts` | 添加草稿类别，修复完成逻辑 |
| `src/commands/artifact-workflow.ts` | 更新 `validateChangeExists()` 以使用目录存在性 |
| `test/commands/artifact-workflow.test.ts` | 为脚手架变更添加测试 |

## 测试策略

1. **单元测试**：使用脚手架变更测试 `validateChangeExists()`
2. **视图测试**：验证三个类别正确渲染
3. **手动测试**：从 `new change` → `status` → `view` 的完整 workflow
