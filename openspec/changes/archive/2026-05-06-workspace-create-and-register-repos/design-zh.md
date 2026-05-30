## 产品形态

此切片是 `workspace-foundation` 之后的第一个面向用户的步骤。

用户体验应该是：

```text
我设置了一个 workspace。
我链接它应该知道的 repository 或文件夹。
我以后可以列出我的 workspace。
我可以询问 OpenSpec 什么出了问题以及如何修复。
```

目前还不需要变更 proposal。

## 链接

Workspace 链接是一个稳定的名称加上当前机器上的本地路径。

示例：

```text
api -> /repos/api
web -> /repos/web
checkout -> /repos/platform/apps/checkout
billing -> /repos/platform/services/billing
```

路径可以指向完整的 repository 或大型单体 repository 内的文件夹。它可以指向尚未采用 repository 本地 OpenSpec 的 repository 或文件夹。

产品语言应使用"repository 或文件夹"。在面向用户的输出中应避免使用"工作集"、"代码区域"、"条目"、"别名"和"本地覆盖"。

路径处理应像文件夹选择器一样工作。用户可以输入相对或绝对路径，但 OpenSpec 应验证它指向一个存在的文件夹，必要时将其转换为相对于命令当前工作目录的绝对路径，并将该已验证的绝对路径存储在本地 workspace 状态中。OpenSpec 不应存储用户输入的原始字符串。

路径转换保持在当前运行时内。本机 Windows 路径、WSL2 路径和 Unix 路径不应跨运行时进行转换。如果重复路径检测需要 spec 比较，OpenSpec 可以在内部比较现有的 spec 路径，但它应存储和显示当前运行时的已验证绝对路径。

## 名称

Workspace 名称应为 kebab-case：

```text
platform
checkout-web
api2
```

无效的 workspace 名称包括大写字母、下划线、点、空格、前导连字符、尾随连字符、空名称、点名称和路径分隔符。交互式 setup 应解释预期的格式并允许用户重试。非交互式 setup 应在错误消息中包含相同的预期说明而失败。

链接名称应保留来自 `workspace-foundation` 的文件夹风格验证：它们不能为空，不能是 `.` 或 `..`，不能包含路径分隔符，并且必须在 workspace 内唯一。这使得推断的链接名称能与现有文件夹基本名称匹配，而无需强迫用户为重命名本地文件夹以进行 workspace planning。

链接名称通常从文件夹基本名称推断：

```text
/repos/api -> api
/repos/platform/apps/checkout -> checkout
```

如果推断的名称冲突，交互式 setup 应显示冲突名称及其映射的现有路径，然后询问不同的名称。非交互式 setup 和直接的 `workspace link` 应使用清晰的消息失败，而不是静默覆盖。

重复名称错误应具有以下特异性：

```text
无法使用链接名称 'api'，因为另一个链接已使用该名称。
现有链接：
 api -> /repos/api

请选择不同的名称：
 openspec workspace link archived-api /archive/api

如果您想更改现有链接的路径：
 openspec workspace relink api /archive/api
```

此切片不添加单独的链接重命名命令。如果用户需要，可以考虑稍后添加重命名链接的功能，但 v1 应保持命令模型简洁：`link` 添加新链接，`relink` 更改现有链接的本地路径。

## 命令

### `workspace setup`

引导式入门：

- 在标准 workspace 位置创建 workspace
- 询问 workspace 名称
- 要求至少一个现有的 repository 或文件夹路径
- 从文件夹名称推断链接名称
- 允许用户通过简单的重复提示添加更多 repository 或文件夹
- 在本地 workspace 注册表中记录该 workspace
- 运行 `workspace doctor`
- 打印 workspace 位置、planning 路径、链接的 repository 或文件夹以及下一步有用命令

此切片不应询问首选 agent 或使用 agent 打开 workspace。这些属于 `workspace-open-agent-context`。

Setup 应支持用于自动化的非交互 schema：

```bash
openspec workspace setup --no-interactive --name platform --link /path/to/api --link web=/path/to/web
```

在非交互 schema 下，除非用户提供有效的 workspace 名称和至少一个有效链接，否则 setup 应优雅失败。`--link` 应接受路径（从文件夹基本名称推断名称）或 `name=path` 形式。

此切片中没有公共的 `workspace create` 命令。Setup 就是创建流程。

### `workspace list`

从本地 workspace 注册表显示已知的 OpenSpec 管理的 workspace。

`workspace ls` 的行为应相同。

输出应回答存在什么以及每个 workspace 链接到什么：

