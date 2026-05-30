# CLI 参考

OpenSpec CLI（`openspec`）提供用于项目设置、验证、状态检查和管理等终端命令。这些命令补充了[命令](commands.md)中记录的 AI 斜杠命令（如 `/opsx:propose`）。

## 概要

| 类别 | 命令 | 用途 |
|----------|----------|---------|
| **设置** | `init`, `update` | 在你的项目中初始化和更新 OpenSpec |
| **工作区（beta）** | `workspace setup`, `workspace list`, `workspace ls`, `workspace link`, `workspace relink`, `workspace doctor`, `workspace update`, `workspace open` | 设置链接仓库或文件夹的本地视图 |
| **共享上下文（beta）** | `context-store setup`, `context-store register`, `context-store unregister`, `context-store remove`, `context-store list`, `context-store doctor`, `initiative create`, `initiative show`, `initiative list` | 管理本地上下文存储注册和持久化 initiative 上下文 |
| **浏览** | `list`, `view`, `show` | 探索变更和 specs |
| **验证** | `validate` | 检查变更和 specs 是否有问题 |
| **生命周期** | `archive` | 最终确定已完成变更 |
| **工作流** | `new change`, `set change`, `status`, `instructions`, `templates`, `schemas` | 产物驱动的工作流支持 |
| **Schema** | `schema init`, `schema fork`, `schema validate`, `schema which` | 创建和管理自定义工作流 |
| **配置** | `config` | 查看和修改设置 |
| **工具** | `feedback`, `completion` | 反馈和 Shell 集成 |

---

## 人类命令与 Agent 命令

大多数 CLI 命令是为**终端中的人类使用**而设计的。部分命令也支持通过 JSON 输出供 **agent/脚本使用**。

### 仅人类命令

这些命令是交互式的，专为终端使用设计：

| 命令 | 用途 |
|---------|---------|
| `openspec init` | 初始化项目（交互式提示） |
| `openspec view` | 交互式仪表板 |
| `openspec config edit` | 在编辑器中打开配置 |
| `openspec feedback` | 通过 GitHub 提交反馈 |
| `openspec completion install` | 安装 Shell 补全 |

### Agent 兼容命令

这些命令支持 `--json` 输出，供 AI agent 和脚本以编程方式使用：

| 命令 | 人类使用 | Agent 使用 |
|---------|-----------|-----------|
| `openspec list` | 浏览变更/specs | `--json` 获取结构化数据 |
| `openspec show <item>` | 读取内容 | `--json` 供解析 |
| `openspec validate` | 检查问题 | `--all --json` 用于批量验证 |
| `openspec status` | 查看产物进度 | `--json` 获取结构化状态 |
| `openspec instructions` | 获取下一步操作 | `--json` 供 agent 使用 |
| `openspec templates` | 查找模板路径 | `--json` 用于路径解析 |
| `openspec schemas` | 列出可用 schema | `--json` 用于 schema 发现 |
| `openspec workspace setup --no-interactive` | 使用显式输入创建工作区 | `--json` 获取结构化设置输出 |
| `openspec workspace list` | 浏览已知工作区 | `--json` 获取类型化工作区对象 |
| `openspec workspace link` | 链接仓库或文件夹 | `--json` 获取结构化链接输出 |
| `openspec workspace relink` | 修复链接路径 | `--json` 获取结构化链接输出 |
| `openspec workspace doctor` | 检查一个工作区 | `--json` 获取结构化状态输出 |
| `openspec workspace update` | 刷新工作区本地指导和 agent skills | `--tools` 选择 agent；profile 选择工作流 |
| `openspec context-store setup <id>` | 创建本地上下文存储 | `--json` 显式输入获取结构化设置输出 |
| `openspec context-store register <path>` | 注册现有上下文存储 | `--json` 获取结构化注册输出 |
| `openspec context-store unregister <id>` | 遗忘本地上下文存储注册 | `--json` 获取结构化清理输出 |
| `openspec context-store remove <id>` | 删除已注册的本地上下文存储文件夹 | `--yes --json` 用于非交互式删除 |
| `openspec context-store list` | 浏览已注册的上下文存储 | `--json` 获取结构化注册信息 |
| `openspec context-store doctor` | 检查本地存储设置 | `--json` 获取结构化诊断信息 |
| `openspec initiative list` | 浏览共享 initiatives | `--json` 获取结构化 initiative 记录 |
| `openspec initiative show <id>` | 解析 initiative | `--json` 获取规范路径和元数据 |
| `openspec new change <id>` | 创建仓库内变更 scaffold | `--json`，以及 `--initiative` 用于共享协调链接 |
| `openspec set change <id>` | 更新已检入的变更元数据 | `--json`，以及 `--initiative` 用于共享协调链接 |

