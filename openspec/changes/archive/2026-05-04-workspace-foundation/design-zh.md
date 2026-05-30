## 产品模型

OpenSpec workspace 是跨多个 repository 或文件夹的工作的持久 planning 主目录。

它应感觉如下：

```text
workspace = 相关变更所在的位置
link = workspace 可以针对其进行 planning 的命名 repository 或文件夹
change = 一个功能、修复、项目或其他计划的工
```

基础有意避免了 workflow 的其余部分。它仅定义 OpenSpec 如何识别 workspace、管理 workspace 的位置、链接路径如何表示以及共享状态与本地状态的区别。

workspace 不是一个功能。它可以随时间持有许多变更。链接的 repository 或文件夹提供 planning 上下文，而代码保持在原处。

## workspace 形状

OpenSpec workspace 使用以下形状：

```text
workspace-root/
 changes/ # workspace 级别的 proposal、任务、spec
 .openspec-workspace/
 workspace.yaml # 共享的 workspace 信息
 local.yaml # 本机的路径和偏好
```

面向用户的 planning 表面是 `changes/`。使目录成为 workspace 的标识文件是 `.openspec-workspace/workspace.yaml`。

repository 本地项目保持现有形状：

```text
repo-root/
 openspec/
 specs/
 changes/
```

这种区别使用户或 agent 能够分辨他们在哪个表面工作：

```text
协调 workspace -> 共享的跨 repository planning
repository 本地项目 -> repository 拥有的 spec 和实施 planning
```

用户不应在 workspace 根目录内运行 repository 本地的 `openspec init`。workspace 已经是 OpenSpec 协调表面；它不是采用 repository 本地 OpenSpec 的产品 repository。

## workspace 名称

workspace 名称是简单的文件夹风格标识符，而非显示名称。

名称必须可用作当前运行时的文件夹名称。它不能为空，不能是 `.` 或 `..`，且不能包含路径分隔符。

OpenSpec 在此切片中不应维护跨平台保留名称列表。设置/创建流程应让文件系统创建暴露操作系统特定的无效文件夹名称，然后清晰报告该失败。

相同的 workspace 名称存储在 `.openspec-workspace/workspace.yaml` 中，用作默认管理 workspace 文件夹名称，并用作本地注册表名称。

## 共享和本地状态

workspace 状态遵循一个简单的共享规则：

```text
共享稳定的链接名称和 planning
将本地检出路径保持本地
```

预期的共享状态：

```yaml
version: 1
name: platform
links:
 api: {}
 web: {}
```

预期的本地状态：

```yaml
version: 1
paths:
 api: /repos/api
 web: /repos/web
```

后续切片可以扩展这些形状，但产品规则应保持稳定：共享 workspace 不应提交一个用户的绝对检出路径。

OpenSpec 创建的 workspace 应为 `.openspec-workspace/local.yaml` 包含忽略规则，以便本地检出路径不会意外共享。`.openspec-workspace/workspace.yaml` 保持为可移植的 workspace 标识和链接名称状态。

## workspace 位置

OpenSpec 应在一个标准位置创建管理 workspace：

```text
getGlobalDataDir()/workspaces
```

这复用了现有的 OpenSpec 数据目录行为：

- `$XDG_DATA_HOME/openspec/workspaces` 当设置了 `XDG_DATA_HOME`
- `~/.local/share/openspec/workspaces` 在 Unix/macOS 回退
- `%LOCALAPPDATA%\openspec\workspaces` 在本机 Windows 回退

此切片有意不定义 workspace 特定的环境变量、命令或配置覆盖，用于管理 workspace 存储。测试应依赖于现有的全局数据目录控制和测试助手，而不是单独的 workspace 主目录覆盖。

这有意保持安静。产品不应询问大多数用户 workspace 应存放在哪里。

OpenSpec 应在设置后显示解析后的 workspace 路径。安静的默认值应避免提示，而不是隐藏 planning 文件的创建位置。

## 本地 workspace 注册表

OpenSpec 应维护已知 workspace 的轻量级本地注册表：

