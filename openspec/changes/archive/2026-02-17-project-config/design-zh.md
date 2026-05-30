# 设计：项目配置

## 背景

OpenSpec 目前使用固定的模式解析顺序：
1. `--schema` CLI 标志
2. change 目录中的 `.openspec.yaml`
3. 硬编码默认值：`"spec-driven"`

这迫使用户即使只是为了简单的需求（如注入技术栈上下文或添加特定 artifact 的规则），也需要 fork 整个模式来获得项目级别的自定义能力。

本提案引入 `openspec/config.yaml` 作为一个轻量级自定义层，位于预设模式和完整 fork 之间。它允许团队：
- 设置默认模式
- 将项目上下文注入所有 artifact
- 添加每个 artifact 的规则

**约束条件：**
- 不能破坏缺少配置的现有 change
- 必须在"配置"（本功能）和"fork"（项目本地模式）之间保持清晰分离
- 配置仅限项目级别（无全局/用户级别配置）

**关键利益相关方：**
- 需要轻量自定义而无需 fork 的 OpenSpec 用户
- 通过提交的配置共享工作流约定的团队

## 目标 / 非目标

**目标：**
- 使用 Zod 模式加载和解析 `openspec/config.yaml`
- 在模式解析中使用配置的 `schema` 字段作为默认值
- 将 `context` 注入所有 artifact 指令
- 仅将 `rules` 注入匹配的 artifact 指令
- 优雅处理缺失或无效的配置（回退到默认值）

**非目标：**
- 对模式进行结构性更改（`skip`、`add`、继承）——这些属于 fork 路径
- 上下文的文件引用（`context: ./file.md`）——从字符串开始
- 全局用户级别配置（XDG 目录等）
- 配置管理命令（`openspec config init`）——目前手动创建
- 从旧设置迁移（没有需要迁移的现有配置）

## 决策

### 1. 配置文件格式：YAML 对比 JSON

**决策：** 使用 YAML（`.yaml` 扩展名，支持 `.yml` 别名）

**理由：**
- YAML 天然支持多行字符串（`context: |`）
- 对于文档密集型内容更具可读性
- 与 change 中使用的 `.openspec.yaml` 保持一致
- 易于使用现有的 `yaml` 库解析

**考虑过的替代方案：**
- JSON：更严格，但多行字符串用户体验差
- TOML：大多数用户不熟悉

### 2. 配置位置：项目根目录对比 openspec/ 目录

**决策：** `./openspec/config.yaml`（位于 openspec 目录内）

**理由：**
- 与 `openspec/schemas/`（项目本地模式）放在同一位置
- 保持项目根目录整洁
- OpenSpec 配置的自然命名空间
- 镜像其他工具使用的结构（例如 `.github/`）

**考虑过的替代方案：**
- 根目录下的 `./openspec.config.yaml`：污染根目录，所有权不清晰
- XDG 配置目录：超出范围，尚无全局配置

### 3. 上下文注入：XML 标签对比 Markdown 章节

**决策：** 使用 XML 风格的标签 `<context>` 和 `<rules>`

**理由：**
- 不与 Markdown 冲突的清晰分隔符
- 智能体可以轻松解析结构
- 与代码库中特殊章节的现有模式匹配

**示例：**
```xml
<context>
技术栈：TypeScript, React
</context>

<rules>
- 包含回滚计划
</rules>

<template>
## 摘要
...
</template>
```

**考虑过的替代方案：**
- Markdown 标题：与模板内容冲突
- 注释：对智能体可见性较低

### 4. 模式解析：插入位置

**决策：** 配置的 `schema` 字段位于 change 元数据和硬编码默认值之间

**新的解析顺序：**
1. `--schema` CLI 标志（显式覆盖）
2. change 目录中的 `.openspec.yaml`（change 级别的绑定）
3. **`openspec/config.yaml` schema 字段**（新增——项目默认值）
4. `"spec-driven"`（硬编码回退）

**理由：**
- 保留 CLI 和 change 级别的覆盖（最具体的优先）
- 使配置充当"项目默认值"
- 向后兼容（没有需要冲突的现有配置）

### 5. 规则验证：严格对比宽松

**决策：** 对未知的 artifact ID 给出警告，不报错

**理由：**
- 面向未来：如果模式添加新 artifact，旧配置不会出错
- 开发体验：拼写错误显示警告，但不中断工作流
- 用户可以增量修复