---

## 全局选项

这些选项适用于所有命令：

| 选项 | 描述 |
|--------|-------------|
| `--version`, `-V` | 显示版本号 |
| `--no-color` | 禁用彩色输出 |
| `--help`, `-h` | 显示命令帮助 |

---

## 设置命令

### `openspec init`

在你的项目中初始化 OpenSpec。创建文件夹结构并配置 AI 工具集成。

默认行为使用全局配置默认值：配置 `core`，交付方式 `both`，工作流 `propose, explore, apply, sync, archive`。

```
openspec init [path] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path` | 否 | 目标目录（默认：当前目录） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--tools <list>` | 非交互式配置 AI 工具。使用 `all`、`none` 或逗号分隔列表 |
| `--force` | 自动清理遗留文件，无需提示 |
| `--profile <profile>` | 为此次 init 运行覆盖全局配置（`core` 或 `custom`） |

`--profile custom` 使用当前在全局配置中选中的工作流（`openspec config profile`）。

**支持的工具 ID（`--tools`）：** `amazon-q`, `antigravity`, `auggie`, `bob`, `claude`, `cline`, `codex`, `forgecode`, `codebuddy`, `continue`, `costrict`, `crush`, `cursor`, `factory`, `gemini`, `github-copilot`, `iflow`, `junie`, `kilocode`, `kimi`, `kiro`, `opencode`, `pi`, `qoder`, `lingma`, `qwen`, `roocode`, `trae`, `windsurf`

**示例：**

```bash
# 交互式初始化
openspec init

# 在特定目录中初始化
openspec init ./my-project

# 非交互式：为 Claude 和 Cursor 配置
openspec init --tools claude,cursor

# 为所有支持的工具配置
openspec init --tools all

# 为此次运行覆盖配置
openspec init --profile core

# 跳过提示并自动清理遗留文件
openspec init --force
```

**创建的内容：**

```
openspec/
├── specs/              # 你的规范（唯一真相来源）
├── changes/            # 提议的变更
└── config.yaml         # 项目配置

.claude/skills/         # Claude Code skills（如果选择了 claude）
.cursor/skills/         # Cursor skills（如果选择了 cursor）
.cursor/commands/       # Cursor OPSX 命令（如果交付方式包含 commands）
... (其他工具配置)
```

---

### `openspec update`

升级 CLI 后更新 OpenSpec 指令文件。使用你当前的全局配置、选中的工作流和交付方式重新生成 AI 工具配置文件。

```
openspec update [path] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path` | 否 | 目标目录（默认：当前目录） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--force` | 即使文件已是最新也强制更新 |

**示例：**

```bash
# npm 升级后更新指令文件
npm update @fission-ai/openspec
openspec update
```

---

## 工作区命令

工作区命令处于 beta 阶段。下面的本地视图模型是当前方向，但外部自动化、集成和长期工作流仍应将命令行为、状态文件和 JSON 输出视为持续演进中。

协调工作区是链接仓库或文件夹的机器本地视图。工作区可见性不等于变更提交：链接 OpenSpec 应该知道的仓库或文件夹，然后在准备好规划具体工作时创建变更。

### `openspec workspace setup`

在标准 OpenSpec 工作区位置创建工作区，并链接至少一个现有仓库或文件夹。

```bash
openspec workspace setup [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--name <name>` | 工作区名称。名称必须使用 kebab-case |
| `--link <path>` | 链接现有仓库或文件夹并从文件夹名称推断链接名称 |
| `--link <name>=<path>` | 使用显式链接名称链接现有仓库或文件夹 |
| `--opener <id>` | 在非交互式设置中存储首选打开方式：`codex-cli`、`claude`、`github-copilot` 或 `editor` |
| `--tools <tools>` | 为 agent 安装工作区本地 OpenSpec skills。使用 `all`、`none` 或逗号分隔的工具 ID |
| `--no-interactive` | 禁用提示；需要 `--name` 和至少一个 `--link` |
| `--json` | 输出 JSON；需要 `--no-interactive` |

**示例：**

