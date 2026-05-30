# 项目配置

## 摘要

添加 `openspec/config.yaml` 支持，用于项目级别的配置。这使得团队无需 fork 模式即可自定义 OpenSpec 行为，通过提供注入到 artifact 生成中的上下文和规则来实现。

## 动机

目前，自定义 OpenSpec 需要 fork 整个模式：
- 即使只添加一条规则也必须复制所有文件
- 当 openspec 升级时会丢失更新
- 对于简单的自定义操作来说门槛过高

大多数用户不需要不同的工作流结构。他们需要的是：
- 提供项目上下文（技术栈、约定、约束）
- 为特定 artifact 添加规则（需求、格式偏好）

## 设计决策

### 双路径模型

OpenSpec 自定义遵循两条不同的路径：

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   配置（本次变更）                FORK（项目本地模式）           │
│   ─────────────────────           ────────────────────────────  │
│                                                                 │
│   使用预设模式                     从头定义自己的模式            │
│   + 添加上下文                                                  │
│   + 添加规则                                                    │
│                                                                 │
│   openspec/config.yaml            openspec/schemas/my-flow/     │
│                                                                 │
│   ✓ 简单                          ✓ 完全控制                    │
│   ✓ 获取更新                      ✗ 需自行维护所有内容          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 配置模式

```yaml
# openspec/config.yaml

# 必填：使用哪个工作流模式
schema: spec-driven

# 可选：注入到所有 artifact 提示中的项目上下文
context: |
  技术栈：TypeScript, React, Node.js, PostgreSQL
  API 风格：RESTful，记录在 docs/api-conventions.md 中
  测试：Jest + React Testing Library
  我们重视所有公共 API 的向后兼容性

# 可选：每个 artifact 的规则（附加性）
rules:
  proposal:
    - 包含回滚计划
    - 识别受影响的团队并在 #platform-changes 中通知
  specs:
    - 使用 Given/When/Then 格式
    - 在发明新模式之前参考现有模式
  tasks:
    - 每个任务应在 < 2 小时内完成
    - 包含验收标准
```

### 配置中不包含的内容

以下内容被明确排除以保持模型简单：

| 功能 | 决策 | 理由 |
|------|------|------|
| `skip: [artifact]` | 不支持 | 结构性变更属于 fork 路径 |
| `add: [{...}]` | 不支持 | 结构性变更属于 fork 路径 |
| `extends: base` | 不支持 | 无继承，fork 是完整复制 |
| `context: ./file.md` | 暂不支持 | 从字符串开始，如果需要后续添加文件引用 |

### 字段定义

#### `schema`（必填）

使用哪个工作流模式。可以是：
- 内置名称：`spec-driven`、`tdd`
- 项目本地模式名称：`my-workflow`（需要 project-local-schemas 变更）

它成为以下情况的默认模式：
- 创建时未使用 `--schema` 标志的新 change
- 在未有 `.openspec.yaml` 元数据的 change 上运行的命令

#### `context`（可选）

包含项目上下文的字符串。注入到所有 artifact 提示中。

使用场景：
- 技术栈描述
- 约定/风格指南的链接
- 团队约束或偏好
- 领域特定上下文

#### `rules`（可选）

每个 artifact 的规则，以 artifact ID 为键。对模式内置指导的附加补充。

```yaml
rules:
  <artifact-id>:
    - 规则 1
    - 规则 2
```

规则注入到特定 artifact 的提示中，而非所有提示。

### 注入格式

为 artifact 生成指令时：

```xml
<context>
技术栈：TypeScript, React, Node.js, PostgreSQL
API 风格：RESTful，记录在 docs/api-conventions.md 中
...
</context>

<rules>
- 包含回滚计划
- 识别受影响的团队并在 #platform-changes 中通知
</rules>

<template>
[模式的内置模板内容]
</template>
```

上下文出现在所有 artifact 中。规则仅出现在匹配的 artifact 中。

### 配置创建策略

**为何与 `artifact-experimental-setup` 集成？**

此功能面向**实验性工作流用户**。在实验性设置期间创建配置（而非提供独立命令）是有意为之的：

