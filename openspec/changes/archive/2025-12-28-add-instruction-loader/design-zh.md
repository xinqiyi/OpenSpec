## 上下文

这是 artifact-graph POC 的第 3 个切片。目前已有的功能：
- `ArtifactGraph` 类及图操作（切片 1）
- `detectCompleted()` 用于基于文件系统的状态检测（切片 1）
- `resolveSchema()` 用于 XDG schema 解析（切片 1）
- `createChange()` 和 `validateChangeName()` 工具函数（切片 2）

在 `restructure-schema-directories` 实现之后，schema 将成为自包含的目录：
```
schemas/<name>/
├── schema.yaml
└── templates/
    └── *.md
```

本提案在此结构之上增加了模板加载和指令丰富功能。

## 目标 / 非目标

**目标：**
- 从 schema 目录加载模板
- 用变更特定上下文（依赖状态）丰富模板
- 格式化变更状态用于 CLI 输出

**非目标：**
- 模板创作 UI
- 动态模板编译/执行
- 缓存（保持无状态，与其他部分一致）

## 决策

### 1. 纯函数而非类

遵循 `resolver.ts` 和 `state.ts` 中的模式。使用简单的 `ChangeContext` 接口配合纯函数：

```typescript
interface ChangeContext {
  changeName: string;
  changeDir: string;
  schemaName: string;
  graph: ArtifactGraph;
  completed: CompletedSet;
}

function loadChangeContext(projectRoot: string, changeName: string, schemaName?: string): ChangeContext
function loadTemplate(schemaName: string, templatePath: string): string
function getInstructions(artifactId: string, context: ChangeContext): string
function formatStatus(context: ChangeContext): string
```

**原因：** 匹配现有代码库模式。更易于测试。无隐藏状态。

### 2. 从 schema 目录解析模板

模板从 schema 的 `templates/` 子目录加载：

```typescript
function loadTemplate(schemaName: string, templatePath: string): string {
  const schemaDir = getSchemaDir(schemaName);  // 来自 resolver.ts
  const fullPath = path.join(schemaDir, 'templates', templatePath);
  return fs.readFileSync(fullPath, 'utf-8');
}
```

解析由 `getSchemaDir()` 处理，该函数已检查用户覆盖 → 包内置。

**原因：** 利用已有的 schema 解析。模板与 schema 放置在一起。

### 3. 模板路径来自工件定义

工件的 `template` 字段是相对于 schema 的 `templates/` 目录的路径：

```yaml
artifacts:
  - id: proposal
    template: "proposal.md"  # → schemas/<schema>/templates/proposal.md
```

**原因：** 明确、简单、无魔法。

### 4. 最小化上下文注入

模板是 markdown。注入会在顶部添加一个包含上下文的标题部分：

```markdown
---
change: add-auth
artifact: proposal
schema: spec-driven
output: openspec/changes/add-auth/proposal.md
---

## 依赖项
- [x] （无——这是一个根工件）

## 后续步骤
创建此工件后，您可以进行：design, specs

---

[原始模板内容...]
```

**原因：** 简单的字符串拼接。无需模板引擎依赖。清晰的分离。

### 5. 状态输出格式

```markdown
## 变更：add-auth（spec-driven）

| 工件 | 状态 | 输出 |
|----------|--------|--------|
| proposal | 完成 | proposal.md |
| specs | 就绪 | specs/*.md |
| design | 阻塞（需要：proposal） | design.md |
| tasks | 阻塞（需要：specs, design） | tasks.md |
```

**原因：** Markdown 表格在终端和文档中均可读。与 CLI 输出风格一致。

## 文件结构

```
src/core/artifact-graph/
├── index.ts              # 添加新导出
├── template.ts           # 新建：模板加载
├── context.ts            # 新建：ChangeContext 加载
└── instructions.ts       # 新建：丰富和格式化
```

## 风险 / 权衡

**对 restructure-schema-directories 的依赖：**
- 本提案要求先完成 schema 重构
- 缓解措施：明确记录依赖关系，按顺序实现

**没有模板引擎：**
- 优点：零依赖，代码简单
- 缺点：表达能力有限
- 缓解措施：当前用例只需要静态模板 + 头部注入

## 迁移计划

不适用——新功能，无需迁移现有代码。

## 开放问题

无。
