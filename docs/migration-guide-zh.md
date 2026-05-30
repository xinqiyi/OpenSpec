# 迁移到 OPSX

本指南帮助您从旧版 OpenSpec 工作流过渡到 OPSX。迁移过程设计为平滑过渡——您现有的工作将被保留，新系统提供更多灵活性。

## 有哪些变化？

OPSX 用灵活的、基于行动的方法取代了旧有的阶段锁定工作流。以下是关键变化：

| 方面 | 旧版 | OPSX |
|--------|--------|------|
| **命令** | `/openspec:proposal`, `/openspec:apply`, `/openspec:archive` | 默认：`/opsx:propose`, `/opsx:apply`, `/opsx:sync`, `/opsx:archive`（扩展工作流命令可选） |
| **工作流** | 一次性创建所有产物 | 增量创建或一次性创建——您的选择 |
| **回退** | 笨拙的阶段门控 | 自然——随时更新任何产物 |
| **自定义** | 固定结构 | Schema 驱动，完全可定制 |
| **配置** | 带标记的 `CLAUDE.md` + `project.md` | `openspec/config.yaml` 中的干净配置 |

**理念的转变：** 工作不是线性的。OPSX 不再假装它是线性的。

---

## 开始之前

### 您现有的工作是安全的

迁移过程以保留为首要考虑：

- **`openspec/changes/` 中的活跃变更** — 完全保留。您可以使用 OPSX 命令继续它们。
- **已归档的变更** — 不受影响。您的历史记录完好无损。
- **`openspec/specs/` 中的主 specs** — 不受影响。这是您的唯一真相来源。
- **您在 CLAUDE.md、AGENTS.md 等中的内容** — 保留。仅移除 OpenSpec 标记块；您写的所有内容都保留。

### 哪些内容被移除

仅移除正在被替换的 OpenSpec 管理的文件：

| 内容 | 原因 |
|------|------|
| 旧版斜杠命令目录/文件 | 被新的 skills 系统取代 |
| `openspec/AGENTS.md` | 过时的工作流触发器 |
| `CLAUDE.md`、`AGENTS.md` 等中的 OpenSpec 标记 | 不再需要 |

**各工具的旧版命令位置**（示例——您的工具可能不同）：

- Claude Code：`.claude/commands/openspec/`
- Cursor：`.cursor/commands/openspec-*.md`
- Windsurf：`.windsurf/workflows/openspec-*.md`
- Cline：`.clinerules/workflows/openspec-*.md`
- Roo：`.roo/commands/openspec-*.md`
- GitHub Copilot：`.github/prompts/openspec-*.prompt.md`（仅限 IDE 扩展；Copilot CLI 不支持）
- 以及其他（Augment, Continue, Amazon Q 等）

迁移会检测您配置了哪些工具并清理其旧版文件。

移除列表可能看起来很长，但这些都是 OpenSpec 最初创建的文件。您自己的内容永远不会被删除。

### 需要您注意的内容

有一个文件需要手动迁移：

**`openspec/project.md`** — 此文件不会自动删除，因为它可能包含您编写的项目上下文。您需要：

1. 审查其内容
2. 将有价值的上下文移至 `openspec/config.yaml`（参见下方指南）
3. 准备好后删除该文件

**为什么我们做了这个更改：**

旧的 `project.md` 是被动的——agent 可能会读它，也可能不会，或者读了之后忘记。我们发现可靠性不一致。

新的 `config.yaml` 上下文会被**主动注入到每个 OpenSpec 规划请求中**。这意味着您的项目约定、技术栈和规则在 AI 创建产物时始终存在。可靠性更高。

**权衡：**

因为上下文会被注入到每个请求中，您需要保持简洁。关注真正重要的内容：
- 技术栈和关键约定
- AI 需要了解的非显而易见约束
- 之前经常被忽略的规则

不必追求完美。我们仍在学习什么最有效，并且随着实验的进行，我们会改进上下文注入的工作方式。

---

## 运行迁移

`openspec init` 和 `openspec update` 都会检测旧版文件并引导您完成相同的清理过程。根据您的情况选择：

- 新安装默认使用 `core` 配置（`propose`、`explore`、`apply`、`sync`、`archive`）。
- 已迁移的安装会通过必要时写入 `custom` 配置来保留您先前安装的工作流。

### 使用 `openspec init`

如果您想添加新工具或重新配置已设置的工具，运行此命令：

```bash
openspec init
```

init 命令检测旧版文件并引导您完成清理：

