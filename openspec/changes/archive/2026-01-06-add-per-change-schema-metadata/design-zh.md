## 上下文

实验性工件工作流支持多种架构（`spec-driven`、`tdd`），但架构选择必须在每个命令上传递。这给代理和用户带来了摩擦。

我们需要一个轻量级的元数据文件来持久化每个变更的架构选择。

## 目标 / 非目标

**目标：**
- 在创建变更时一次性存储架构选择
- 在实验性工作流命令中自动检测架构
- 保持向后兼容性（无元数据 = 默认值）
- 使用 Zod 架构验证元数据

**非目标：**
- 迁移现有变更（它们使用默认值）
- 扩展到遗留命令
- 存储超出架构的额外元数据（目前保持最小化）

## 决策

### 决策：Zod 架构设计

元数据文件（`.openspec.yaml`）将使用此 Zod 架构进行验证：

```typescript
// src/core/artifact-graph/types.ts（或新的 metadata.ts）

import { z } from 'zod';
import { listSchemas } from './resolver.js';

/**
 * 存储在 .openspec.yaml 中的每个变更元数据的架构
 */
export const ChangeMetadataSchema = z.object({
  // 必需：此变更使用哪个工作流架构
  schema: z.string().min(1, { message: 'schema 是必需的' }).refine(
    (val) => listSchemas().includes(val),
    (val) => ({ message: `未知架构 '${val}'。可用：${listSchemas().join(', ')}` })
  ),

  // 可选：创建时间戳（ISO 日期字符串）
  created: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, {
    message: 'created 必须是 YYYY-MM-DD 格式'
  }).optional(),
});

export type ChangeMetadata = z.infer<typeof ChangeMetadataSchema>;
```

**理由：**
- `schema` 是必需的，并在解析时针对可用架构进行验证
- `created` 是可选的，ISO 日期格式以保持一致
- 最小字段——可以在以后扩展而不破坏现有文件
- 遵循现有代码库模式（参见 `ArtifactSchema`、`SchemaYamlSchema`）

### 决策：文件位置和格式

**位置：** `openspec/changes/<name>/.openspec.yaml`

**格式：**
```yaml
schema: tdd
created: 2025-01-05
```

**考虑的替代方案：**
- `change.yaml`——不太隐蔽，但使目录变得杂乱
- `proposal.md` 中的 Frontmatter——与 proposal 的存在耦合
- `openspec.json`——YAML 与现有架构文件匹配

### 决策：读/写函数

```typescript
// src/utils/change-metadata.ts

import * as fs from 'node:fs';
import * as path from 'node:path';
import * as yaml from 'yaml';
import { ChangeMetadataSchema, type ChangeMetadata } from '../core/artifact-graph/types.js';

const METADATA_FILENAME = '.openspec.yaml';

export function writeChangeMetadata(
  changeDir: string,
  metadata: ChangeMetadata
): void {
  // 写入前验证
  const validated = ChangeMetadataSchema.parse(metadata);
  const content = yaml.stringify(validated);
  fs.writeFileSync(path.join(changeDir, METADATA_FILENAME), content);
}

export function readChangeMetadata(
  changeDir: string
): ChangeMetadata | null {
  const metaPath = path.join(changeDir, METADATA_FILENAME);

  if (!fs.existsSync(metaPath)) {
    return null;
  }

  const content = fs.readFileSync(metaPath, 'utf-8');
  const parsed = yaml.parse(content);

  // 验证并返回（如果无效则抛出 ZodError）
  return ChangeMetadataSchema.parse(parsed);
}
```

### 决策：架构解析顺序

确定使用哪个架构时：

1. **显式的 `--schema` 标志**（最高优先级——用户覆盖）
2. **`.openspec.yaml` 元数据**（持久化的选择）
3. **默认的 `spec-driven`**（回退）

```typescript
function resolveSchemaForChange(
  changeDir: string,
  explicitSchema?: string
): string {
  if (explicitSchema) return explicitSchema;

  const metadata = readChangeMetadata(changeDir);
  if (metadata?.schema) return metadata.schema;

  return 'spec-driven';
}
```

## 风险 / 权衡

- **每个变更的额外文件** → 最小开销，隐藏文件
- **YAML 解析依赖** → 已在架构文件中使用 `yaml` 包
- **读取时架构验证** → 如果损坏则快速失败并显示清晰的错误

## 迁移计划

无需迁移：
- 没有 `.openspec.yaml` 的现有变更继续工作（使用默认值）
- 使用 `openspec new change --schema X` 创建的新变更获取元数据文件

## 未决问题

- 如果未指定，`openspec new change` 是否应该以交互方式提示架构？（倾向于不——默认值就可以）