**理由：**
1. **单一入口点**——正在设置实验性功能的用户已经处于"配置模式"
2. **上下文时机**——在设置工作流时配置项目默认值很自然
3. **避免过早暴露 API 面**——在功能毕业前不提供独立的 `openspec config init`
4. **实验性范围**——保持配置作为实验性功能，而非稳定 API
5. **渐进式披露**——用户可以跳过，后续如果需要再手动创建

**演进路径：**

```
今天（实验性）：
  openspec artifact-experimental-setup
    → 提示创建配置
    → 创建 .claude/skills/
    → 创建 openspec/config.yaml

未来（毕业时）：
  openspec init
    → 提示创建配置
    → 创建 openspec/ 目录
    → 创建 openspec/config.yaml

  + 独立命令：
    openspec config init
    openspec config validate
    openspec config set <key> <value>
```

**为何可选？**

配置是**附加性**的，非必选：
- OpenSpec 无需配置也可工作（使用默认值）
- 用户可以在设置期间跳过，稍后手动添加
- 团队可以从简单开始，在遇到摩擦时添加配置
- 没有 git 中的配置文件 = 没问题，每个人都能得到默认值

**设计原则：** 系统从不*要求*配置，但在用户需要自定义时使其易于创建。

## 范围

### 在范围之内

**核心配置系统：**
- 使用 Zod 模式定义 `ProjectConfig` 类型
- 添加带有优雅错误处理的 `readProjectConfig()` 函数
- 更新指令生成以注入上下文（所有 artifact）
- 更新指令生成以注入规则（每个 artifact）
- 更新模式解析以使用配置的 `schema` 字段作为默认值
- 更新 `openspec new change` 以使用配置的模式作为默认值

**配置创建（实验性设置）：**
- 扩展 `artifact-experimental-setup` 命令，可选创建配置
- 模式选择的交互式提示（含每个模式的描述）
- 项目上下文的交互式提示（可选多行输入）
- 每个 artifact 规则的交互式提示（可选）
- 创建后立即验证配置
- 为希望稍后手动创建配置的用户显示清晰的"跳过"选项
- 显示创建的配置位置和使用示例

### 超出范围

- 结构性变更的 `skip`/`add`（结构性变更使用 fork 路径）
- 上下文的文件引用（`context: ./CONTEXT.md`）——从字符串开始，后续需要时添加
- 全局用户级别配置（XDG 目录等）
- 与标准 `openspec init` 的集成（实验性毕业时将添加）
- 独立 `openspec config init` 命令（可能在未来的变更中添加）
- `openspec config validate` 命令（可能在未来的变更中添加）
- 配置编辑/更新命令（用户直接编辑 YAML）

## 用户体验

### 设置配置（实验性工作流）

当用户设置实验性工作流时，他们会被提示可选地创建配置：

```bash
$ openspec artifact-experimental-setup

正在设置实验性 artifact 工作流...

✓ 已创建 .claude/skills/openspec-explore/SKILL.md
✓ 已创建 .claude/skills/openspec-new-change/SKILL.md
✓ 已创建 .claude/skills/openspec-continue-change/SKILL.md
✓ 已创建 .claude/skills/openspec-apply-change/SKILL.md
✓ 已创建 .claude/skills/openspec-ff-change/SKILL.md
✓ 已创建 .claude/skills/openspec-sync-specs/SKILL.md
✓ 已创建 .claude/skills/openspec-archive-change/SKILL.md

✓ 已创建 .claude/commands/opsx/explore.md
✓ 已创建 .claude/commands/opsx/new.md
✓ 已创建 .claude/commands/opsx/continue.md
✓ 已创建 .claude/commands/opsx/apply.md
✓ 已创建 .claude/commands/opsx/ff.md
✓ 已创建 .claude/commands/opsx/sync.md
✓ 已创建 .claude/commands/opsx/archive.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 项目配置（可选）

配置 OpenSpec 工作流的项目默认值。

? 创建 openspec/config.yaml？（Y/n）Y

? 新 change 的默认模式？
  ❯ spec-driven（proposal → specs → design → tasks）
    tdd（spec → tests → implementation → docs）

? 添加项目上下文？（可选）
  上下文在创建 artifact 时展示给 AI。
  示例：技术栈、约定、风格指南、领域知识

  按 Enter 跳过，或输入/粘贴上下文：
  │ 技术栈：TypeScript, React, Node.js, PostgreSQL
  │ API 风格：RESTful，记录在 docs/api-conventions.md 中
  │ 测试：Jest + React Testing Library
  │ 我们重视所有公共 API 的向后兼容性
  │
  [按 Enter 完成]

? 添加每个 artifact 的规则？（可选）（Y/n）Y

  哪些 artifact 应自定义规则？
  [空格选择，按 Enter 完成]
  ◯ proposal
  ◉ specs
  ◯ design
  ◯ tasks

? 为 specs artifact 设置规则：
  每行输入一条规则，在空行按 Enter 完成：
  │ 使用 Given/When/Then 格式编写场景
  │ 在发明新模式之前参考现有模式
  │
  [空行完成]

✓ 已创建 openspec/config.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 设置完成！

📖 配置创建于：openspec/config.yaml
   • 默认模式：spec-driven
   • 项目上下文：已添加（4 行）
   • 规则：1 个 artifact 已配置

使用方法：
  • 新 change 自动使用 'spec-driven' 模式
  • 上下文注入到所有 artifact 指令中
  • 规则应用于匹配的 artifact

与团队共享：
  git add openspec/config.yaml .claude/
  git commit -m "使用项目配置设置 OpenSpec 实验性工作流"

[实验性设置的其余输出...]
```