```text
getGlobalDataDir()/workspaces/registry.yaml
```

预期的注册表状态：

```yaml
version: 1
workspaces:
 platform: /Users/tabish/.local/share/openspec/workspaces/platform
 checkout: /Users/tabish/.local/share/openspec/workspaces/checkout
```

注册表是本地索引，不是真实源。它存在以便 workspace 命令可以从任何地方工作，在多个 workspace 存在时显示选择器，并列出已知 workspace 而无需扫描任意文件夹。

每个 workspace 文件夹对其自己的 `.openspec-workspace/workspace.yaml` 和 `.openspec-workspace/local.yaml` 保持权威。如果注册表条目指向缺失或无效的 workspace，后续的检查/列出流程可以报告并建议修复。

## Windows 和 WSL2

路径行为是运行时本地的：

- PowerShell/本机 Windows 使用 Windows 路径和 Windows 数据目录回退。
- WSL2 在 WSL 内部使用 Linux 路径和 Linux/XDG 回退。
- 本地 repository 路径按用户为当前运行时所提供的方式存储。

示例：

```text
PowerShell：
 默认基础路径 -> %LOCALAPPDATA%\openspec\workspaces

WSL2：
 默认基础路径 -> ~/.local/share/openspec/workspaces
```

此切片不应在 `D:\repo`、`/mnt/d/repo` 和 `\\wsl$` 路径之间进行转换。如果 agent 启动 workflow 需要，跨运行时转换可以在以后重新考虑。

## 链接名称

链接名称是在 workspace planning 中引用 repository 或文件夹的稳定方式。

本地路径可以因机器而异：

```text
共享链接名称：landing
Tabish 路径： /Users/tabish/repos/landing
Windows 路径： D:\repos\landing
WSL2 路径： /mnt/d/repos/landing
```

后续 workflow 应在 workspace planning、状态和应用上下文中引用 `landing`。本地路径仅是当前机器找到该 repository 或文件夹的方式。

链接名称有意保持最小：它们不能为空，不能是 `.` 或 `..`，不能包含路径分隔符，并且在 workspace 内必须是唯一的。

拥有 repository 或文件夹仍然是 spec 标准和实施工作的主目录。workspace 使跨边界计划可读；它不会从链接的 repository 或文件夹中拿走所有权。

链接名称通常在引导流中从文件夹基本名称推断。直接流可以在默认值会冲突或不清晰时允许显式名称。

## 链接的 repository 和文件夹

workspace planning 可见性不应要求 repository 本地 OpenSpec 状态。

这对两种常见情况很重要：

- repository 尚未采用 OpenSpec，但仍需要在 planning 中被考虑
- 大型单体 repository 有诸如包、服务或应用等文件夹，应像独立区域一样 planning，而无需每个文件夹拥有自己的 `openspec/`

基础应允许链接模型描述两者：

```text
多 repository：
 api -> /repos/api
 web -> /repos/web

大型单体 repository：
 billing -> /repos/platform/services/billing
 checkout -> /repos/platform/apps/checkout
```

后续的应用/验证/archive workflow 可以决定实施需要哪些额外准备。planning 应在此之前能够开始。

链接仅记录 workspace 链接名称与本地路径之间的关系。它不得在链接的 repository 或文件夹内创建、复制、移动、初始化或编辑文件。

repository 本地 spec 可用性在需要时计算。例如，当链接路径包含 `openspec/specs` 时，后续的 doctor 命令可以报告 `repo_specs_path`，但该路径不应被视为必需的 workspace 状态。

## 后续切片

此基础在面向用户的 workspace workflow 之前停止：

- `workspace-create-and-register-repos` 拥有 setup、link、relink、list 和 doctor 行为。
- `workspace-open-agent-context` 拥有 agent 启动上下文。
- `workspace-change-planning` 拥有 workspace proposal 和 repository 范围。
- `workspace-apply-repo-slice` 拥有一个 repository 切片的实施。
- `workspace-verify-and-archive` 拥有完成和 archive 行为。
