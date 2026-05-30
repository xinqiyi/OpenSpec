## 上下文

内置 schema 当前作为 TypeScript 对象嵌入：

```typescript
// src/core/artifact-graph/builtin-schemas.ts
export const SPEC_DRIVEN_SCHEMA: SchemaYaml = {
 name: 'spec-driven',
 version: 1,
 artifacts: [...]
};
```

这种方式不支持 template 与 schema 放在同一位置。指令加载器（切片 3）需要 template，最简洁的方案是使用自包含的 schema 目录。

## 目标 / 非目标

**目标：**
- Schema 作为自包含目录（schema.yaml + templates/）
- 用户通过 XDG 数据目录覆盖
- 简单的两级解析（用户 → 包）
- template 与所属 schema 放在一起

**非目标：**
- 共享 template 回退（有意避免复杂性）
- 运行时 schema 编译
- Schema 继承

## 决策

### 1. 目录结构

每个 schema 是一个包含 `schema.yaml` 和 `templates/` 的目录：

```
<package>/schemas/
├── spec-driven/
│ ├── schema.yaml
│ └── templates/
│ ├── proposal.md
│ ├── design.md
│ ├── spec.md
│ └── tasks.md
└── tdd/
 ├── schema.yaml
 └── templates/
 ├── spec.md
 ├── test.md
 ├── implementation.md
 └── docs.md
```

**原因：** 像 Helm chart 一样自包含。无跨 schema 依赖。每个 schema 拥有自己的 template。

### 2. 解析顺序（2 级）

```
1. ${XDG_DATA_HOME}/openspec/schemas/<name>/schema.yaml # 用户覆盖
2. <package>/schemas/<name>/schema.yaml # 内置
3. 错误（未找到）
```

**原因：** 简单的思维模型。用户可以覆盖整个 schema 目录或仅覆盖部分内容。

### 3. schema.yaml 中的 template 路径

`template` 字段是相对于 schema 的 `templates/` 目录的：

```yaml
# schemas/spec-driven/schema.yaml
artifacts:
 - id: proposal
 template: "proposal.md" # → schemas/spec-driven/templates/proposal.md
```

**原因：** 路径相对于 schema，而非全局 template 目录。

### 4. 通过 import.meta.url 解析包目录

```typescript
function getPackageSchemasDir(): string {
 const currentFile = fileURLToPath(import.meta.url);
 // 从 src/core/artifact-graph/ 导航到包根目录
 return path.join(path.dirname(currentFile), '..', '..', '..', 'schemas');
}
```

**原因：** 在 ESM 中工作。无需硬编码路径。

### 5. 保持 schema.yaml 格式不变

YAML 格式保持不变——仅存储位置发生变化：

```yaml
name: spec-driven
version: 1
description: spec 驱动开发
artifacts:
 - id: proposal
 generates: "proposal.md"
 template: "proposal.md"
 requires: []
```

**原因：** schema 格式无破坏性变更。仅从 TS 迁移到 YAML 文件。

## 迁移

1. 在包根目录创建 `schemas/` 目录
2. 将 `SPEC_DRIVEN_SCHEMA` 转换为 `schemas/spec-driven/schema.yaml`
3. 将 `TDD_SCHEMA` 转换为 `schemas/tdd/schema.yaml`
4. 更新 `resolveSchema()` 以从目录加载
5. 移除 `builtin-schemas.ts`
6. 更新 `listSchemas()` 以扫描目录

## 风险 / 权衡

**运行时的文件 I/O：**
- 以前 schema 是内存中的对象
- 现在需要读取 YAML 文件
- 缓解措施：Schema 很小，每次操作只加载一次

**包分发：**
- 必须确保 `schemas/` 目录包含在 npm 包中
- 在 package.json 的 `files` 中添加

## 开放问题

无。