```
正在升级到新版 OpenSpec

OpenSpec 现在使用 agent skills，这是编码 agent 领域的新兴标准。
这简化了您的设置，同时保持一切正常工作。

要移除的文件
没有需要保留的用户内容：
  • .claude/commands/openspec/
  • openspec/AGENTS.md

要更新的文件
OpenSpec 标记将被移除，您的内容将保留：
  • CLAUDE.md
  • AGENTS.md

需要您的注意
  • openspec/project.md
    我们不会删除此文件。它可能包含有用的项目上下文。

    新的 openspec/config.yaml 有一个"context:"部分用于规划
    上下文。它会被包含在每个 OpenSpec 请求中，并且比
    旧的 project.md 方法更可靠。

    请审查 project.md，将有价值的内容移动到 config.yaml 的 context
    部分，然后准备好后删除该文件。

? 升级并清理旧版文件？(Y/n)
```

**当您确认时会发生什么：**

1. 旧版斜杠命令目录被移除
2. OpenSpec 标记从 `CLAUDE.md`、`AGENTS.md` 等中剥离（您的内容保留）
3. `openspec/AGENTS.md` 被删除
4. 新的 skills 被安装到 `.claude/skills/`
5. `openspec/config.yaml` 以默认 schema 创建

### 使用 `openspec update`

如果您只想迁移并将现有工具刷新到最新版本，运行此命令：

```bash
openspec update
```

update 命令也会检测并清理旧版产物，然后刷新生成的 skills/命令以匹配您当前的配置和交付方式设置。

### 非交互式 / CI 环境

对于脚本化迁移：

```bash
openspec init --force --tools claude
```

`--force` 标志跳过提示并自动接受清理。

---

## 将 project.md 迁移到 config.yaml

旧的 `openspec/project.md` 是一个用于项目上下文的自由格式 Markdown 文件。新的 `openspec/config.yaml` 是结构化的，并且关键的是——**会被注入到每个规划请求中**，这样您的约定在 AI 工作时始终存在。

### 之前（project.md）

```markdown
# 项目上下文

这是一个使用 React 和 Node.js 的 TypeScript monorepo。
我们使用 Jest 进行测试，并遵循严格的 ESLint 规则。
我们的 API 是 RESTful 的，在 docs/api.md 中有文档。

## 约定

- 所有公共 API 必须保持向后兼容
- 新功能应包含测试
- 使用 Given/When/Then 格式编写规范
```

### 之后（config.yaml）

```yaml
schema: spec-driven

context: |
  技术栈：TypeScript, React, Node.js
  测试：Jest 与 React Testing Library
  API：RESTful，在 docs/api.md 中有文档
  我们为所有公共 API 保持向后兼容性

rules:
  proposal:
    - 对风险变更包含回滚计划
  specs:
    - 使用 Given/When/Then 格式编写场景
    - 在发明新模式之前参考现有模式
  design:
    - 对复杂流程包含时序图
```

### 主要区别

| project.md | config.yaml |
|------------|-------------|
| 自由格式 Markdown | 结构化 YAML |
| 单一文本块 | 独立的上下文和按产物规则 |
| 不清楚何时使用 | 上下文出现在所有产物中；规则仅出现在匹配的产物中 |
| 无 schema 选择 | 显式 `schema:` 字段设置默认工作流 |

### 保留什么，舍弃什么

迁移时要有选择性。问自己："AI 在*每个*规划请求中都需要这个吗？"

**适合放入 `context:` 的内容**
- 技术栈（语言、框架、数据库）
- 关键架构模式（monorepo、微服务等）
- 非显而易见的约束（"我们不能使用 X 库，因为……"）
- 经常被忽略的关键约定

**改为放入 `rules:`**
- 产物特定格式要求（"在 specs 中使用 Given/When/Then"）
- 审查标准（"proposal 必须包含回滚计划"）
- 这些仅在匹配的产物中出现，保持其他请求更简洁

**完全省略**
- AI 已经知道的一般最佳实践
- 可以概括的冗长解释
- 不影响当前工作的历史背景

### 迁移步骤

1. **创建 config.yaml**（如果 init 尚未创建）：
   ```yaml
   schema: spec-driven
   ```

2. **添加您的上下文**（保持简洁——这会被放入每个请求）：
   ```yaml
   context: |
     在此处放置您的项目背景。
     关注 AI 真正需要知道的内容。
   ```

3. **添加按产物规则**（可选）：
   ```yaml
   rules:
     proposal:
       - 您的 proposal 特定指南
     specs:
       - 您的 spec 编写规则
   ```