```yaml
workspaces:
 - name: platform
 location: /.../openspec/workspaces/platform
 links:
 - name: api
 path: /repos/api
 - name: web
 path: /repos/web
 - name: checkout
 location: /.../openspec/workspaces/checkout
 links:
 - name: app
 path: /repos/platform/apps/checkout
```

List 应将深度验证留给 `workspace doctor`。如果已知的 workspace 位置不再存在，它仍可以报告明显过期的 workspace 注册表条目。此切片中过期的注册表条目只做报告：`workspace list` 不应删除、重写或修复注册表条目，此切片也不应添加 `workspace forget` 命令。

对于 JSON 输出，list 应使用类型化的 workspace 对象，并带有用于问题的结构化 `status` 数组：

```json
{
 "workspaces": [
 {
 "name": "platform",
 "root": "/.../openspec/workspaces/platform",
 "links": [
 {
 "name": "api",
 "path": "/repos/api",
 "status": []
 }
 ],
 "status": []
 },
 {
 "name": "old-platform",
 "root": "/.../openspec/workspaces/old-platform",
 "links": [],
 "status": [
 {
 "severity": "error",
 "code": "workspace_root_missing",
 "message": "Workspace 位置不存在。",
 "fix": "移除或修复本地注册表条目。"
 }
 ]
 }
 ],
 "status": []
}
```

### `workspace link [name] <path>`

为选定的 workspace 记录现有的 repository 或文件夹路径。

支持的形式：

```bash
openspec workspace link /path/to/api
openspec workspace link api-service /path/to/api
```

单参数形式从文件夹基本名称推断链接名称。双参数形式允许用户选择链接名称。

路径必须存在。该命令应接受：

- 完整的 repository 根目录
- 单体 repository 文件夹，如 packages、services 和 apps
- 没有 repository 本地 `openspec/` 的 repository 或文件夹

如果用户传递相对路径，OpenSpec 应在写入本地状态之前将其解析为命令当前工作目录的绝对路径。

如果路径有 repository 本地的 OpenSpec 状态，OpenSpec 可以在 doctor 输出中报告 repository 的 specs 路径。如果没有，OpenSpec 仍应允许 workspace planning。

`workspace link` 仅记录链接。它不得在链接的 repository 或文件夹中创建、复制、移动、初始化或编辑文件。

### `workspace relink <name> <path>`

修复或更改现有链接的本地路径。

Relink 应使用与 link 相同的路径处理：要求存在的文件夹，将相对输入解析为绝对运行时本地路径，并存储已验证的路径。

此切片应保持 relink 专注于路径修复。它不应包含所有者或交接元数据；POC 中这些语言过于注重流程，如果用户以后需要联系人或备注字段，可以重新考虑。

### `workspace doctor`

解释用户机器上的一个选定 workspace。如果命令从 workspace 文件夹或子目录运行且未提供 `--workspace <name>`，doctor 应使用该当前 workspace。否则，它应遵循正常的 workspace 选择规则。

Doctor 应检查：

- workspace 位置
- workspace planning 路径
- 链接的 repository 和文件夹
- 每个本地路径是否存在
- 存在的 repository 本地 specs 路径
- 缺失的本地路径
- 不在共享 workspace 状态中的本地名称
- 缺少本地路径的共享链接名称
- 每个问题的建议修复方法

Doctor 默认不应扫描本地注册表中的每个已知 workspace。广泛的注册表可见性属于 `workspace list`。如果用户以后需要全局 workspace 诊断，可以考虑添加未来的 `workspace doctor --all`。

Doctor 应报告问题并建议修复方法。它不应自动修复任何内容。

注册表清理仍不在范围内。如果 doctor 无法检查选定的 workspace，因为注册表指向缺失或无效的 workspace 位置，它应通过状态条目报告该选定 workspace 的问题，并在检查链接之前停止。其他过期的注册表条目应由 `workspace list` 来揭示，而不是由选定 workspace 的 doctor 来揭示。

人工输出默认应具有可读性：简短的 workspace 摘要、链接的 repository 或文件夹行，以及在需要关注时的清晰问题部分。不应是原始的 JSON 或刻板的 YAML 转储。

JSON 输出应遵循对象/状态 schema：主要数据位于类型化对象中，诊断信息位于 `status` 数组中。健康的对象具有 `status: []`。状态条目应包括 `severity`、`code`、`message` 以及可选的 `target` 和 `fix` 字段。

