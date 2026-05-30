# 自定义

OpenSpec 提供三个级别的自定义：

| 级别 | 功能 | 最适合 |
|-------|--------------|----------|
| **项目配置** | 设置默认值，注入上下文/规则 | 大多数团队 |
| **自定义 Schema** | 定义自己的工作流产物 | 有独特流程的团队 |
| **全局覆盖** | 在所有项目中共享 schema | 高级用户 |

---

## 项目配置

`openspec/config.yaml` 文件是为您的团队自定义 OpenSpec 最简单的方式。它允许您：

- **设置默认 schema** - 在每个命令上跳过 `--schema`
- **注入项目上下文** - AI 看到您的技术栈、约定等
- **添加按产物规则** - 特定产物的自定义规则

### 快速设置

```bash
openspec init
```

这会引导您交互式地创建配置。或者手动创建：

```yaml
# openspec/config.yaml
schema: spec-driven

context: |
  技术栈：TypeScript, React, Node.js, PostgreSQL
  API 风格：RESTful，在 docs/api.md 中有文档
  测试：Jest + React Testing Library
  我们重视所有公共 API 的向后兼容性

rules:
  proposal:
    - 包括回滚计划
    - 标识受影响的团队
  specs:
    - 使用 Given/When/Then 格式
    - 在发明新模式之前参考现有模式
```

### 工作原理

**默认 schema：**

```bash
# 没有配置时
openspec new change my-feature --schema spec-driven

# 有配置时 - schema 自动使用
openspec new change my-feature
```

**上下文和规则注入：**

在生成任何产物时，您的上下文和规则会被注入到 AI 提示中：

```xml
<context>
技术栈：TypeScript, React, Node.js, PostgreSQL
...
</context>

<rules>
- 包括回滚计划
- 标识受影响的团队
</rules>

<template>
[Schema 的内置模板]
</template>
```

- **上下文**出现在所有产物中
- **规则**仅出现在匹配的产物中

### Schema 解析顺序

当 OpenSpec 需要 schema 时，它按此顺序检查：

1. CLI 标志：`--schema <name>`
2. 变更元数据（变更文件夹中的 `.openspec.yaml`）
3. 项目配置（`openspec/config.yaml`）
4. 默认（`spec-driven`）

---

## 自定义 Schema

当项目配置不足时，创建具有完全自定义工作流的自有 schema。自定义 schema 位于项目的 `openspec/schemas/` 目录中，并与您的代码一起进行版本控制。

```text
your-project/
├── openspec/
│   ├── config.yaml        # 项目配置
│   ├── schemas/           # 自定义 schema 存放位置
│   │   └── my-workflow/
│   │       ├── schema.yaml
│   │       └── templates/
│   └── changes/           # 您的变更
└── src/
```

### Fork 现有 Schema

自定义的最快方式是 fork 内置 schema：

```bash
openspec schema fork spec-driven my-workflow
```

这会将整个 `spec-driven` schema 复制到 `openspec/schemas/my-workflow/`，您可以在其中自由编辑。

**您将获得：**

```text
openspec/schemas/my-workflow/
├── schema.yaml           # 工作流定义
└── templates/
    ├── proposal.md       # proposal 产物的模板
    ├── spec.md           # specs 的模板
    ├── design.md         # design 的模板
    └── tasks.md          # tasks 的模板
```

现在编辑 `schema.yaml` 来更改工作流，或编辑模板来更改 AI 生成的内容。

### 从零创建 Schema

对于完全全新的工作流：

```bash
# 交互式
openspec schema init research-first

# 非交互式
openspec schema init rapid \
  --description "快速迭代工作流" \
  --artifacts "proposal,tasks" \
  --default
```

### Schema 结构

Schema 定义工作流中的产物及其相互依赖关系：

```yaml
# openspec/schemas/my-workflow/schema.yaml
name: my-workflow
version: 1
description: 我的团队的自定义工作流

artifacts:
  - id: proposal
    generates: proposal.md
    description: 初始提案文档
    template: proposal.md
    instruction: |
      创建一个解释为何需要此变更的提案。
      关注问题，而非解决方案。
    requires: []

  - id: design
    generates: design.md
    description: 技术设计
    template: design.md
    instruction: |
      创建解释如何实施的设计文档。
    requires:
      - proposal    # 在 proposal 存在之前无法创建设计

  - id: tasks
    generates: tasks.md
    description: 实施检查清单
    template: tasks.md
    requires:
      - design

apply:
  requires: [tasks]
  tracks: tasks.md
```

**关键字段：**