**示例：**
```yaml
rules:
  proposal: [...]
  testplan: [...]  # 模式没有这个 artifact → WARN，不是 ERROR
```

### 6. 错误处理：配置解析失败

**决策：** 记录警告并回退到默认值（不中断命令）

**理由：**
- 配置中的语法错误不应破坏整个 OpenSpec
- 用户可以增量修复配置
- 命令在配置开发期间仍然可用

**警告消息：**
```
⚠️  无法解析 openspec/config.yaml：[错误详情]
    回退到默认模式（spec-driven）
```

## 实现计划

### 阶段 1：核心类型和加载

**文件：`src/core/project-config.ts`（新建）**

```typescript
import { z } from 'zod';
import { readFileSync, existsSync } from 'fs';
import { parse as parseYaml } from 'yaml';
import { findProjectRoot } from '../utils/path-utils';

/**
 * 项目配置的 Zod 模式。
 *
 * 目的：
 * 1. 文档——清晰定义配置文件结构
 * 2. 类型安全——TypeScript 从模式推断 ProjectConfig 类型
 * 3. 运行时验证——使用 safeParse() 进行弹性的逐字段验证
 *
 * 为什么选择 Zod 而不是手动验证：
 * - 帮助快速了解 OpenSpec 的数据接口
 * - 类型和验证的单一可信源
 * - 与其他 OpenSpec 模式保持一致
 */
export const ProjectConfigSchema = z.object({
  schema: z.string().min(1).describe('要使用的工作流模式（例如 "spec-driven", "tdd"）'),
  context: z.string().optional().describe('注入所有 artifact 指令的项目上下文'),
  rules: z.record(
    z.string(),
    z.array(z.string())
  ).optional().describe('每个 artifact 的规则，以 artifact ID 为键'),
});

export type ProjectConfig = z.infer<typeof ProjectConfigSchema>;

const MAX_CONTEXT_SIZE = 50 * 1024; // 50KB 硬限制

/**
 * 从项目根目录读取并解析 openspec/config.yaml。
 * 使用弹性解析——使用 Zod safeParse 独立验证每个字段。
 * 如果文件不存在则返回 null。
 * 如果某些字段无效则返回部分配置（含警告）。
 */
export function readProjectConfig(): ProjectConfig | null {
  const projectRoot = findProjectRoot();

  // 尝试 .yaml 和 .yml，优先使用 .yaml
  let configPath = path.join(projectRoot, 'openspec', 'config.yaml');
  if (!existsSync(configPath)) {
    configPath = path.join(projectRoot, 'openspec', 'config.yml');
    if (!existsSync(configPath)) {
      return null; // 没有配置也可以
    }
  }

  try {
    const content = readFileSync(configPath, 'utf-8');
    const raw = parseYaml(content);

    if (!raw || typeof raw !== 'object') {
      console.warn(`⚠️  openspec/config.yaml 不是有效的 YAML 对象`);
      return null;
    }

    const config: Partial<ProjectConfig> = {};

    // 使用 Zod 解析 schema 字段
    const schemaField = z.string().min(1);
    const schemaResult = schemaField.safeParse(raw.schema);
    if (schemaResult.success) {
      config.schema = schemaResult.data;
    } else if (raw.schema !== undefined) {
      console.warn(`⚠️ 配置中的 'schema' 字段无效（必须是非空字符串）`);
    }

    // 解析带大小限制的 context 字段
    if (raw.context !== undefined) {
      const contextField = z.string();
      const contextResult = contextField.safeParse(raw.context);

      if (contextResult.success) {
        const contextSize = Buffer.byteLength(contextResult.data, 'utf-8');
        if (contextSize > MAX_CONTEXT_SIZE) {
          console.warn(
            `⚠️ 上下文太大（${(contextSize / 1024).toFixed(1)}KB，限制：${MAX_CONTEXT_SIZE / 1024}KB）`
          );
          console.warn(`   忽略 context 字段`);
        } else {
          config.context = contextResult.data;
        }
      } else {
        console.warn(`⚠️ 配置中的 'context' 字段无效（必须是字符串）`);
      }
    }

    // 使用 Zod 解析 rules 字段
    if (raw.rules !== undefined) {
      const rulesField = z.record(z.string(), z.array(z.string()));

      // 首先检查是否为对象结构
      if (typeof raw.rules === 'object' && !Array.isArray(raw.rules)) {
        const parsedRules: Record<string, string[]> = {};
        let hasValidRules = false;

        for (const [artifactId, rules] of Object.entries(raw.rules)) {
          const rulesArrayResult = z.array(z.string()).safeParse(rules);

          if (rulesArrayResult.success) {
            // 过滤掉空字符串
            const validRules = rulesArrayResult.data.filter(r => r.length > 0);
            if (validRules.length > 0) {
              parsedRules[artifactId] = validRules;
              hasValidRules = true;
            }
            if (validRules.length < rulesArrayResult.data.length) {
              console.warn(
                `⚠️ '${artifactId}' 的一些规则是空字符串，已忽略它们`
              );
            }
          } else {
            console.warn(
              `⚠️ '${artifactId}' 的规则必须是字符串数组，已忽略此 artifact 的规则`
            );
          }
        }

        if (hasValidRules) {
          config.rules = parsedRules;
        }
      } else {
        console.warn(`⚠️ 配置中的 'rules' 字段无效（必须是对象）`);
      }
    }

    // 即使某些字段失败也返回部分配置
    return Object.keys(config).length > 0 ? (config as ProjectConfig) : null;

  } catch (error) {
    console.warn(`⚠️ 无法解析 openspec/config.yaml:`, error);
    return null;
  }
}

/**
 * 根据模式的 artifact 验证规则中的 artifact ID。
 * 在指令加载时调用（当模式已知时）。
 * 返回未知 artifact ID 的警告。
 */
export function validateConfigRules(
  rules: Record<string, string[]>,
  validArtifactIds: Set<string>,
  schemaName: string
): string[] {
  const warnings: string[] = [];

  for (const artifactId of Object.keys(rules)) {
    if (!validArtifactIds.has(artifactId)) {
      const validIds = Array.from(validArtifactIds).sort().join(', ');
      warnings.push(
        `规则中的未知 artifact ID: "${artifactId}"。` +
        `模式 "${schemaName}" 的有效 ID：${validIds}`
      );
    }
  }

  return warnings;
}

/**
 * 当用户提供无效模式时建议有效的模式名称。
 * 使用模糊匹配查找相似名称。
 */
export function suggestSchemas(
  invalidSchemaName: string,
  availableSchemas: { name: string; isBuiltIn: boolean }[]
): string {
  // 简单模糊匹配：Levenshtein 距离
  function levenshtein(a: string, b: string): number {
    const matrix: number[][] = [];
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    return matrix[b.length][a.length];
  }

  // 查找最接近的匹配（距离 <= 3）
  const suggestions = availableSchemas
    .map(s => ({ ...s, distance: levenshtein(invalidSchemaName, s.name) }))
    .filter(s => s.distance <= 3)
    .sort((a, b) => a.distance - b.distance)
    .slice(0, 3);

  const builtIn = availableSchemas.filter(s => s.isBuiltIn).map(s => s.name);
  const projectLocal = availableSchemas.filter(s => !s.isBuiltIn).map(s => s.name);

  let message = `❌ 在 openspec/config.yaml 中未找到模式 '${invalidSchemaName}'\n\n`;

  if (suggestions.length > 0) {
    message += `您是否想用以下之一？\n`;
    suggestions.forEach(s => {
      const type = s.isBuiltIn ? '内置' : '项目本地';
      message += `  - ${s.name}（${type}）\n`;
    });
    message += '\n';
  }

  message += `可用模式：\n`;
  if (builtIn.length > 0) {
    message += `  内置：${builtIn.join(', ')}\n`;
  }
  if (projectLocal.length > 0) {
    message += `  项目本地：${projectLocal.join(', ')}\n`;
  } else {
    message += `  项目本地：（未找到）\n`;
  }

  message += `\n修复方式：编辑 openspec/config.yaml，将 'schema: ${invalidSchemaName}' 改为有效的模式名称`;

  return message;
}
```

