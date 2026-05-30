## 背景

这是产物跟踪器 POC 的第 2 个切片。目标是提供以编程方式创建变更目录的工具。

**当前状态：** 没有以编程方式创建变更的方法。用户必须手动创建目录。

**提议状态：** 用于变更创建和名称验证的工具函数。

## 目标 / 非目标

### 目标
- **添加** `createChange()` 函数以创建变更目录
- **添加** `validateChangeName()` 函数以进行 kebab-case 验证
- **支持**自动化（Claude 命令、脚本）来创建变更

### 非目标
- 重构现有的 CLI 命令（它们运行良好）
- 创建抽象层或管理器类
- 改变 `ListCommand` 或 `ChangeCommand` 的工作方式

## 决策

### 决策 1：简单的工具函数

**选择**：将函数添加到 `src/utils/change-utils.ts` - 不使用类。

```typescript
// src/utils/change-utils.ts

export function validateChangeName(name: string): { valid: boolean; error?: string }

export async function createChange(
  projectRoot: string,
  name: string
): Promise<void>
```

**原因**：
- 简单，无抽象开销
- 易于测试
- 易于在需要的地方导入
- 匹配 `src/utils/` 中现有的工具模式

**考虑的替代方案**：
- ChangeManager 类：被拒绝 - 对 2 个函数来说过度设计
- 添加到现有命令：被拒绝 - 将 CLI 与可重用逻辑混合

### 决策 2：Kebab-Case 验证模式

**选择**：使用 `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` 验证名称

有效：`add-auth`、`refactor-db`、`add-feature-2`、`refactor`
无效：`Add-Auth`、`add auth`、`add_auth`、`-add-auth`、`add-auth-`、`add--auth`

**原因**：
- 文件系统安全（无特殊字符）
- URL 安全（用于未来的 Web UI）
- 与仓库中现有的变更命名一致

## 文件变更

### 新增文件
- `src/utils/change-utils.ts` - 工具函数
- `src/utils/change-utils.test.ts` - 单元测试

### 修改的文件
- 无

## 风险 / 权衡

| 风险 | 缓解措施 |
|------|----------|
| 函数可能无法覆盖所有用例 | 从简单开始，需要时扩展 |
| 与未来工作的命名冲突 | 使用清晰、具体的函数名 |