```bash
openspec workspace setup
openspec workspace setup --no-interactive --name platform --link /repos/api --link web=/repos/web
openspec workspace setup --no-interactive --name platform --link /repos/api --opener codex-cli
openspec workspace setup --no-interactive --name platform --link /repos/api --tools codex,claude
openspec workspace setup --no-interactive --json --name checkout --link /repos/platform/apps/checkout
```

交互式设置询问首选打开方式，并可以为选中的 agent 安装工作区本地 OpenSpec skills。非交互式设置仅在提供了 `--opener` 时存储首选打开方式；否则 `workspace open` 会在交互式终端中提示选择一个受支持的打开方式，或要求脚本传递 `--agent <tool>` 或 `--editor`。

在此 beta 阶段，工作区 skill 安装仅限 skills：即使全局交付方式是 `commands` 或 `both`，工作区设置也只会在工作区根目录写入 agent skill 文件夹，而不会创建斜杠命令文件。激活的全局 profile 选择安装哪些工作流 skills；`--tools` 选择哪些 agent 接收它们。如果在非交互式设置中省略 `--tools`，则不会安装任何 skills，后续可以通过 `workspace update --tools <ids>` 添加。

### `openspec workspace list`

从本地注册表中列出已知的 OpenSpec 工作区。

```bash
openspec workspace list [--json]
openspec workspace ls [--json]
```

列表显示每个工作区的位置和链接的仓库或文件夹。过期的注册记录会被报告但不会更改。

### `openspec workspace link`

为一个工作区记录一个现有的仓库或文件夹。

```bash
openspec workspace link [name] <path> [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--workspace <name>` | 从本地注册表中选择一个已知工作区 |
| `--json` | 输出 JSON |
| `--no-interactive` | 禁用工作区选择器提示 |

**示例：**

```bash
openspec workspace link /repos/api
openspec workspace link api-service /repos/api
openspec workspace link --workspace platform /repos/platform/apps/checkout
```

路径必须已经存在。相对路径根据命令的当前目录进行解析，然后 OpenSpec 将验证后的绝对路径存储在机器本地的工作区状态中。链接路径可以是完整的仓库、包、服务、应用或没有仓库本地 `openspec/` 状态的文件夹。

### `openspec workspace relink`

修复或更改现有链接的本地路径。

```bash
openspec workspace relink <name> <path> [options]
```

路径必须已经存在。Relink 仅更新稳定链接名称对应的机器本地路径。

### `openspec workspace doctor`

检查一个工作区在当前机器上可以解析的内容。

```bash
openspec workspace doctor [options]
```

Doctor 显示工作区位置、链接的仓库或文件夹、缺失的路径、仓库本地 specs 路径（如果存在）和建议的修复。JSON 输出还包括用于兼容性的工作区规划路径。它仅报告问题；不会自动修复。

需要单个工作区的命令在工作区文件夹或子目录中运行时使用当前工作区。从其他位置运行时，传递 `--workspace <name>`，在交互式终端的选择器中选取，或当仅有一个已知工作区时自动使用。在 `--json` 或 `--no-interactive` 模式下，歧义选择会失败并返回结构化状态错误，建议使用 `--workspace <name>`。

JSON 响应使用类型化对象加上 `status` 数组。主要数据位于 `workspace`、`workspaces` 或 `link` 中；警告和错误位于 `status` 中。

### `openspec workspace update`

刷新工作区本地的 OpenSpec 指导和 agent skills。

```bash
openspec workspace update [name] [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--workspace <name>` | 从本地注册表中选择一个已知工作区 |
| `--tools <tools>` | 为工作区 skills 选择 agent。使用 `all`、`none` 或逗号分隔的工具 ID |
| `--json` | 输出 JSON |
| `--no-interactive` | 禁用工作区选择器提示 |

**示例：**

```bash
openspec workspace update
openspec workspace update platform
openspec workspace update --workspace platform --tools codex,claude
openspec workspace update --workspace platform --tools none
```

`workspace update` 刷新生成的工作区指导块和本地开放面。对于 agent skills，当省略 `--tools` 时，会重用存储的工作区 skill agent 选择。传递 `--tools` 会替换该存储的选择。它仅刷新工作区根目录中 OpenSpec 管理工作流 skill 目录，移除取消选择的管理工作流 skills，并保持链接的仓库和文件夹不变。

从工作区内部运行 `openspec update` 会重定向到 `openspec workspace update`；在仓库本地项目中运行 `openspec update` 当你想要更新仓库拥有的工具文件时使用。

### `openspec workspace open`

