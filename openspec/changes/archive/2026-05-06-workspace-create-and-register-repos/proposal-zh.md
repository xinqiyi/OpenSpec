## 为什么

注意：变更 ID 保留了较旧的"register repos"措辞以保持连续性。此切片中面向用户的产品语言是 `workspace setup`、`workspace link`、`workspace relink` 和"链接的仓库或文件夹"。

用户通过创建规划家园并链接 OpenSpec 应了解的仓库或文件夹来开始 workspace 工作。

在 OpenSpec 能看到相关仓库、单体仓库文件夹、包、服务或应用之前，他们不应必须创建变更。

产品规则是：

```text
Workspace 可见性不等同于变更承诺。
```

Workspace 是持久的规划家园。变更是该 workspace 内的一个功能、修复、项目或其他计划中的工作。

## 变更内容

添加第一个面向用户的 workspace 设置流程：

```text
设置一个 workspace。
链接现有的仓库或文件夹。
列出已知的 workspace 及其链接内容。
检查 OpenSpec 能解析什么以及如何修复问题。
```

预期的用户界面：

```bash
openspec workspace setup
openspec workspace setup --no-interactive --name platform --link /path/to/api --link web=/path/to/web
openspec workspace list
openspec workspace ls
openspec workspace link /path/to/api
openspec workspace link api-service /path/to/api
openspec workspace relink api /new/path/to/api
openspec workspace doctor
```

`workspace setup` 是用户的创建路径。它应首先询问 workspace 名称，在标准位置创建 workspace，要求至少一个现有的仓库或文件夹路径，从文件夹名称推断链接名称，显示 workspace 位置，并在最后运行检查以便用户知道 OpenSpec 能看到什么。

Workspace 名称应为 kebab-case，这样它们就是干净的管理文件夹名称和稳定的注册表标识符。链接名称应保留来自 `workspace-foundation` 的文件夹风格验证，因为它们通常直接从现有的仓库或文件夹基本名称推断而来。

`workspace setup --no-interactive` 是自动化路径。它应需要足够的标志来创建一个有用的 workspace，包括 workspace 名称和至少一个链接。

`workspace list` 从本地 workspace 注册表显示已知的 OpenSpec 管理的 workspace，包括每个 workspace 位置和链接的仓库或文件夹。

`workspace link` 为选定的 workspace 记录一个现有的本地仓库或文件夹路径。它应支持从文件夹名称推断链接名称的简单形式，以及用于冲突或清晰性的显式名称形式。链接不会在链接的仓库或文件夹中创建、复制、移动、初始化或编辑文件。

链接应像从选择器中选择文件夹一样：OpenSpec 验证文件夹存在，将相对输入解析为当前运行时的绝对路径，并存储该已验证的路径而不是原始输入字符串。

当链接名称已被使用时，OpenSpec 应保留现有链接并显示冲突名称及其现有路径。错误应建议选择不同的链接名称，或者如果用户意图更改现有链接的路径，应使用 `workspace relink <name> <path>`。

`workspace relink` 允许用户修复或更改现有链接的本地路径，而无需重新创建 workspace。此切片中不应引入所有者或交接元数据。

`workspace doctor` 解释当前机器能为一个选定的 workspace 解析什么：workspace 位置、workspace 规划路径、链接的仓库或文件夹、缺失的路径、存在的仓库本地 specs 路径以及建议的修复方法。当从 workspace 内部运行时，它应推断当前 workspace。它报告问题但不自动修复。

Workspace 命令应全局工作。当命令需要一个 workspace 且用户未指定时，OpenSpec 应使用本地注册表显示交互式选择器。在非交互模式下，它应以清晰的消息失败并建议 `--workspace <name>`。

当命令从本地注册表中不存在但有效的 workspace 内部运行时，OpenSpec 仍应使用该当前 workspace。它应显示一个非致命的警告状态，指明该 workspace 在本地未知，并且成功的变更性命令（如 `workspace link` 或 `workspace relink`）应在更新 workspace 状态后将该 workspace 记录到本地注册表。

机器可读的输出应将 workspace 或链接对象与状态条目分开。状态应是一个结构化问题的数组，而不是将诸如 `root_status`、`issue` 或 `fix` 等字段分散到主要对象形状中。

每当输出必须是脚本安全的时，应禁用交互式行为。`--no-interactive` 表示无提示，`--json` 应在选择或 setup 输入歧义时失败而不是提示。`workspace setup --json` 应要求 `--no-interactive`，以便 JSON setup 始终使用显式的自动化路径。

规划依赖：

- 依赖 `workspace-foundation`。

## POC 发现

要保留的行为：

- `workspace setup` 是友好的引导式入门路径。
- `workspace list` 使管理的 workspace 可被发现。
- 直接的自动化路径仍然有用，但它应位于 `workspace setup --no-interactive` 下。
- 链接修复很有用，但所有者或交接元数据不应在此切片中延续。
- `workspace doctor` 是回答"OpenSpec 对此 workspace 了解什么？"的正确位置。
- 共享的 workspace 状态和本地路径分开存储。
- 非交互式输入不完整时，Setup 优雅失败。
- 创建的 workspace 将机器本地路径状态从可移植的 workspace 状态中排除。

要变更的行为：

- POC 要求链接的仓库路径已经包含仓库本地的 `openspec/`。这应成为实现就绪信号，而不是规划前提。
- POC 使用仅仓库的语言。此切片应在面向用户的文本中使用"仓库或文件夹"。
- 公共命令应为 `workspace link`，而不是 `workspace add-repo`。
- 修复命令应为 `workspace relink`，而不是 `workspace update-repo`。
- 公共的 `workspace create` 应在首个版本中移除。Setup 应为创建流程。
- POC 的 `setup` 流程存储了首选代理和打开行为。代理启动偏好属于 `workspace-open-agent-context`，而不是此切片。
- 人工输出应避免实现术语，如工作集、代码区域、条目、别名或本地覆盖。
- `setup` 应要求至少一个链接的仓库或文件夹，以便创建的 workspace 立即可用。

## 非目标

- 首个版本中没有公共的 `openspec workspace create` 命令。
- 没有代理启动或 workspace 打开行为。
- 没有首选代理提示或保存的代理偏好。
- 没有所有者或交接元数据字段。
- 没有 workspace 变更创建或目标选择。
- 没有 apply、verify、archive、branch 或 worktree 行为。
- 不要求链接的仓库或文件夹具有仓库本地的 OpenSpec 状态。
- `workspace doctor` 中没有自动修复行为。
- 没有注册表清理命令如 `workspace forget`；此切片中过期的注册表条目仅做报告。
- 没有独立的 `workspace register` 或 `workspace join` 命令；未注册的当前 workspace 是可用的，变更性的 workspace 命令可以在本地记录它们。

## 能力

### 新能力

- `workspace-links`：允许用户设置 workspace、链接仓库或文件夹、列出已知 workspace 以及在变更创建前检查 workspace 解析。

### 修改的能力

- `cli-artifact-workflow`：引入在变更创建之前发生的 workspace 设置命令。
- `workspace-foundation`：将 workspace 名称收紧为 kebab-case，同时保留文件夹风格的链接名称。

## 影响

- `openspec workspace setup`
- `openspec workspace list`
- `openspec workspace ls`
- `openspec workspace link`
- `openspec workspace relink`
- `openspec workspace doctor`
- 使用来自 `workspace-foundation` 的本地 workspace 注册表。
- 文档和生成的指导，将链接的仓库或文件夹解释为规划上下文，而不是实现承诺。