### 阶段 2：模式解析

**文件：`src/utils/change-metadata.ts`**

更新 `resolveSchemaForChange()` 以检查配置：

```typescript
export function resolveSchemaForChange(
  changeName: string,
  cliSchema?: string
): string {
  // 1. CLI 标志优先
  if (cliSchema) {
    return cliSchema;
  }

  // 2. Change 元数据（.openspec.yaml）
  const metadata = readChangeMetadata(changeName);
  if (metadata?.schema) {
    return metadata.schema;
  }

  // 3. 项目配置（新增）
  const projectConfig = readProjectConfig();
  if (projectConfig?.schema) {
    return projectConfig.schema;
  }

  // 4. 硬编码默认值
  return 'spec-driven';
}
```

**文件：`src/utils/change-utils.ts`**

更新 `createNewChange()` 以使用配置模式：

```typescript
export function createNewChange(
  changeName: string,
  schema?: string
): void {
  // 如果未指定，使用配置中的模式
  const resolvedSchema = schema ?? readProjectConfig()?.schema ?? 'spec-driven';

  // ... 其余 change 创建逻辑
}
```

### 阶段 3：指令注入和验证

**文件：`src/core/artifact-graph/instruction-loader.ts`**

更新 `loadInstructions()` 以注入上下文、规则和验证 artifact ID：