通过存储的首选打开方式、单会话 agent 覆盖或 VS Code 编辑器模式打开工作区工作集。

```bash
openspec workspace open [name] [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--workspace <name>` | 位置工作区名称的别名 |
| `--initiative <id>` | 将 initiative 作为本地工作区视图打开。接受 `<id>` 或 `<store>/<id>` |
| `--store <id>` | 已注册的上下文存储 ID，用于 `--initiative` |
| `--store-path <path>` | 用于 `--initiative` 的现有本地上下文存储根目录 |
| `--agent <tool>` | 单会话 agent 覆盖：`codex-cli`、`claude` 或 `github-copilot` |
| `--editor` | 将维护的 VS Code 工作区文件作为普通编辑器工作区打开 |
| `--no-interactive` | 禁用工作区和打开方式选择器提示 |

**示例：**

```bash
openspec workspace open
openspec workspace open platform
openspec workspace open platform --agent github-copilot
openspec workspace open --agent codex-cli
openspec workspace open --editor
openspec workspace open --initiative billing-launch --store platform
openspec workspace open --initiative platform/billing-launch
```

`workspace open` 在工作区内运行时使用当前工作区，在其他位置运行时自动选择唯一已知的工作区，当有多个已知工作区时让用户选择。`--agent` 和 `--editor` 不会更改存储的首选打开方式。同时传递两个打开方式覆盖是错误；请选择 `--agent <tool>` 或 `--editor`。

当使用了 `--initiative` 时，OpenSpec 为该 initiative 准备或选择一个私有本地工作区视图。通过注册表选择的存储按 ID 存储；`--store-path` 存储运行时本地路径选择器，因为工作区视图是私有本地状态。

OpenSpec 在工作区根目录维护 `<workspace-name>.code-workspace` 文件，用于 VS Code 编辑器和 VS Code 中的 GitHub Copilot 打开。该文件是机器本地工作区视图状态。

维护的 VS Code 工作区首先列出有效的链接仓库或文件夹，然后在附加时列出 initiative 上下文，最后列出 OpenSpec 工作区文件。VS Code 将这些条目显示为多根工作区。

根工作区打开使链接的仓库或文件夹可用于探索和上下文。实施编辑应在显式用户请求和正常的 OpenSpec 实施工作流之后才开始。

---

## 共享上下文命令

上下文存储和 initiatives 是 beta 协调层。上下文存储是持久化共享上下文的本地注册，通常是一个 Git 支持的文件夹或克隆。Initiative 是上下文存储内部的共享协调上下文；仓库本地变更可以链接到它，而无需将共享计划复制到每个仓库。

### `openspec context-store setup`

创建并注册一个本地上下文存储。在终端中无参数运行时，OpenSpec 引导用户完成设置。Agent 和脚本应传递显式输入并使用 `--json`。

```bash
openspec context-store setup [id] [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--path <path>` | 上下文存储文件夹路径；默认为 OpenSpec 管理的本地数据目录 |
| `--init-git` | 在上下文存储中初始化 Git 仓库 |
| `--no-init-git` | 不初始化 Git 仓库 |
| `--json` | 输出 JSON |

当省略 `--path` 时，setup 在 `getGlobalDataDir()/context-stores/<id>` 下创建存储：当设置了 `XDG_DATA_HOME` 时在 `$XDG_DATA_HOME/openspec/context-stores/<id>`，或在 Unix 风格的回退路径 `~/.local/share/openspec/context-stores/<id>` 下。当你希望存储位于可见的克隆或团队特定文件夹中时，传递 `--path`。

示例：

```bash
openspec context-store setup
openspec context-store setup team-context
openspec context-store setup team-context --path /repos/team-context --no-init-git
openspec context-store setup team-context --json --no-init-git
```

### `openspec context-store register`

注册一个现有的本地上下文存储文件夹。

```bash
openspec context-store register [path] [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--id <id>` | 上下文存储 ID；默认为存储元数据或文件夹名称 |
| `--json` | 输出 JSON |

### `openspec context-store unregister`

遗忘本地上下文存储注册，不删除文件。

```bash
openspec context-store unregister <id> [--json]
```

当存储被移动、克隆到其他地方或不应再在此机器上由 OpenSpec 显示时使用。

### `openspec context-store remove`

遗忘本地上下文存储注册并删除其本地文件夹。

```bash
openspec context-store remove <id> [--yes] [--json]
```

