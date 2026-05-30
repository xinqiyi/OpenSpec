## 为什么

用户需要一个 workspace，使其感觉像是跨多个 repository 或文件夹进行 planning 的自然主目录。

他们应该能够这样思考：

```text
我有经常一起 planning 的 repository 或文件夹。
我创建一个 OpenSpec workspace。
该 workspace 是变更所在的地方。
我的代码保持在原处。
OpenSpec 将 workspace 链接到那些本地路径。
```

workspace 不是一个功能。它是持久的 planning 主目录。各个功能、修复和项目是 workspace 内部的变更。

用户不必选择存储位置、提前创建变更或在 OpenSpec 能够定位之前了解内部 workspace 状态。

POC 证明了 workspace 状态是有用的。此重新实现应将其转化为一个简单的产品模型，用户和 agent 无需特殊词汇即可解释。

## 什么变更

此变更定义了 OpenSpec workspace 的面向用户基础。

一个 OpenSpec workspace 具有可识别的 planning 主目录：

```text
workspace-root/
 changes/
 .openspec-workspace/
```

`changes/` 是 workspace 级别 planning 所在的位置。`.openspec-workspace/` 将目录标识为 OpenSpec workspace 并存储 workspace 状态。

OpenSpec 管理 workspace 位于一个标准位置：

```text
<全局数据目录>/workspaces/
```

用户不应需要选择该位置。OpenSpec 仍在设置后显示 workspace 路径，以便用户知道 planning 文件所在位置。此基础切片不提供 workspace 特定的环境变量或配置覆盖，用于管理 workspace 存储。

OpenSpec 还在当前机器上维护已知 workspace 的轻量级本地注册表。注册表驱动全局命令、选择器和列表，但每个 workspace 文件夹保持为真实源。

workspace 状态按用户期望进行拆分：

- 共享的 workspace 信息可以在机器之间移动
- 本地检出路径保持每台机器本地
- 链接的 repository 和文件夹通过稳定的链接名称引用，而不是绝对路径

链接路径可以是完整的 repository、单体 repository 内的文件夹或 workspace 应针对其进行 planning 的其他现有文件夹。链接路径在被纳入 workspace planning 之前不需要 repository 本地 `openspec/` 状态。repository 本地 OpenSpec 状态以后可能对实施、验证或 archive workflow 很重要，但它不是 planning 可见性的先决条件。

本机 Windows/PowerShell 和 WSL2 都受支持。每个运行时使用自己的路径约定。OpenSpec 在此基础切片中不在 Windows 和 WSL 之间翻译路径。

## 成果

在此变更之后，后续 workspace 功能可以依赖一个清晰的产品契约：

- OpenSpec 可以判断用户何时在 workspace 内部。
- OpenSpec 知道默认在何处创建管理 workspace。
- OpenSpec 可以维护已知 workspace 的本地注册表。
- workspace 有一个可见的 planning 区域：`changes/`。
- workspace 状态可与 repository 本地 `openspec/` 状态区分。
- 共享 workspace 状态不会强制将一个用户的本地路径强加给另一个用户。
- workspace planning 可以通过稳定的链接名称引用现有 repository 或文件夹。
- 链接的 repository 或文件夹不需要 repository 本地 OpenSpec 状态即可进行 workspace planning。
- 多 repository 和大型单体 repository 工作可以使用相同的 workspace planning 模型。
- repository 拥有的 spec 和实施仍由其 repository 或源区域拥有。
- Windows、PowerShell 和 WSL2 路径行为是可预测的。

此变更不交付完整的 workspace workflow。它为 `workspace-create-and-register-repos` 提供了添加第一个面向用户命令所需的基础。

## POC 发现

要保留的行为：

- workspace 是用于跨 repository planning 的持久协调主目录。
- workspace 在其根目录有一个可见的 `changes/` 目录。
- 链接的 repository 和文件夹提供 workspace 可以针对其进行 planning 的上下文。
- 稳定的链接名称比本地检出路径更重要。
- 本地机器路径不应成为共享 workspace 状态。
- spec 标准和实施仍属于拥有它们的 repository。

要继承的经验教训：

- POC 隐藏的 `.openspec/` workspace 元数据形状使 workspace 状态太容易与 repository 本地 OpenSpec 状态混淆。
- 用户不应需要在 workspace 根目录内运行 repository 本地的 `openspec init`。
- POC 要求已注册的 repository 已有 `openspec/` 对于 planning 来说过于严格。repository 和文件夹在采用 repository 本地 OpenSpec 状态之前应该是可链接的。
- repository 或文件夹可见性不应依赖于创建变更。
- workspace 设置不应暗示 repository 本地实施、分支、工作树、应用、验证或 archive 行为。
- `add-repo` 对于面向用户的模型来说过于狭窄。链接现有 repository 或文件夹更清晰。

## 决策

- workspace 标识目录：`.openspec-workspace/`。
- workspace 标识文件：`.openspec-workspace/workspace.yaml`。
- workspace 名称：当前操作系统的有效文件夹名称，排除空名称、`.`/`..` 和路径分隔符。
- workspace 名称使用：存储在 `workspace.yaml` 中，用作默认管理 workspace 文件夹名称，并用作本地注册表名称。
- planning 表面：顶级 `changes/`。
- 本地机器状态：`.openspec-workspace/local.yaml`。
- 本地机器状态排除：OpenSpec 创建的 workspace 默认将 `.openspec-workspace/local.yaml` 从可移植协作状态中排除。
- 本地 workspace 注册表：`<全局数据目录>/workspaces/registry.yaml`。
- 默认 workspace 基础路径：`<全局数据目录>/workspaces/`。
- 平台行为：本机 Windows 和 WSL2 各自使用运行 OpenSpec 的运行时的路径约定。
- 链接路径可以是完整 repository、单体 repository 文件夹或其他现有文件夹。
- 链接名称：非空、稳定的名称，在 workspace 内唯一，排除 `.`/`..` 和路径分隔符。
- repository 本地 `openspec/` 状态不是 workspace planning 可见性的必要条件。
- 链接仅记录关系；它不在链接的 repository 或文件夹内创建、复制、移动、初始化或编辑文件。

planning 依赖：

- 无。这是第一个实施切片。

## 非目标

- 尚无完整的 `openspec workspace setup`、`openspec workspace link` 或 `openspec workspace relink` 流程。
- 第一个面向用户的 workspace 流程中没有公共的 `openspec workspace create` 命令。
- 没有用于更改标准 workspace 位置的面向用户命令、环境变量或配置设置。
- 没有询问用户 OpenSpec 默认应在何处存储 workspace 的问题。
- 没有自动的 Windows 到 WSL 或 WSL 到 Windows 路径翻译。
- 没有 workspace 打开 agent 启动行为。
- 没有 workspace 级别 proposal 创建。
- 没有 repository 切片应用、验证、archive、分支或工作树行为。
- 没有将 workspace planning 文件复制到链接的 repository 或文件夹中，作为创建、检测或链接 workspace 的副作用。

## 能力

### 新能力

- `workspace-foundation`：定义 OpenSpec workspace 的产品基础。

### 修改的能力

- `openspec-conventions`：描述协调 workspace 与 repository 本地 OpenSpec 项目的区别。

## 影响

- workspace 识别和路径行为。
- workspace 状态解析。
- 本地 workspace 注册表解析。
- workspace 心智模型的文档和 agent 指导。
- 后续 workspace 切片应基于此契约构建，而不是重新定义 workspace 存储、标识、注册表或路径行为。
