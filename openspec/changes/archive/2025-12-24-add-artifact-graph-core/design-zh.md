## 背景

这实现了制品 POC 分析中的"切片 1：什么已就绪？"。核心思想是将文件系统用作数据库——制品完成状态通过文件存在性检测，使系统成为无状态的，并对版本控制友好。

该模块将与当前的 OpenSpec 系统并行存在，作为一个并行能力，可能支持未来的迁移或集成。

## 目标 / 非目标

**目标：**
- 纯净的依赖图逻辑，无副作用
- 无状态检测（每次查询重新扫描文件系统）
- 支持多文件制品的 glob schema（例如 `specs/*.md`）
- 从 YAML schema 加载制品定义
- 计算拓扑构建顺序
- 基于依赖完成状态确定"就绪"的制品

**非目标：**
- CLI 命令（切片 4）
- 多变更管理（切片 2）
- template 解析和丰富（切片 3）
- agent 集成或 Claude 命令
- 替换现有的 OpenSpec 功能

## 决策

### 决策：文件系统作为数据库
使用文件存在性进行状态检测，而非单独的状态文件。

**理由：**
- 无状态——不可能出现状态损坏
- 对 Git 友好——状态从已提交文件推导
- 简单——状态文件和实际文件之间无同步问题

**考虑过的替代方案：**
- JSON/SQLite 状态文件：更复杂，有同步问题，对 Git 不友好
- Git 元数据：与 Git 耦合太紧，实现复杂

### 决策：Kahn 算法用于拓扑排序
使用 Kahn 算法计算构建顺序。

**理由：**
- 理解成熟，O(V+E) 复杂度
- 在执行过程中自然检测循环
- 产生稳定、确定性的顺序

### 决策：Glob schema 支持
在制品的 `generates` 字段中支持 glob schema，如 `specs/*.md`。

**理由：**
- 允许多个文件满足单个制品需求
- 包含多个文件的 spec 目录的常见 schema
- 使用标准 glob 语法

### 决策：不可变的 CompletedSet
将完成状态表示为已完成的制品 ID 的不可变 Set。

**理由：**
- 函数式风格，更容易推理
- 每次查询重新推导状态，无需变异
- 图结构和运行时状态之间清晰分离
- 文件系统只能检测二进制存在（完成 vs 未完成）

**注意：** `inProgress` 和 `failed` 状态推迟到未来切片。它们需要外部状态跟踪（例如状态文件），因为仅靠文件存在性无法区分这些状态。

### 决策：Zod 用于 schema 验证
使用 Zod 验证 YAML schema 结构并推导 TypeScript 类型。

**理由：**
- 已是项目依赖（v4.0.17），在 `src/core/schemas/` 中使用
- 通过 `z.infer<>` 进行类型推导——类型的单一权威来源
- 运行时验证，带有详细错误消息
- 与现有项目 schema 一致（`base.schema.ts`、`config-schema.ts`）

**考虑过的替代方案：**
- 手动验证：更多代码，容易出错，无类型推导
- JSON Schema：需要额外依赖，TypeScript 集成较少
- io-ts：项目中尚未使用，学习曲线较陡

### 决策：两级 schema 解析
schema 从全局用户数据目录解析，回退到包内置。

**解析顺序：**
1. `${XDG_DATA_HOME:-~/.local/share}/openspec/schemas/<name>.yaml` - 全局用户覆盖
2. `<package>/schemas/<name>.yaml` - 内置默认值

**理由：**
- 遵循 XDG 基本目录 spec（schema 是数据，而非配置）
- 镜像 `src/core/global-paths.ts` 中的现有 `getGlobalConfigDir()` schema
- 内置 schema 打包在包中，永不自动复制
- 用户通过在全局数据目录中创建文件进行自定义
- 简单——无项目级覆盖（如有需要可稍后添加）

**XDG 合规：**
- 设置时使用 `XDG_DATA_HOME` 环境变量（所有平台）
- Unix/macOS 回退：`~/.local/share/openspec/`
- Windows 回退：`%LOCALAPPDATA%/openspec/`

**考虑过的替代方案：**
- 项目级覆盖：增加复杂性，初期不需要
- 自动复制到用户空间：产生漂移，更难更新默认值
- 配置目录（`XDG_CONFIG_HOME`）：schema 是 workflow 定义（数据），而非用户偏好（配置）

### 决策：template 字段已解析但未解析
`template` 字段在 schema YAML 中是必填的，但 template 解析推迟到切片 3。

**理由：**
- 切片 1 专注于"什么已就绪？"——仅依赖和完成查询
- template 路径在语法上验证（非空字符串）但未解析
- 保持切片 1 聚焦且可独立测试

### 决策：循环错误格式
循环错误列出循环中的所有制品 ID，以便于调试。

**格式：** `"检测到循环依赖：A → B → C → A"`

**理由：**
- 显示完整的循环路径，而不仅仅存在循环
- 可操作——开发者可以确切看到需要修复哪些制品
- 与 Kahn 算法一致，该算法自然识别循环参与者

## 数据结构

**Zod schema（权威来源）：**

```typescript
import { z } from 'zod';

// 制品定义 schema
export const ArtifactSchema = z.object({
 id: z.string().min(1, '制品 ID 是必填的'),
 generates: z.string().min(1), // 例如 "proposal.md" 或 "specs/*.md"
 description: z.string(),
 template: z.string(), // template 文件路径
 requires: z.array(z.string()).default([]),
});

// 完整 schema YAML 结构
export const SchemaYamlSchema = z.object({
 name: z.string().min(1, 'schema 名称是必填的'),
 version: z.number().int().positive(),
 description: z.string().optional(),
 artifacts: z.array(ArtifactSchema).min(1, '至少需要一个制品'),
});

// 推导的 TypeScript 类型
export type Artifact = z.infer<typeof ArtifactSchema>;
export type SchemaYaml = z.infer<typeof SchemaYamlSchema>;
```

**运行时状态（非 Zod - 仅内部）：**

```typescript
// 切片 1：通过文件系统的简单完成跟踪
type CompletedSet = Set<string>;

// 阻塞查询返回类型
interface BlockedArtifacts {
 [artifactId: string]: string[]; // 制品 → 未满足的依赖列表
}

interface ArtifactGraphResult {
 completed: string[];
 ready: string[];
 blocked: BlockedArtifacts;
 buildOrder: string[];
}
```

## 文件结构

```
src/core/artifact-graph/
├── index.ts # 公共导出
├── types.ts # Zod schema 和类型定义
├── graph.ts # ArtifactGraph 类
├── state.ts # 状态检测逻辑
├── resolver.ts # schema 解析（全局 → 内置）
└── schemas/ # 内置 schema 定义（包级别）
 ├── spec-driven.yaml # 默认：proposal → specs → design → tasks
 └── tdd.yaml # 替代方案：tests → implementation → docs
```

**schema 解析路径：**
- 全局用户覆盖：`${XDG_DATA_HOME:-~/.local/share}/openspec/schemas/<name>.yaml`
- 包内置：`src/core/artifact-graph/schemas/<name>.yaml`（随包捆绑）

## 风险 / 权衡

| 风险 | 缓解措施 |
|------|------------|
| Glob schema 边界情况 | 使用经过充分测试的 glob 库（fast-glob 或类似库） |
| 循环检测 | Kahn 算法在循环上自然失败；提供清晰错误 |
| schema 演进 | schema 中的版本字段，加载时验证 |

## 未决问题

无——所有问题已在决策部分解决。