`remove` 在交互式终端中显示确切的文件夹后再删除。Agent、脚本和 JSON 调用者必须传递 `--yes` 以确认删除。OpenSpec 拒绝删除不包含匹配上下文存储元数据的文件夹。

### `openspec context-store list`

列出本地注册的上下文存储。

```bash
openspec context-store list [--json]
openspec context-store ls [--json]
```

### `openspec context-store doctor`

检查本地上下文存储注册、元数据和 Git 存在情况。

```bash
openspec context-store doctor [id] [--json]
```

Doctor 仅做诊断；它报告缺失的根目录、元数据不匹配和无效的本地注册状态，而不会修改存储。

### `openspec initiative create`

在上下文存储中创建一个 initiative。

```bash
openspec initiative create <id> --title <title> --summary <summary> [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--store <id>` | 来自本地注册表的上下文存储 ID |
| `--store-path <path>` | 现有的本地上下文存储根目录 |
| `--title <title>` | Initiative 标题 |
| `--summary <summary>` | Initiative 摘要 |
| `--json` | 输出 JSON |

### `openspec initiative list`

列出 initiatives。没有选择器时，会搜索所有已注册的上下文存储，并在 `status` 中报告部分读取警告。

```bash
openspec initiative list [options]
openspec initiative ls [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--store <id>` | 列出一个已注册的上下文存储 |
| `--store-path <path>` | 列出一个现有的本地上下文存储根目录 |
| `--json` | 输出 JSON |

### `openspec initiative show`

解析一个 initiative 并打印其规范位置。

```bash
openspec initiative show <id> [options]
openspec initiative show <store>/<id> [options]
```

没有 `--store` 时，OpenSpec 搜索所有已注册的上下文存储。如果同一 initiative ID 存在于多个存储中，传递 `--store <id>` 或使用 `<store>/<id>` 形式。

---

## 浏览命令

### `openspec list`

列出项目中的变更或 specs。

```
openspec list [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--specs` | 列出 specs 而非变更 |
| `--changes` | 列出变更（默认） |
| `--sort <order>` | 按 `recent`（默认）或 `name` 排序 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 列出所有活跃变更
openspec list

# 列出所有 specs
openspec list --specs

# JSON 输出供脚本使用
openspec list --json
```

**输出（文本）：**

```
Active changes:
  add-dark-mode     UI theme switching support
  fix-login-bug     Session timeout handling