```typescript
// 会话级验证警告缓存（避免重复相同的警告）
const shownWarnings = new Set<string>();

export function loadInstructions(
  changeName: string,
  artifactId: string
): InstructionOutput {
  const projectConfig = readProjectConfig();

  // 从模式加载基础指令
  const baseInstructions = loadSchemaInstructions(changeName, artifactId);
  const schema = getSchemaForChange(changeName); // 假设已加载模式

  // 验证规则 artifact ID（每个会话仅一次）
  if (projectConfig?.rules) {
    const validArtifactIds = new Set(schema.artifacts.map(a => a.id));
    const warnings = validateConfigRules(
      projectConfig.rules,
      validArtifactIds,
      schema.name
    );

    // 每个唯一警告仅显示一次
    for (const warning of warnings) {
      if (!shownWarnings.has(warning)) {
        console.warn(`⚠️  ${warning}`);
        shownWarnings.add(warning);
      }
    }
  }

  // 构建带有 XML 章节的增强指令
  let enrichedInstruction = '';

  // 添加上下文（所有 artifact）
  if (projectConfig?.context) {
    enrichedInstruction += `<context>\n${projectConfig.context}\n</context>\n\n`;
  }

  // 添加规则（仅匹配的 artifact）
  const rulesForArtifact = projectConfig?.rules?.[artifactId];
  if (rulesForArtifact && rulesForArtifact.length > 0) {
    enrichedInstruction += `<rules>\n`;
    for (const rule of rulesForArtifact) {
      enrichedInstruction += `- ${rule}\n`;
    }
    enrichedInstruction += `</rules>\n\n`;
  }

  // 添加原始模板
  enrichedInstruction += `<template>\n${baseInstructions.template}\n</template>`;

  return {
    ...baseInstructions,
    instruction: enrichedInstruction,
  };
}
```

**关于验证时机的说明：** 规则在指令加载期间惰性验证（而非配置加载时），因为：
1. 配置加载时模式未知（循环依赖）
2. 警告在用户实际使用该功能时显示（更好的用户体验）
3. 验证警告按会话缓存以避免刷屏

### 阶段 4：性能和缓存

**为什么配置会被多次读取：**

```typescript
// 示例："openspec instructions proposal --change my-feature"

// 1. 模式解析（确定使用哪个模式）
resolveSchemaForChange('my-feature')
  → readProjectConfig()  // 读取 #1

// 2. 指令加载（注入上下文和规则）
loadInstructions('my-feature', 'proposal')
  → readProjectConfig()  // 读取 #2

// 结果：每条命令读取配置两次
// 更复杂的命令可能读取 3-5 次
```

**性能策略：**

V1 方案：无缓存，每次重新读取配置
- 实现更简单
- 没有缓存失效的复杂性
- 如果配置读取足够快，可以接受

**基准测试目标：**
- 典型配置（1KB 上下文，5 条 artifact 规则）：**< 10ms** 每次读取（即使 5 次也不可察觉）
- 大型配置（50KB 上下文限制）：**< 50ms** 每次读取（对于罕见情况可接受）

**如果基准测试不达标：** 添加简单缓存：