**关键 UX 决策：**

1. **设置期间提示**——因为用户已经在配置实验性功能，这是自然的位置
2. **每一步都可选**——清晰的跳过选项，无强制配置
3. **引导式提示**——模式描述、上下文示例、artifact 选择
4. **即时验证**——创建后立即验证配置，错误即时显示
5. **清晰输出**——精确显示创建了什么及其对工作流的影响

### 设置配置（手动创建）

用户也可以手动创建配置（或在设置期间跳过，稍后添加）：

```bash
# 手动创建配置文件
cat > openspec/config.yaml << 'EOF'
schema: spec-driven

context: |
  技术栈：TypeScript, React, Node.js
  我们遵循 docs/api.md 中记录的 REST 约定
  所有变更需考虑向后兼容性

rules:
  proposal:
    - 必须包含回滚计划
    - 必须识别受影响的团队
  specs:
    - 使用 Given/When/Then 格式
EOF
```

### 对工作流的影响

一旦创建了配置，它以三种方式影响实验性工作流：

**1. 默认模式选择**

```bash
# 配置前：必须指定模式
/opsx:new my-feature --schema spec-driven

# 配置后（含 schema: spec-driven）：模式自动确定
/opsx:new my-feature
# 自动使用配置中的 spec-driven

# 覆盖仍可工作
/opsx:new my-feature --schema tdd
# 使用 tdd，忽略配置
```

**2. 上下文注入（所有 artifact）**

```bash
# 获取任何 artifact 的指令
openspec instructions proposal --change my-feature

# 输出现在包含项目上下文：
<context>
技术栈：TypeScript, React, Node.js, PostgreSQL
API 风格：RESTful，记录在 docs/api-conventions.md 中
测试：Jest + React Testing Library
我们重视所有公共 API 的向后兼容性
</context>

<template>
[模式的 proposal 模板]
</template>
```

上下文出现在**所有 artifact** 的指令中（proposal, specs, design, tasks）。

**3. 规则注入（每个 artifact）**

```bash
# 获取已配置规则的 artifact 的指令
openspec instructions specs --change my-feature

# 输出包含 artifact 特定的规则：
<context>
[项目上下文]
</context>

<rules>
- 使用 Given/When/Then 格式编写场景
- 在发明新模式之前参考现有模式
</rules>

<template>
[模式的 specs 模板]
</template>
```

规则仅出现在为其配置的**特定 artifact** 中。

**没有规则的 artifact**（例如 design, tasks）不会获得 `<rules>` 章节：

```bash
openspec instructions design --change my-feature
# 输出：仅有 <context> 然后是 <template>（无 rules）
```

### 团队共享

```bash
# 提交配置
git add openspec/config.yaml
git commit -m "添加包含上下文和规则的项目配置"

# 每个人自动获得相同的上下文和规则
```

## 实现说明

### 要修改/创建的文件