```

---

### `openspec view`

显示一个用于探索 specs 和变更的交互式仪表板。

```
openspec view
```

打开一个基于终端的界面，用于浏览项目的规范和变更。

---

### `openspec show`

显示变更或 spec 的详细信息。

```
openspec show [item-name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `item-name` | 否 | 变更或 spec 的名称（省略时提示） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--type <type>` | 指定类型：`change` 或 `spec`（无歧义时自动检测） |
| `--json` | 输出为 JSON |
| `--no-interactive` | 禁用提示 |

**变更特定选项：**

| 选项 | 描述 |
|--------|-------------|
| `--deltas-only` | 仅显示 delta specs（JSON 模式） |

**Spec 特定选项：**

| 选项 | 描述 |
|--------|-------------|
| `--requirements` | 仅显示需求，排除场景（JSON 模式） |
| `--no-scenarios` | 排除场景内容（JSON 模式） |
| `-r, --requirement <id>` | 按基于 1 的索引显示特定需求（JSON 模式） |

**示例：**

```bash
# 交互式选择
openspec show

# 显示特定变更
openspec show add-dark-mode

# 显示特定 spec
openspec show auth --type spec

# JSON 输出供解析
openspec show add-dark-mode --json
```

---

## 验证命令

### `openspec validate`

验证变更和 specs 的结构性问题。

```
openspec validate [item-name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `item-name` | 否 | 要验证的特定项（省略时提示） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--all` | 验证所有变更和 specs |
| `--changes` | 验证所有变更 |
| `--specs` | 验证所有 specs |
| `--type <type>` | 当名称有歧义时指定类型：`change` 或 `spec` |
| `--strict` | 启用严格验证模式 |
| `--json` | 输出为 JSON |
| `--concurrency <n>` | 最大并行验证数（默认：6，或 `OPENSPEC_CONCURRENCY` 环境变量） |
| `--no-interactive` | 禁用提示 |

**示例：**

```bash
# 交互式验证
openspec validate

# 验证特定变更
openspec validate add-dark-mode

# 验证所有变更
openspec validate --changes

# 验证所有内容并输出 JSON（用于 CI/脚本）
openspec validate --all --json

# 严格的验证，增加并行度
openspec validate --all --strict --concurrency 12
```

**输出（文本）：**

```
Validating add-dark-mode...
  ✓ proposal.md valid
  ✓ specs/ui/spec.md valid
  ⚠ design.md: missing "Technical Approach" section

1 warning found
```

**输出（JSON）：**

```json
{
  "version": "1.0.0",
  "results": {
    "changes": [
      {
        "name": "add-dark-mode",
        "valid": true,
        "warnings": ["design.md: missing 'Technical Approach' section"]
      }
    ]
  },
  "summary": {
    "total": 1,
    "valid": 1,
    "invalid": 0
  }
}
```

---

## 生命周期命令

### `openspec archive`

归档已完成的变更并将 delta specs 合并到主 specs 中。

```
openspec archive [change-name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `change-name` | 否 | 要归档的变更（省略时提示） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `-y, --yes` | 跳过确认提示 |
| `--skip-specs` | 跳过 spec 更新（用于基础设施/工具/纯文档变更） |
| `--no-validate` | 跳过验证（需要确认） |

**示例：**

```bash
# 交互式归档
openspec archive

# 归档特定变更
openspec archive add-dark-mode

# 无提示归档（CI/脚本）
openspec archive add-dark-mode --yes

# 归档不影响 specs 的工具变更
openspec archive update-ci-config --skip-specs
```

**作用：**

1. 验证变更（除非使用 `--no-validate`）
2. 提示确认（除非使用 `--yes`）
3. 将 delta specs 合并到 `openspec/specs/`
4. 将变更文件夹移至 `openspec/changes/archive/YYYY-MM-DD-<name>/`

---

## 工作流命令

这些命令支持产物驱动的 OPSX 工作流。对人类检查进度和 agent 确定下一步操作都很有用。

### `openspec new change`

创建仓库内变更目录和可选的检入元数据。

```bash
openspec new change <name> [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--description <text>` | 添加到 `README.md` 的描述 |
| `--goal <text>` | 与变更一起存储的工作区产品目标 |
| `--areas <names>` | 逗号分隔的受影响工作区链接名称 |
| `--initiative <id>` | 将仓库内变更链接到 initiative |
| `--store <id>` | 用于 `--initiative` 的上下文存储 ID |
| `--store-path <path>` | 用于 `--initiative` 的现有本地上下文存储根目录 |
| `--schema <name>` | 要使用的工作流 schema |
| `--json` | 输出 JSON |

示例：

```bash
openspec new change add-billing-api --initiative billing-launch --store platform
openspec new change add-billing-api --initiative platform/billing-launch --json
```

### `openspec set change`

更新已检入的仓库内变更元数据，无需重新创建变更。

```bash
openspec set change <name> [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--initiative <id>` | 将仓库内变更链接到 initiative |
| `--store <id>` | 用于 `--initiative` 的上下文存储 ID |
| `--store-path <path>` | 用于 `--initiative` 的现有本地上下文存储根目录 |
| `--json` | 输出 JSON |

`set change --initiative` 在请求的链接已存在时是幂等的，并拒绝替换不同的现有 initiative 链接。

### `openspec status`

显示变更的产物完成状态。

```
openspec status [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--change <id>` | 变更名称（省略时提示） |
| `--schema <name>` | Schema 覆盖（从变更配置自动检测） |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 交互式状态检查
openspec status

# 特定变更的状态
openspec status --change add-dark-mode

# JSON 供 agent 使用
openspec status --change add-dark-mode --json
```

**输出（文本）：**

```
Change: add-dark-mode
Schema: spec-driven
Progress: 2/4 artifacts complete

[x] proposal
[ ] design
[x] specs
[-] tasks (blocked by: design)
```

**输出（JSON）：**

```json
{
  "changeName": "add-dark-mode",
  "schemaName": "spec-driven",
  "isComplete": false,
  "applyRequires": ["tasks"],
  "artifacts": [
    {"id": "proposal", "outputPath": "proposal.md", "status": "done"},
    {"id": "design", "outputPath": "design.md", "status": "ready"},
    {"id": "specs", "outputPath": "specs/**/*.md", "status": "done"},
    {"id": "tasks", "outputPath": "tasks.md", "status": "blocked", "missingDeps": ["design"]}
  ]
}
```

---

### `openspec instructions`

获取创建产物或实施任务的增强指令。由 AI agent 用于了解下一步要创建什么。

```
openspec instructions [artifact] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `artifact` | 否 | 产物 ID：`proposal`、`specs`、`design`、`tasks` 或 `apply` |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--change <id>` | 变更名称（非交互模式必需） |
| `--schema <name>` | Schema 覆盖 |
| `--json` | 输出为 JSON |

**特殊情况：** 使用 `apply` 作为产物来获取任务实施指令。

**示例：**

```bash
# 获取下一个产物的指令
openspec instructions --change add-dark-mode

# 获取特定产物的指令
openspec instructions design --change add-dark-mode

# 获取 apply/实施指令
openspec instructions apply --change add-dark-mode

# JSON 供 agent 消费
openspec instructions design --change add-dark-mode --json
```

**输出包括：**

- 产物的模板内容
- 来自配置的项目上下文
- 来自依赖产物的内容
- 来自配置的按产物规则

---

### `openspec templates`

显示 schema 中所有产物的已解析模板路径。

```
openspec templates [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--schema <name>` | 要检查的 schema（默认：`spec-driven`） |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 显示默认 schema 的模板路径
openspec templates

# 显示自定义 schema 的模板
openspec templates --schema my-workflow

# JSON 供编程使用
openspec templates --json
```

**输出（文本）：**

```
Schema: spec-driven

Templates:
  proposal  → ~/.openspec/schemas/spec-driven/templates/proposal.md
  specs     → ~/.openspec/schemas/spec-driven/templates/specs.md
  design    → ~/.openspec/schemas/spec-driven/templates/design.md
  tasks     → ~/.openspec/schemas/spec-driven/templates/tasks.md
```

---

### `openspec schemas`

列出可用的工作流 schema 及其描述和产物流。

```
openspec schemas [options]
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--json` | 输出为 JSON |

**示例：**

```bash
openspec schemas
```

**输出：**

```
Available schemas:

  spec-driven (package)
    The default spec-driven development workflow
    Flow: proposal → specs → design → tasks

  my-custom (project)
    Custom workflow for this project
    Flow: research → proposal → tasks
```

---

## Schema 命令

用于创建和管理自定义工作流 schema 的命令。

### `openspec schema init`

创建一个新的项目本地 schema。

```
openspec schema init <name> [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `name` | 是 | Schema 名称（kebab-case） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--description <text>` | Schema 描述 |
| `--artifacts <list>` | 逗号分隔的产物 ID（默认：`proposal,specs,design,tasks`） |
| `--default` | 设置为项目默认 schema |
| `--no-default` | 不提示设置为默认 |
| `--force` | 覆盖现有 schema |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 交互式 schema 创建
openspec schema init research-first

# 非交互式，指定产物
openspec schema init rapid \
  --description "Rapid iteration workflow" \
  --artifacts "proposal,tasks" \
  --default
```

**创建的内容：**

```
openspec/schemas/<name>/
├── schema.yaml           # Schema 定义
└── templates/
    ├── proposal.md       # 每个产物的模板
    ├── specs.md
    ├── design.md
    └── tasks.md
```

---

### `openspec schema fork`

将现有 schema 复制到你的项目中进行自定义。

```
openspec schema fork <source> [name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `source` | 是 | 要复制的 schema |
| `name` | 否 | 新 schema 名称（默认：`<source>-custom`） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--force` | 覆盖现有目标 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# Fork 内置的 spec-driven schema
openspec schema fork spec-driven my-workflow
```

---

### `openspec schema validate`

验证 schema 的结构和模板。

```
openspec schema validate [name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `name` | 否 | 要验证的 schema（省略时验证所有） |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--verbose` | 显示详细验证步骤 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 验证特定 schema
openspec schema validate my-workflow

# 验证所有 schema
openspec schema validate
```

---

### `openspec schema which`

显示 schema 从哪里解析（用于调试优先级）。

```
openspec schema which [name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `name` | 否 | Schema 名称 |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--all` | 列出所有 schema 及其来源 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 检查 schema 从何而来
openspec schema which spec-driven
```

**输出：**

```
spec-driven resolves from: package
  Source: /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven
```

**Schema 优先级：**

1. 项目：`openspec/schemas/<name>/`
2. 用户：`~/.local/share/openspec/schemas/<name>/`
3. 包：内置 schema

---

## 配置命令

### `openspec config`

查看和修改全局 OpenSpec 配置。

```
openspec config <subcommand> [options]
```

**子命令：**

| 子命令 | 描述 |
|------------|-------------|
| `path` | 显示配置文件位置 |
| `list` | 显示所有当前设置 |
| `get <key>` | 获取特定值 |
| `set <key> <value>` | 设置值 |
| `unset <key>` | 移除键 |
| `reset` | 重置为默认值 |
| `edit` | 在 `$EDITOR` 中打开 |
| `profile [preset]` | 交互式或通过预设配置工作流配置 |

**示例：**

```bash
# 显示配置文件路径
openspec config path

# 列出所有设置
openspec config list

# 获取特定值
openspec config get telemetry.enabled

# 设置值
openspec config set telemetry.enabled false

# 显式设置字符串值
openspec config set user.name "My Name" --string

# 移除自定义设置
openspec config unset user.name

# 重置所有配置
openspec config reset --all --yes

# 在编辑器中编辑配置
openspec config edit

# 使用基于操作的向导配置 profile
openspec config profile

# 快速预设：切换工作流到 core（保留交付方式）
openspec config profile core
```

`openspec config profile` 以当前状态摘要开始，然后让你选择：
- 更改交付方式 + 工作流
- 仅更改交付方式
- 仅更改工作流
- 保留当前设置（退出）

如果你保留当前设置，不会写入任何更改，也不会显示更新提示。
如果没有配置更改，但当前项目或工作区文件与你的全局配置/交付方式不同步，OpenSpec 会显示警告并建议对仓库本地项目运行 `openspec update`，或对工作区本地指导和 skills 运行 `openspec workspace update`。
按 `Ctrl+C` 也会干净地取消流程（无堆栈跟踪）并以代码 `130` 退出。
在工作流复选框中，`[x]` 表示该工作流已在全局配置中选择。要将这些选择应用于项目文件，运行 `openspec update`（或在项目内提示时选择`立即将更改应用于此项目？`）。从工作区内部，使用 `openspec workspace update` 刷新工作区本地指导和 skills；这仍然仅针对生成的 agent 工作流文件生成 skills，不会生成工作区斜杠命令。

**交互式示例：**

```bash
# 仅更新交付方式
openspec config profile
# 选择：仅更改交付方式
# 选择交付方式：仅 Skills

# 仅更新工作流
openspec config profile
# 选择：仅更改工作流
# 在复选框中切换工作流，然后确认
```

---

## 工具命令

### `openspec feedback`

提交关于 OpenSpec 的反馈。创建一个 GitHub Issue。

```
openspec feedback <message> [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `message` | 是 | 反馈消息 |

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--body <text>` | 详细描述 |

**要求：** 必须安装并认证 GitHub CLI（`gh`）。

**示例：**

```bash
openspec feedback "Add support for custom artifact types" \
  --body "I'd like to define my own artifact types beyond the built-in ones."
```

---

### `openspec completion`

管理 OpenSpec CLI 的 Shell 补全。

```
openspec completion <subcommand> [shell]
```

**子命令：**

| 子命令 | 描述 |
|------------|-------------|
| `generate [shell]` | 输出补全脚本到 stdout |
| `install [shell]` | 为你的 Shell 安装补全 |
| `uninstall [shell]` | 移除已安装的补全 |

**支持的 Shell：** `bash`, `zsh`, `fish`, `powershell`

**示例：**

```bash
# 安装补全（自动检测 Shell）
openspec completion install

# 为特定 Shell 安装
openspec completion install zsh

# 生成脚本供手动安装
openspec completion generate bash > ~/.bash_completion.d/openspec

# 卸载
openspec completion uninstall
```

---

## 退出码

| 代码 | 含义 |
|------|---------|
| `0` | 成功 |
| `1` | 错误（验证失败、文件缺失等） |

---

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `OPENSPEC_TELEMETRY` | 设置为 `0` 以禁用遥测 |
| `DO_NOT_TRACK` | 设置为 `1` 以禁用遥测（标准 DNT 信号） |
| `OPENSPEC_CONCURRENCY` | 批量验证的默认并发数（默认：6） |
| `EDITOR` 或 `VISUAL` | 用于 `openspec config edit` 的编辑器 |
| `NO_COLOR` | 设置后禁用彩色输出 |

---

## 相关文档

- [命令](commands.md) - AI 斜杠命令（`/opsx:propose`，`/opsx:apply` 等）
- [工作流](workflows.md) - 常见模式及何时使用每个命令
- [自定义](customization.md) - 创建自定义 schema 和模板
- [快速入门](getting-started.md) - 首次设置指南
