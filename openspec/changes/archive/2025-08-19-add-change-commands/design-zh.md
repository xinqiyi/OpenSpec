# 设计：变更命令

## 架构决策

### 命令结构
与 spec 命令类似，我们使用子命令（`change show`、`change list`、`change validate`）的原因：
- 与 spec 命令 schema 保持一致
- 清晰关注点分离
- 未来变更管理功能的可扩展性

### 变更的 JSON Schema
```typescript
{
 version: string, // Schema 版本
 format: "change", // 标识为变更文档
 sourcePath: string, // 原始 markdown 文件路径
 id: string, // 变更标识符
 title: string, // 变更标题
 why: string, // 动机部分
 whatChanges: Array<{
 type: "ADDED" | "MODIFIED" | "REMOVED" | "RENAMED",
 deltas: Array<{
 specId: string,
 description: string,
 requirements?: Array<Requirement> // 仅适用于 ADDED/MODIFIED
 }>
 }>
}
```

**理由：**
- 按操作类型对 delta 进行分组，使得组织更清晰
- 可选的 requirements 字段（仅与 ADDED/MODIFIED 相关）
- 复用 spec 命令中的 RequirementSchema 以保持一致性

### delta 操作
**四种操作类型：**
1. **ADDED**：添加到 spec 的新需求
2. **MODIFIED**：对现有需求的变更
3. **REMOVED**：被删除的需求
4. **RENAMED**：spec 标识符的变更

**设计选择：** 使用显式操作类型而非基于差异的方法，原因：
- Markdown 中的人类可读性
- 清晰的意图传达
- 更易于验证和工具化

### 对 spec 命令的依赖
- **共享 schema**：复用 RequirementSchema 和 ScenarioSchema
- **实现顺序**：必须先实现 spec 命令
- **通用解析器工具**：共享 markdown 解析逻辑

### 遗留兼容性
- 保留现有 `list` 命令功能并显示弃用警告
- 迁移路径：`list` → `change list`，功能相同
- 逐步过渡以避免破坏现有 workflow