```typescript
// 简单的内存缓存，无失效
let cachedConfig: { mtime: number; config: ProjectConfig | null } | null = null;

export function readProjectConfig(): ProjectConfig | null {
  const projectRoot = findProjectRoot();
  const configPath = path.join(projectRoot, 'openspec', 'config.yaml');

  if (!existsSync(configPath)) {
    return null;
  }

  const stats = statSync(configPath);
  const mtime = stats.mtimeMs;

  // 如果文件未更改，返回缓存配置
  if (cachedConfig && cachedConfig.mtime === mtime) {
    return cachedConfig.config;
  }

  // 读取并解析配置
  const config = parseConfigFile(configPath); // 提取的逻辑

  // 缓存结果
  cachedConfig = { mtime, config };
  return config;
}
```

**性能测试任务：** 添加到阶段 6（测试）
- 测量典型配置读取时间（1KB 上下文）
- 测量大型配置读取时间（50KB 上下文限制）
- 测量单条命令内的重复读取
- 记录结果，仅在需要时添加缓存

## 数据流

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  用户运行：openspec instructions proposal --change foo       │
│                                                              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  resolveSchemaForChange("foo")                               │
│                                                              │
│  1. 检查 CLI 标志 ✗                                          │
│  2. 检查 .openspec.yaml ✗                                    │
│  3. 检查 openspec/config.yaml ✓ → "spec-driven"              │
│                                                              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  loadInstructions("foo", "proposal")                         │
│                                                              │
│  1. 加载 spec-driven/artifacts/proposal.yaml                 │
│  2. 读取 openspec/config.yaml                                │
│  3. 构建增强指令：                                            │
│     - <context>...</context>                                 │
│     - <rules>...</rules>  (如果 rules.proposal 存在)          │
│     - <template>...</template>                               │
│                                                              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  返回包含增强内容的 InstructionOutput                         │
│                                                              │
│  智能体看到项目上下文 + 规则 + 模式模板                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 风险 / 权衡

**[风险]** 配置拼写错误被静默忽略（例如，规则中的错误 artifact ID）
→ **缓解措施：** 在配置加载时验证并警告未知的 artifact ID。不报错以支持向前兼容。

**[风险]** 上下文过大，污染所有 artifact 指令
→ **缓解措施：** 记录推荐大小（< 500 字符）。如果此问题出现，稍后添加每个 artifact 的上下文覆盖。

**[风险]** YAML 解析错误破坏 OpenSpec 命令
→ **缓解措施：** 捕获解析错误，记录警告，回退到默认值。命令保持可用。

**[风险]** 配置在跨命令时被错误缓存
→ **缓解措施：** 每次 `readProjectConfig()` 调用时重新读取配置。V1 无缓存层（简单性优于性能）。

**[权衡]** 上下文注入到所有 artifact
→ **好处：** 跨工作流的项目知识一致
→ **成本：** 目前无法将上下文限定到特定 artifact
→ **未来：** 如果需要，添加 `context: { global: "...", proposal: "..." }`

**[权衡]** 规则使用 artifact ID，而非人类可读名称
→ **好处：** 稳定的标识符（ID 不会改变）
→ **成本：** 用户需要了解模式的 artifact ID
→ **缓解措施：** 记录常见 artifact ID，在 `openspec status` 输出中显示

## 迁移计划

**无需迁移**——这是一个新功能，没有现有状态。

**发布步骤：**
1. 在功能标志后部署配置加载（可选，为安全起见）
2. 使用内部项目测试（本仓库）
3. 在 README 中编写文档并提供示例
4. 如果使用功能标志，将其移除

**回滚策略：**
- 配置仅为附加功能（不破坏现有 change）
- 如果发现错误，可通过环境变量禁用配置解析
- 用户可以删除配置文件以恢复旧行为

## 开放问题

**问：上下文是否应支持文件引用（`context: ./CONTEXT.md`）？**
**答（推迟）：** 从仅字符串开始。如果用户要求，稍后添加文件引用。保持 V1 简单。

**问：除了 .yaml，是否应支持 .yml 别名？**
**答：** 是的，检查两种扩展名。文档中优先使用 .yaml，但接受 .yml 以方便偏好它的用户。

**问：如果配置的 schema 字段引用了不存在的模式怎么办？**
**答：** 模式解析会在下游失败。在尝试加载模式时显示错误，建议有效的模式名称。

**问：规则是否应根据已解析模式的 artifact ID 进行验证？**
**答：** 是的，验证并警告，但不中断。这允许在模式演化时向前兼容。
