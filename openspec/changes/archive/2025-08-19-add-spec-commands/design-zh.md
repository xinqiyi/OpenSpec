# 设计：Spec 命令

## 架构决策

### 命令层次结构
我们选择了子命令模式（`spec show`、`spec list`、`spec validate`）以：
- 在公共命名空间下对相关功能进行分组
- 实现未来可扩展性而不污染顶级 CLI
- 保持与计划中的 `change` 命令结构的一致性

### JSON 模式结构
Spec JSON 模式遵循以下结构：
```typescript
{
  version: string,        // 用于兼容性的模式版本
  format: "spec",        // 标识为规范文档
  sourcePath: string,    // 原始 Markdown 文件路径
  id: string,           // 来自文件名的规范标识符
  title: string,        // 人类可读的标题
  overview?: string,    // 可选的概述章节
  requirements: Array<{
    id: string,
    text: string,
    scenarios: Array<{
      id: string,
      text: string
    }>
  }>
}
```

**理由：**
- 需求数组的扁平结构（而非嵌套对象）便于迭代
- 场景嵌套在需求中以维护关系
- 元数据字段（version、format、sourcePath）用于工具集成

### 解析器架构
- **Markdown 优先方法**：解析 Markdown 标题而非自定义语法
- **流式解析器**：逐行处理以高效处理大文件
- **严格的标题层次结构**：强制使用 ##/###/#### 结构以确保一致性

### 验证策略
- **解析时验证**：在解析期间捕获结构性问题
- **模式验证**：使用 Zod 对解析后的数据进行运行时类型检查
- **独立的验证命令**：允许无需完整解析/转换即可验证