4. **删除 project.md**，一旦您已经移动了所有有用的内容。

**不要想太多。** 从基本要素开始，然后迭代。如果您注意到 AI 遗漏了重要内容，添加它。如果上下文感觉臃肿，修剪它。这是一个活文档。

### 需要帮助？使用这个提示

如果您不确定如何提炼您的 project.md，请询问您的 AI 助手：

```
我正在从 OpenSpec 的旧版 project.md 迁移到新的 config.yaml 格式。

以下是我当前的 project.md：
[粘贴您的 project.md 内容]

请帮我创建一个 config.yaml，包含：
1. 一个简洁的 `context:` 部分（这会被注入到每个规划请求中，所以保持紧凑——关注技术栈、关键约束和经常被忽略的约定）
2. 如果某些内容特定于某个产物，放入 `rules:` 部分（例如，"使用 Given/When/Then" 属于 specs 规则，而非全局上下文）

省略任何 AI 模型已经知道的通用内容。对简洁性要毫不留情。
```

AI 将帮助您识别哪些是必需的，哪些可以删减。

---

## 新命令

命令可用性取决于配置：

**默认（`core` 配置）：**

| 命令 | 用途 |
|---------|---------|
| `/opsx:propose` | 一步创建变更并生成规划产物 |
| `/opsx:explore` | 无结构地思考想法 |
| `/opsx:apply` | 根据 tasks.md 实施任务 |
| `/opsx:archive` | 最终确定并归档变更 |

**扩展工作流（自定义选择）：**

| 命令 | 用途 |
|---------|---------|
| `/opsx:new` | 启动新的变更 scaffold |
| `/opsx:continue` | 创建下一个产物（一次一个） |
| `/opsx:ff` | 快进——一次性创建规划产物 |
| `/opsx:verify` | 验证实施是否匹配 specs |
| `/opsx:sync` | 将 delta specs 合并到主 specs |
| `/opsx:bulk-archive` | 一次归档多个变更 |
| `/opsx:onboard` | 引导式端到端入职工作流 |

使用 `openspec config profile` 启用扩展命令，然后运行 `openspec update`。

### 从旧版命令映射

| 旧版 | OPSX 对应命令 |
|--------|-----------------|
| `/openspec:proposal` | `/opsx:propose`（默认）或 `/opsx:new` 然后 `/opsx:ff`（扩展） |
| `/openspec:apply` | `/opsx:apply` |
| `/openspec:archive` | `/opsx:archive` |

### 新能力

这些能力是扩展工作流命令集的一部分。

**粒度产物创建：**
```
/opsx:continue
```
根据依赖关系一次创建一个产物。当您想要审查每一步时使用。

**探索模式：**
```
/opsx:explore
```
在提交变更之前与伙伴一起思考想法。

---

## 理解新架构

### 从阶段锁定到流动

旧版工作流强制线性推进：

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    规划     │ ───► │    实施     │ ───► │    归档     │
│    阶段     │      │    阶段     │      │    阶段     │
└──────────────┘      └──────────────┘      └──────────────┘

如果在实施阶段发现设计错误？
没办法。阶段门控不会让你轻松回退。
```

OPSX 使用行动，而非阶段：

```
         ┌───────────────────────────────────────────────┐
         │              行动（而非阶段）                  │
         │                                               │
         │     new ◄──► continue ◄──► apply ◄──► archive │
         │      │          │           │             │   │
         │      └──────────┴───────────┴─────────────┘   │
         │                   任意顺序                     │
         └───────────────────────────────────────────────┘
```

### 依赖关系图

产物形成一个有向图。依赖关系是使能器，而非门控：

```
                        proposal
                       (根节点)
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
           specs                       design
        (需要：                    (需要：
         proposal)                   proposal)
              │                           │
              └─────────────┬─────────────┘
                            │
                            ▼
                         tasks
                     (需要：
                     specs, design)
```

当您运行 `/opsx:continue` 时，它会检查什么已就绪并提供下一个产物。您也可以按任意顺序创建多个就绪的产物。

### Skills 与命令

旧版系统使用工具特定的命令文件：

```
.claude/commands/openspec/
├── proposal.md
├── apply.md
└── archive.md
```

OPSX 使用新兴的 **skills** 标准：

```
.claude/skills/
├── openspec-explore/SKILL.md
├── openspec-new-change/SKILL.md
├── openspec-continue-change/SKILL.md
├── openspec-apply-change/SKILL.md
└── ...
```

Skills 被多个 AI 编码工具识别，并提供更丰富的元数据。

---

## 继续现有变更

您进行中的变更可以与 OPSX 命令无缝配合。

**有来自旧版工作流的活跃变更？**

```
/opsx:apply add-my-feature
```

OPSX 读取现有产物并从上次中断的地方继续。

**想为现有变更添加更多产物？**

```
/opsx:continue add-my-feature
```

显示根据已存在的内容可以创建什么。

**需要查看状态？**

```bash
openspec status --change add-my-feature
```

---

## 新配置系统

### config.yaml 结构

```yaml
# 必需：新变更的默认 schema
schema: spec-driven

