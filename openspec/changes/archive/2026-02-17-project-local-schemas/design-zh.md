## 背景

OpenSpec 当前从两个位置解析模式：
1. 用户覆盖：`~/.local/share/openspec/schemas/<name>/`
2. 包内置：`<npm-package>/schemas/<name>/`

此变更增加第三个、最高优先级的层级：项目本地模式，位于 `./openspec/schemas/<name>/`。

`src/core/artifact-graph/resolver.ts` 中的解析函数目前不带 `projectRoot` 参数，因为用户路径和包路径都是绝对路径。为了支持项目本地模式，我们需要将项目根上下文传递到解析器中。

## 目标 / 非目标

**目标：**
- 启用版本控制的自定义工作流模式
- 允许团队通过 git 共享模式，无需每台机器单独设置
- 保持与现有解析器 API 的向后兼容
- 与 `config.yaml` 的 `schema` 字段集成（来自项目配置变更）

**非目标：**
- 模式继承或 `extends` 关键字
- 模板级覆盖（部分分支）
- 模式管理 CLI 命令（`openspec schema copy/which/diff/reset`）
- 验证项目本地模式名称不与内置模式冲突（故意遮蔽）

## 决策

### 决策 1：为解析器函数添加可选的 `projectRoot` 参数

**选择：** 为解析器函数添加可选的 `projectRoot?: string` 参数，而不是在内部使用 `process.cwd()`。

**考虑过的替代方案：**
- 在内部使用 `process.cwd()`：API 更简单但不明确，更难测试，与现有代码库模式不匹配
- 创建独立的项目感知函数：无破坏性变更但 API 笨拙，调用者需要组合使用

**理由：** 代码库已遵循一种模式，即 CLI 命令通过 `process.cwd()` 获取项目根，并将其传递到需要它的函数。添加可选参数保持了向后兼容性，同时实现了明确、可测试的行为。

**受影响的函数：**
```typescript
getSchemaDir(name: string, projectRoot?: string): string | null
listSchemas(projectRoot?: string): string[]
listSchemasWithInfo(projectRoot?: string): SchemaInfo[]
resolveSchema(name: string, projectRoot?: string): SchemaYaml
```

### 决策 2：解析顺序为项目 → 用户 → 包

**选择：** 项目本地模式具有最高优先级，其次是用户覆盖，最后是包内置。

**理由：**
- 项目本地应优先，因为它代表团队意图（版本控制、共享）
- 用户覆盖仍然适用于个人实验，不影响团队
- 包内置是回退默认值

```
1. ./openspec/schemas/<name>/              # 项目本地（最高）
2. ~/.local/share/openspec/schemas/<name>/ # 用户覆盖
3. <npm-package>/schemas/<name>/           # 包内置（最低）
```

### 决策 3：添加 `getProjectSchemasDir()` 辅助函数

**选择：** 创建一个专门的函数来获取项目模式目录路径。

```typescript
function getProjectSchemasDir(projectRoot: string): string {
  return path.join(projectRoot, 'openspec', 'schemas');
}
```

**理由：** 与现有的 `getPackageSchemasDir()` 和 `getUserSchemasDir()` 模式匹配。保持路径逻辑集中。

### 决策 4：扩展 `SchemaInfo.source` 以包含 `'project'`

**选择：** 将 source 类型从 `'package' | 'user'` 更新为 `'project' | 'user' | 'package'`。

**理由：** 消费者需要区分项目本地模式以用于显示目的（例如，`schemasCommand` 输出）。

### 决策 5：不对模式名称冲突进行特殊处理

**选择：** 如果项目本地模式与内置模式同名（例如 `spec-driven`），项目本地版本优先。不产生警告，不报错。

**理由：** 这是有意的遮蔽。团队可能希望自定义内置模式，同时保留相同名称以便熟悉。

## 风险 / 权衡

### 风险：项目模式遮蔽内置模式造成混乱
团队可能创建 `openspec/schemas/spec-driven/` 遮蔽内置模式，导致期望默认行为的人感到困惑。

**缓解措施：** `openspec schemas` 命令显示每个模式的来源。用户可以看到 `spec-driven (project)` vs `spec-driven (package)`。

### 风险：缺少 projectRoot 参数
如果调用者忘记传递 `projectRoot`，将找不到项目本地模式。

**缓解措施：**
- 增量进行更改，更新需要项目本地支持的调用点
- 当 `projectRoot` 未定义时，保留现有行为（仅用户 + 包）

### 权衡：可选参数 vs 必需参数
使 `projectRoot` 可选项保持了向后兼容性，但意味着某些代码路径可能静默跳过项目本地解析。

**已接受：** 向后兼容性更重要。主要入口点（CLI 命令）将始终传递 `projectRoot`。

## 实施方案

1. **更新 `resolver.ts`：**
   - 添加 `getProjectSchemasDir(projectRoot: string)` 函数
   - 更新 `getSchemaDir()` 在提供 `projectRoot` 时优先检查项目本地
   - 更新 `listSchemas()` 在提供 `projectRoot` 时包含项目模式
   - 更新 `listSchemasWithInfo()` 为项目模式返回 `source: 'project'`
   - 更新 `SchemaInfo` 类型以在 source 联合中包含 `'project'`

2. **更新 `artifact-workflow.ts`：**
   - 更新 `schemasCommand` 以传递 `projectRoot` 并显示来源标签

3. **更新调用点：**
   - 任何需要项目本地解析的现有代码应传递 `projectRoot`
   - `config.yaml` 模式解析已可访问 `projectRoot`