| 文件 | 变更 |
|------|------|
| `src/core/project-config.ts` | **新文件：** 类型、解析、读取、验证辅助函数 |
| `src/core/artifact-graph/instruction-loader.ts` | 注入上下文（所有 artifact）和规则（每个 artifact） |
| `src/utils/change-utils.ts` | 在 `createChange()` 中使用配置模式作为默认值 |
| `src/utils/change-metadata.ts` | 更新 `resolveSchemaForChange()` 以检查配置 |
| `src/commands/artifact-workflow.ts` | 扩展 `artifactExperimentalSetupCommand()` 以提示创建配置 |
| `src/core/config-prompts.ts` | **新文件：** 配置创建的交互式提示（可复用） |

### 配置位置

始终位于项目根目录的 `./openspec/config.yaml`。为简单起见，不使用 XDG/全局配置。

### 解析顺序更新

模式选择顺序变为：

```
1. --schema CLI 标志                    # 显式覆盖
2. change 目录中的 .openspec.yaml       # Change 级别的绑定
3. openspec/config.yaml schema 字段     # 项目默认值（新增）
4. "spec-driven"                        # 硬编码回退
```

### 验证

- `schema` 必须是有效的模式名称（在解析中存在）
- `context` 必须是字符串
- `rules` 必须是键为字符串（artifact ID）、值为数组的对象
- `rules` 中未知的 artifact ID 应警告而非报错（允许向前兼容）

### 实验性设置集成

**对 `src/commands/artifact-workflow.ts` 中 `artifactExperimentalSetupCommand()` 的变更：**

在创建技能和命令之后，设置命令将：

1. **显示章节标题：**
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📋 项目配置（可选）
   配置 OpenSpec 工作流的项目默认值。
   ```

2. **提示：创建配置？**
   - 是/否提示，默认"是"
   - 如果否 → 跳过整个配置章节，显示使用说明
   - 如果是 → 继续详细提示

3. **提示：模式选择**
   - 使用 `listSchemasWithInfo()` 获取可用模式
   - 显示每个模式的描述和 artifact 流程
   - 默认选择第一个模式（通常是 "spec-driven"）

4. **提示：项目上下文**
   - 多行输入（或编辑器，如果可用）
   - 显示示例："技术栈、约定、风格指南"
   - 允许为空（跳过）

5. **提示：每个 artifact 的规则**
   - 是/否提示，默认"否"（规则不太常见）
   - 如果是：
     - 显示所选模式的 artifact 清单
     - 为每个选中的 artifact，提示输入规则（逐行输入）
     - 空行完成每个 artifact 的规则

6. **创建并验证配置：**
   - 从输入构建 `ProjectConfig` 对象
   - 使用 Zod 模式验证
   - 使用 YAML 序列化器写入 `openspec/config.yaml`
   - 如果验证失败，显示错误并要求重试或跳过

7. **显示成功摘要：**
   - 创建的配置路径
   - 摘要：使用的模式、添加上下文（行数）、规则数量
   - 展示配置如何影响工作流的使用示例
   - 建议将配置提交到 git

**错误处理：**
- 无效的模式选择 → 显示带有模糊匹配建议的可用模式，重试
- 上下文过大（>50KB）→ 拒绝并报错，要求减小大小
- 规则引用无效 artifact → 警告但继续（向前兼容）
- 文件写入失败 → 显示错误，建议手动创建
- 配置已存在 → 显示消息，跳过配置章节，继续设置
- 用户取消（Ctrl+C）→ 记录"配置创建已取消"，继续执行设置的其余部分（技能/命令已创建）

**如果配置已存在：**

当 `openspec/config.yaml` 已存在时：

```bash
$ openspec artifact-experimental-setup