# 可选：项目上下文（最大 50KB）
# 注入到所有产物指令中
context: |
  您的项目背景、技术栈、
  约定和约束。

# 可选：按产物规则
# 仅注入到匹配的产物中
rules:
  proposal:
    - 包括回滚计划
  specs:
    - 使用 Given/When/Then 格式
  design:
    - 记录回退策略
  tasks:
    - 分解为最大 2 小时的块
```

### Schema 解析

在确定要使用的 schema 时，OPSX 按顺序检查：

1. **CLI 标志**：`--schema <name>`（最高优先级）
2. **变更元数据**：变更目录中的 `.openspec.yaml`
3. **项目配置**：`openspec/config.yaml`
4. **默认**：`spec-driven`

### 可用 Schema

| Schema | 产物 | 最适合 |
|--------|-----------|----------|
| `spec-driven` | proposal → specs → design → tasks | 大多数项目 |

列出所有可用 schema：

```bash
openspec schemas
```

### 自定义 Schema

创建您自己的工作流：

```bash
openspec schema init my-workflow
```

或 fork 一个现有的：

```bash
openspec schema fork spec-driven my-workflow
```

有关详细信息，请参阅[自定义](customization.md)。

---

## 故障排除

### "在非交互模式下检测到旧版文件"

您在 CI 或非交互环境中运行。使用：

```bash
openspec init --force
```

### 迁移后命令未显示

重新启动您的 IDE。Skills 在启动时被检测。

### "规则中的未知产物 ID"

检查您的 `rules:` 键是否与您的 schema 的产物 ID 匹配：

- **spec-driven**：`proposal`、`specs`、`design`、`tasks`

运行此命令查看有效的产物 ID：

```bash
openspec schemas --json
```

### 配置未生效

1. 确保文件位于 `openspec/config.yaml`（不是 `.yml`）
2. 验证 YAML 语法
3. 配置更改立即生效——无需重启

### project.md 未迁移

系统有意保留 `project.md`，因为它可能包含您的自定义内容。手动审查，将有用部分移至 `config.yaml`，然后删除它。

### 想看哪些内容会被清理？

运行 init 并拒绝清理提示——您将看到完整的检测摘要，而不进行任何更改。

---

## 快速参考

### 迁移后的文件

```
project/
├── openspec/
│   ├── specs/                    # 未更改
│   ├── changes/                  # 未更改
│   │   └── archive/              # 未更改
│   └── config.yaml               # 新增：项目配置
├── .claude/
│   └── skills/                   # 新增：OPSX skills
│       ├── openspec-propose/     # 默认 core 配置
│       ├── openspec-explore/
│       ├── openspec-apply-change/
│       ├── openspec-sync-specs/
│       └── ...                   # 扩展配置添加 new/continue/ff 等
├── CLAUDE.md                     # OpenSpec 标记已移除，您的内容保留
└── AGENTS.md                     # OpenSpec 标记已移除，您的内容保留
```

### 已移除的内容

- `.claude/commands/openspec/` — 由 `.claude/skills/` 取代
- `openspec/AGENTS.md` — 已过时
- `openspec/project.md` — 迁移到 `config.yaml`，然后删除
- `CLAUDE.md`、`AGENTS.md` 等中的 OpenSpec 标记块

### 命令速查表

```text
/opsx:propose      快速开始（默认 core 配置）
/opsx:apply        实施任务
/opsx:archive      完成并归档

# 扩展工作流（如果启用）：
/opsx:new          创建变更 scaffold
/opsx:continue     创建下一个产物
/opsx:ff           创建规划产物
```

---

## 获取帮助

- **Discord**：[discord.gg/YctCnvvshC](https://discord.gg/YctCnvvshC)
- **GitHub Issues**：[github.com/Fission-AI/OpenSpec/issues](https://github.com/Fission-AI/OpenSpec/issues)
- **文档**：[docs/opsx.md](opsx.md) 获取完整的 OPSX 参考