| 字段 | 用途 |
|-------|---------|
| `id` | 唯一标识符，用于命令和规则 |
| `generates` | 输出文件名（支持 glob 模式，如 `specs/**/*.md`） |
| `template` | `templates/` 目录中的模板文件 |
| `instruction` | 创建此产物的 AI 指令 |
| `requires` | 依赖关系——哪些产物必须首先存在 |

### 模板

模板是指导 AI 的 Markdown 文件。它们在创建该产物时被注入到提示中。

```markdown
<!-- templates/proposal.md -->
## 原因

<!-- 解释此变更的动机。解决了什么问题？ -->

## 变更内容

<!-- 描述将发生什么变化。具体说明新功能或修改内容。 -->

## 影响

<!-- 受影响的代码、API、依赖、系统 -->
```

模板可以包含：
- AI 应填写的章节标题
- 带有 AI 指导的 HTML 注释
- 显示预期结构的示例格式

### 验证您的 Schema

在使用自定义 schema 之前，请验证它：

```bash
openspec schema validate my-workflow
```

这会检查：
- `schema.yaml` 语法正确
- 所有引用的模板都存在
- 没有循环依赖
- 产物 ID 有效

### 使用您的自定义 Schema

一旦创建，使用您的 schema：

```bash
# 在命令中指定
openspec new change feature --schema my-workflow

# 或在 config.yaml 中设置为默认
schema: my-workflow
```

### 调试 Schema 解析

不确定正在使用哪个 schema？用以下命令检查：

```bash
# 查看特定 schema 从哪里解析
openspec schema which my-workflow

# 列出所有可用 schema
openspec schema which --all
```

输出显示它是来自您的项目、用户目录还是包：

```text
Schema: my-workflow
来源：项目
路径：/path/to/project/openspec/schemas/my-workflow
```

---

> **注意：** OpenSpec 还支持用户级 schema，位于 `~/.local/share/openspec/schemas/`，用于在项目间共享，但推荐使用项目级 schema（在 `openspec/schemas/` 中），因为它们与代码一起进行版本控制。

---

## 示例

### 快速迭代工作流

适用于快速迭代的最小工作流：

```yaml
# openspec/schemas/rapid/schema.yaml
name: rapid
version: 1
description: 最小开销的快速迭代

artifacts:
  - id: proposal
    generates: proposal.md
    description: 快速提案
    template: proposal.md
    instruction: |
      为此变更创建一个简短的提案。
      关注什么和为什么，跳过详细 specs。
    requires: []

  - id: tasks
    generates: tasks.md
    description: 实施检查清单
    template: tasks.md
    requires: [proposal]

apply:
  requires: [tasks]
  tracks: tasks.md
```

### 添加审查产物

Fork 默认 schema 并添加审查步骤：

```bash
openspec schema fork spec-driven with-review
```

然后编辑 `schema.yaml` 添加：

```yaml
  - id: review
    generates: review.md
    description: 实施前审查检查清单
    template: review.md
    instruction: |
      基于设计创建审查检查清单。
      包括安全性、性能和测试方面的考虑。
    requires:
      - design

  - id: tasks
    # ... 现有 tasks 配置 ...
    requires:
      - specs
      - design
      - review    # 现在 tasks 也需要审查
```

---

## 社区 Schema

OpenSpec 还支持通过独立仓库分发的社区维护 schema。这些提供有观点的工作流，将 OpenSpec 与其他工具或系统集成，类似于 [github/spec-kit 的社区扩展目录](https://github.com/github/spec-kit/tree/main/extensions) 对 spec-kit 的工作方式。

社区 schema 不包含在 OpenSpec 核心中——它们位于自己的仓库中，有自己的发布节奏。使用时，将 schema 包复制到项目的 `openspec/schemas/<schema-name>/` 目录（每个仓库的 README 都有安装说明）。

| Schema | 维护者 | 仓库 | 描述 |
|--------|-----------|-----------|-------------|
| `superpowers-bridge` | @JiangWay | [JiangWay/openspec-schemas](https://github.com/JiangWay/openspec-schemas/tree/main/superpowers-bridge) | 将 OpenSpec 的产物治理与 [obra/superpowers](https://github.com/obra/superpowers) 执行 skills（头脑风暴、编写计划、通过子 agent 进行 TDD、代码审查、收尾）集成。新增一个证据优先的 `retrospective` 产物，填补 Superpowers 未原生覆盖的空白。 |

> 想贡献社区 schema？请提交一个 Issue，附上您的仓库链接，或提交 PR 在此表中添加一行。

---

## 另请参阅

- [CLI 参考：Schema 命令](cli.md#schema-commands) - 完整的命令文档