```json
{
 "workspace": {
 "name": "platform",
 "root": "/.../openspec/workspaces/platform",
 "planning_path": "/.../openspec/workspaces/platform/changes",
 "links": [
 {
 "name": "api",
 "path": "/repos/api",
 "repo_specs_path": "/repos/api/openspec/specs",
 "status": []
 },
 {
 "name": "web",
 "path": "/old/path/web",
 "repo_specs_path": null,
 "status": [
 {
 "severity": "error",
 "code": "linked_path_missing",
 "message": "链接的路径不存在。",
 "target": "links.web.path",
 "fix": "openspec workspace relink web /path/to/web"
 }
 ]
 }
 ],
 "status": []
 },
 "status": []
}
```

## Workspace 选择

Workspace 命令应能从任何地方工作。

不需要一个 workspace 的命令：

- `workspace setup`
- `workspace list`
- `workspace ls`

需要一个 workspace 的命令：

- `workspace link`
- `workspace relink`
- `workspace doctor`

如果当前命令需要一个 workspace 且未提供 `--workspace <name>`：

- 从 workspace 内部运行时使用当前 workspace
- 否则，当存在多个已知 workspace 时显示交互式选择器
- 否则，选择唯一已知的 workspace
- 否则，说明不存在 workspace 并建议 `openspec workspace setup`

即使当前 workspace 不在本地 workspace 注册表中，它也优先。这支持手动创建或共享的 workspace 文件夹。在这种情况下，命令应继续并包含一个非致命的警告状态：

```json
{
 "severity": "warning",
 "code": "workspace_not_in_local_registry",
 "message": "此 workspace 未在本地 workspace 注册表中记录。",
 "target": "workspace.root",
 "fix": "从此 workspace 运行一个变更性 workspace 命令，例如 workspace link 或 workspace relink，以在本地记录它。"
}
```

对于人工输出，这应是一个简短的警告而不是阻塞性错误。使用未注册的当前 workspace 的成功变更性命令，如 `workspace link` 或 `workspace relink`，应在变更成功后记录 workspace 名称和位置到本地注册表。非变更性命令如 `workspace doctor` 不应写入注册表状态；它们应仅报告警告。此切片不应添加独立的 `workspace register` 或 `workspace join` 命令。

在非交互 schema 下，需要一个 workspace 的命令应在选择歧义时失败，并建议 `--workspace <name>`。

`--json` 也应抑制需要一个 workspace 的命令的提示。如果命令本来会显示选择器，JSON schema 应失败并返回结构化的状态错误，并建议 `--workspace <name>`。

## 机器本地文件

Workspace 创建应默认使机器本地状态安全。

Workspace 应忽略：

```text
/.openspec-workspace/local.yaml
```

本地 workspace 注册表也应是机器本地的：

```text
<global-data-dir>/workspaces/registry.yaml
```

生成的 agent 启动界面可以由 `workspace-open-agent-context` 在创建时忽略。

## JSON 输出

交互式 setup 不需要将 JSON 输出作为其主要协议。非交互式 setup 和直接命令应支持用于脚本的 JSON 输出：

- `workspace setup --no-interactive --json`
- `workspace list --json`
- `workspace link --json`
- `workspace relink --json`
- `workspace doctor --json`

`workspace setup --json` 应要求 `--no-interactive`。如果用户在没有 `--no-interactive` 的情况下运行 `workspace setup --json`，setup 应清晰失败，因为交互式向导无法产生干净的 JSON。直接命令如 `workspace list --json`、`workspace link --json`、`workspace relink --json` 和 `workspace doctor --json` 不需要 `--no-interactive`，但 JSON schema 应禁用提示并在 workspace 选择歧义时失败。

JSON 输出应在各命令间使用对象/状态结构：

- 主要实体如 `workspace`、`workspaces` 或 `link` 携带持久数据
- `status` 数组携带警告、错误和建议的修复方法
- 状态条目使用稳定的 `code` 值加上人类可读的 `message` 文本
- 命令级别的 `status` 描述整个响应
- 对象级别的 `status` 描述该特定 workspace 或链接

## POC 调整

保留：

- 引导式 setup 作为默认的首次运行
- 直接的 list/link/check 命令
- 共享状态与本地路径分离
- 当必需的 setup 输入缺失时，干净的非交互式失败
- 用于非交互/直接命令的 JSON 输出

变更：

- 在首个版本中不暴露公共的 `workspace create`
- 不要求 repository 本地的 OpenSpec 状态来链接 repository 或文件夹
- 使用 `workspace link` 代替 `workspace add-repo`
- 使用 `workspace relink` 代替 `workspace update-repo`
- 不在 setup 期间保存首选 agent
- 不从 setup 提供打开 workspace 的选项
- 要求 setup 至少链接一个现有的 repository 或文件夹
- 保持 relink 行为专注于路径修复，而不是所有者或交接元数据
- 不在面向用户的输出中使用"工作集"、"代码区域"、"条目"、"别名"或"本地覆盖"
