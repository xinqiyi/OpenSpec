# 移除 Diff 命令

## 问题

`openspec diff` 命令为 OpenSpec CLI 增加了不必要的复杂性，原因如下：

1. **功能冗余**：`openspec show` 命令已通过结构化 JSON 输出和 Markdown 渲染提供了全面的变更可视化
2. **维护负担**：diff 命令需要单独的依赖（jest-diff）和额外的代码复杂度（约 227 行）
3. **价值有限**：开发者可以使用现有工具实现更好的差异可视化：
   - 使用 Git diff 查看实际文件变更
   - 使用 `show` 命令进行结构化变更查看
   - 使用标准差异工具直接比较规范文件
4. **与动词-名词模式不一致**：该命令不遵循其他命令正在迁移的首选动词优先命令结构

## 解决方案

完全移除 `openspec diff` 命令，并引导用户使用更合适的替代方案：

1. **查看变更内容**：使用 `openspec show <change-name>`，它提供：
   - 使用 `--json` 标志的结构化 JSON 输出
   - 适合人类阅读格式的 Markdown 渲染
   - 使用 `--deltas-only` 标志的仅增量视图
   - 完整的规范内容可视化

2. **比较文件**：使用标准工具：
   - `git diff` 进行版本控制比较
   - 系统差异工具进行逐文件比较
   - IDE 差异查看器进行可视化比较

## 收益

- **降低复杂度**：移除约 227 行代码和 jest-diff 依赖
- **更清晰的用户路径**：引导用户使用规范的 `show` 命令查看变更
- **更低的维护成本**：需要维护和测试的命令更少
- **更好的一致性**：专注于核心 OpenSpec 工作流，无需冗余功能

## 实施

### 要删除的文件
- `/src/core/diff.ts` - 整个 diff 命令实现
- `/openspec/specs/cli-diff/spec.md` - diff 命令规范

### 要更新的文件
- `/src/cli/index.ts` - 移除 diff 命令注册（第 8、84-96 行）
- `/package.json` - 移除 jest-diff 依赖
- `/README.md` - 移除 diff 命令文档
- `/openspec/README.md` - 移除 diff 命令引用
- 其他提及 `openspec diff` 的文档文件

### 用户迁移指南

当前使用 `openspec diff` 的用户应迁移到：

```bash
# 之前
openspec diff add-feature

# 之后 - 查看变更提案
openspec show add-feature

# 之后 - 仅查看增量
openspec show add-feature --json --deltas-only

# 之后 - 使用 git 进行文件比较
git diff openspec/specs openspec/changes/add-feature/specs
```

## 风险

- **用户干扰**：现有用户的工作流可能依赖于 diff 命令
  - 缓解措施：提供清晰的迁移指南和弃用期

- **视觉差异功能丧失**：彩色统一差异格式将不再可用
  - 缓解措施：用户可以使用 git diff 或其他工具进行视觉比较

## 成功指标

- 成功移除，无损坏的依赖
- 文档已更新以反映变更
- 移除 diff 命令后测试通过
- 通过移除 jest-diff 依赖减小包大小