[技能和命令已创建...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 项目配置

ℹ️  openspec/config.yaml 已存在。跳过配置创建。

   要更新配置，手动编辑 openspec/config.yaml 或：
   1. 删除 openspec/config.yaml
   2. 重新运行 openspec artifact-experimental-setup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[设置的其余输出...]
```

这可以防止意外覆盖用户的配置。

**实现方法：**

创建单独的 `src/core/config-prompts.ts` 模块：

```typescript
export interface ConfigPromptResult {
  createConfig: boolean;
  schema?: string;
  context?: string;
  rules?: Record<string, string[]>;
}

export async function promptForConfig(): Promise<ConfigPromptResult> {
  // 使用 inquirer 或类似的提示逻辑
  // 返回用于配置创建的结构化结果
  // 在 Ctrl+C 时抛出 ExitPromptError（由调用方处理）
}
```

**设置命令中的 Ctrl+C 处理：**

```typescript
try {
  const configResult = await promptForConfig();
  if (configResult.createConfig) {
    writeConfigFile(configResult);
    console.log('✓ 已创建 openspec/config.yaml');
  }
} catch (error) {
  if (error.name === 'ExitPromptError') {
    console.log('\nℹ️  配置创建已取消');
    console.log('   技能和命令已创建');
    console.log('   稍后重新运行设置以创建配置');
    // 继续执行设置的其余部分（非致命错误）
  } else {
    throw error; // 重新抛出意外错误
  }
}
```

这使得提示可以独立于设置命令进行复用和测试。

### 依赖项

**交互式提示库：**

实验性设置命令需要一个交互式提示库用于配置创建流程。选项：

1. **@inquirer/prompts**（推荐）
   - 现代化、可 tree-shake、TypeScript 优先
   - 单独导入：`@inquirer/input`、`@inquirer/confirm`、`@inquirer/checkbox`、`@inquirer/editor`
   - 已在 OpenSpec 中使用（如果没有，轻量级添加）

2. **inquirer**（经典）
   - 更成熟，更大的生态系统
   - 较大的打包体积
   - 包含所有提示类型的单个包

**所需提示：**
- `confirm` - "创建配置？" "添加规则？"
- `select` - 带描述的模式选择
- `editor` 或多行 `input` - 项目上下文
- `checkbox` - 规则的 artifact 选择
- `input`（重复） - 规则输入（逐行）

**替代方案（无依赖）：**

使用 Node 内置的 `readline` 实现基本提示：
- 需要编写更多代码
- 用户体验不够精致（无箭头键导航、复选框选择）
- 零依赖成本

**建议：** 使用 `@inquirer/prompts` 以获得最佳用户体验。配置设置是一次性操作，用户体验很重要。

### YAML 序列化

配置创建需要 YAML 序列化：

- **yaml** 包（已是依赖项）
- 使用 `yaml.stringify()` 写入配置
- 使用 `|` 字面风格保留多行字符串
- 格式：2 空格缩进，除非需要否则不使用引号

示例：
```typescript
import { stringify } from 'yaml';

const config = {
  schema: 'spec-driven',
  context: '多行\n上下文\n内容',
  rules: { proposal: ['规则 1', '规则 2'] }
};

const yamlContent = stringify(config, {
  indent: 2,
  defaultStringType: 'QUOTE_DOUBLE',
  defaultKeyType: 'PLAIN',
});
// 多行上下文将自动使用 | 字面风格
```

## 测试注意事项

**核心配置功能：**
- 创建包含所有字段的配置（schema, context, rules），验证解析
- 创建最小配置（仅 schema），验证解析
- 验证上下文出现在所有 artifact 的指令输出中
- 验证规则仅出现在匹配的 artifact 中（而非所有 artifact）
- 验证配置中的模式用于新 change
- 验证 CLI `--schema` 标志覆盖配置
- 验证 change 的 `.openspec.yaml` 覆盖配置
- 验证缺失配置时的优雅处理（回退到默认值）
- 验证无效 YAML 语法的优雅处理（警告，回退）
- 验证无效模式的优雅处理（警告，显示有效模式）
- 验证规则中的未知 artifact ID 发出警告但不中断

**模式解析优先级：**
- 测试模式解析的所有四个级别：
  1. CLI 标志 `--schema`（最高优先级）
  2. Change 元数据 `.openspec.yaml`
  3. 项目配置 `openspec/config.yaml`
  4. 硬编码默认值 "spec-driven"（最低优先级）
- 验证每个级别正确覆盖较低级别

**上下文和规则注入：**
- 验证上下文注入使用 `<context>` XML 风格标签
- 验证规则注入使用带项目符号的 `<rules>` XML 风格标签
- 验证注入顺序：`<context>` → `<rules>` → `<template>`
- 验证多行上下文被保留
- 验证上下文/规则中的特殊字符不被转义
- 验证空的上下文/规则不创建标签

**实验性设置集成：**
- 测试 `artifact-experimental-setup`，用户跳过配置创建
- 测试 `artifact-experimental-setup`，最小配置（仅 schema）
- 测试 `artifact-experimental-setup`，完整配置（schema + context + rules）
- 测试从可用模式中选择模式
- 测试多行上下文输入
- 测试每个 artifact 的规则提示
- 测试 artifact 选择（复选框）
- 测试配置创建期间的验证错误
- 测试文件写入错误（权限等）
- 验证创建的配置可以被 `readProjectConfig()` 解析
- 验证成功摘要显示正确的信息

**边界情况：**
- 配置文件存在但为空 → 视为无效，警告
- 配置是 `.yml` 扩展名而非 `.yaml` → 两者都接受
- `.yaml` 和 `.yml` 同时存在 → 优先使用 `.yaml`
- 上下文包含 YAML 特殊字符 → 在输出中正确转义
- 规则数组包含空字符串 → 过滤掉或警告
- 模式引用不存在的模式 → 报错并给出建议
- 配置在子目录中（非项目根目录）→ 未找到，使用默认值

**向后兼容性：**
- 没有配置的现有项目继续工作
- 使用 `.openspec.yaml` 元数据的现有 change 不受配置影响
- 在现有项目中添加配置不会中断进行中的 change

**集成测试：**
- 创建配置 → 创建 change → 验证使用的模式
- 创建配置 → 获取指令 → 验证上下文已注入
- 创建配置 → 获取指令 → 验证规则已注入
- 更新配置 → 验证变更立即反映（无缓存）
- 运行 `artifact-experimental-setup` → 创建配置 → 创建 change → 验证流程

## 相关变更

- **project-local-schemas**：使 `schema: my-workflow` 可以引用项目本地模式

## 附录：完整配置模式

```typescript
import { z } from 'zod';

// Zod 模式同时作为运行时验证和文档
// 类型从模式推断以获得类型安全
export const ProjectConfigSchema = z.object({
  // 必填：使用哪个模式（例如 "spec-driven", "tdd"，或项目本地模式名称）
  schema: z.string().min(1).describe('要使用的工作流模式（例如 "spec-driven", "tdd"）'),

  // 可选：项目上下文（注入到所有 artifact 指令中）
  // 最大大小：50KB（解析时强制）
  context: z.string().optional().describe('注入到所有 artifact 指令的项目上下文'),

  // 可选：每个 artifact 的规则（对模式内置指导的补充）
  rules: z.record(
    z.string(),           // artifact ID
    z.array(z.string())   // 规则列表
  ).optional().describe('每个 artifact 的规则，以 artifact ID 为键'),
});

export type ProjectConfig = z.infer<typeof ProjectConfigSchema>;

// 注意：解析使用单个字段的 safeParse() 实现弹性错误处理
// 无效字段会被警告，但不阻止其他字段加载
```

## 附录：视觉摘要

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   用户提供：                                                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ openspec/config.yaml                                    │   │
│   │                                                         │   │
│   │ schema: spec-driven                                     │   │
│   │ context: "我们使用 React, TypeScript..."                 │   │
│   │ rules:                                                  │   │
│   │   proposal: [...]                                       │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ OpenSpec 合并：                                           │   │
│   │                                                         │   │
│   │   模式（spec-driven）                                    │   │
│   │   + 用户的上下文                                          │   │
│   │   + 用户的规则                                            │   │
│   │   ─────────────────────────                               │   │
│   │   = 增强指令                                              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 智能体看到（针对 proposal artifact）：                   │   │
│   │                                                         │   │
│   │ <context>                                               │   │
│   │ 我们使用 React, TypeScript...                           │   │
│   │ </context>                                              │   │
│   │                                                         │   │
│   │ <rules>                                                 │   │
│   │ - 包含回滚计划                                           │   │
│   │ - 识别受影响的团队                                       │   │
│   │ </rules>                                                │   │
│   │                                                         │   │
│   │ <template>                                              │   │
│   │ [内置 proposal 模板]                                    │   │
│   │ </template>                                             │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
