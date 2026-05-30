## 产品形态

`workspace open` 应感觉像打开一个多根工作集。

用户模型是：

```text
workspace setup = 创建 planning 主目录并选择默认打开程序
workspace links = OpenSpec 可以跨这些 repository 或文件夹进行 planning
workspace open = 打开该链接的工作集
--agent = 为这一次会话使用不同的 agent
--editor = 将工作集作为编辑器 workspace 打开
```

repository 或文件夹的可见性支持探索和 planning。打开 workspace 使 agent 或编辑器能够访问链接的路径，实施通过显式的后续 workflow 开始。

## 命令表面

支持的 v1 形式：

```bash
openspec workspace open
openspec workspace open platform
openspec workspace open --agent codex
openspec workspace open platform --agent github-copilot
openspec workspace open --editor
```

位置参数的 workspace 名称是 `open` 的主要显式选择表面。面向用户的文档应偏好位置参数形式，因为像 `--workspace <name>` 这样的标志重复了名词。

为了与其他 workspace 命令和脚本保持一致，`workspace open` 也可以支持 `--workspace <name>` 作为位置参数的别名：

```bash
openspec workspace open platform
openspec workspace open --workspace platform
```

面向用户的文档应偏好位置参数形式。如果两者都提供且不同，OpenSpec 应以清晰的冲突错误失败。

`--prepare-only` 不应包含在内。POC 使用它来构建和打印启动表面而不启动外部工具，但这不能清晰映射到面向用户的意图。

`--json` 不应包含在此切片中。如果未来的集成需要机器可读的已解析打开上下文，将其设计为单独的上下文/查询表面，而不是重载启动命令。

`--change` 应被推迟。变更范围的打开取决于 workspace 变更 planning 和目标语义，此切片不应发明这些。

## workspace 选择

选择应遵循以下顺序：

1. 如果提供了位置参数的 workspace 名称，打开该已知 workspace。
2. 否则，如果命令从 workspace 内部运行，打开当前 workspace。
3. 否则，如果本地恰好知道一个 workspace，打开它。
4. 否则，如果知道多个 workspace 且终端是交互式的，显示选择器。
5. 否则，以清晰消息失败，列出已知 workspace 并要求用户传递 workspace 名称。

这使常见情况保持直接，同时仍支持全局使用。

## 首选打开程序

workspace 设置应询问用户默认使用哪个打开程序。答案是机器本地状态，因为不同机器可能安装了不同的 agent 或编辑器。

`workspace open` 在没有传递覆盖时使用保存的打开程序。

`--agent <tool>` 是一次会话的覆盖，保持保存的偏好不变。如果需要，在后续的切片中，持久化更改的默认值需要显式的偏好/配置操作。

此切片不应添加全局 workspace 打开程序配置。OpenSpec 已有全局配置系统，如果重复设置使本地提示显得嘈杂，可以在以后在此处添加 workspace 级别的默认值。

本地偏好的形状应使未来的全局默认值可以平滑迁移。预期的优先级是：

```text
命令覆盖
 -> workspace 本地首选打开程序
 -> 未来的全局 workspace 默认打开程序
 -> 交互式提示或内置回退
```

在未来配置术语中，该全局默认值可能看起来像 `workspace.defaultOpener`；此切片记录后续实现的优先级。

将首选打开程序作为结构化对象存储在 `.openspec-workspace/local.yaml` 中：

```yaml
preferred_opener:
 kind: agent
 id: codex
```

```yaml
preferred_opener:
 kind: editor
 id: vscode
```

允许的初始值：

```text
kind: agent, id: codex
kind: agent, id: claude
kind: agent, id: github-copilot
kind: editor, id: vscode
```

该结构使 agent/编辑器区别清晰，并为未来的打开程序变体留下空间，而无需更改本地状态形状。

交互式设置应显示所有受支持的打开程序选择，但应首先排列已检测到/可用的打开程序。不可用的选择仍应可见，并带有说明，如 `未在 PATH 中找到`。

设置应在需要交互式选择器的回退默认值时，优先选择纯编辑器选项而非 agent。

非交互式设置会在调用者显式传递打开程序选项时存储首选打开程序。否则，它将打开程序选择留给后续的交互式 `workspace open` 提示，或非交互式错误，其中解释如何选择打开程序。

设置时的标志应为：

```bash
openspec workspace setup --no-interactive --name platform --link /repo --opener codex
openspec workspace setup --no-interactive --name platform --link /repo --opener editor
```

`--opener <id>` 设置存储的偏好。它不同于 `workspace open --agent <id>` 和 `workspace open --editor`，后者是一次会话的运行时覆盖。

初始打开程序检测应保持简单且基于可执行文件：

```text
VS Code 编辑器：code
Codex：codex
Claude：claude
VS Code 中的 GitHub Copilot：code
```

在此切片中将初始检测限定在可执行文件可用性。

初始打开表面的受支持 agent 值应限于具有真实启动或附加机制的工​​具：

```text
claude
codex
github-copilot
```

纯编辑器打开应由 `--editor` 配合显式的编辑器种类表示。

对于此切片，`--editor` 指 VS Code 编辑器。`.code-workspace` 格式是 VS Code 特定的，因此提示和错误应称其为 `VS Code 编辑器`，而不是暗示通用编辑器支持。

`github-copilot` 指 VS Code Copilot 体验。它应在 VS Code 中打开维护的 `.code-workspace`，因为这是该 Copilot schema 可用的产品表面。

如果 OpenSpec 以后支持 Copilot CLI agent，它应使用不同的值，如 `github-copilot-cli`，并直接启动 CLI agent。VS Code Copilot 和 CLI agent 具有不同的打开程序机制，因此它们应保持为不同的打开程序值。

## 打开程序可用性

当所选打开程序在当前机器上不可用时，`workspace open` 应清晰失败。

所选打开程序保持必需，因为它代表用户意图，无论它来自本地偏好还是命令行覆盖。

错误应指明缺少的可执行文件或不可用的打开程序，并建议具体的下一步。对于基于编辑器的打开，错误应包括 `.code-workspace` 路径，以便用户必要时手动打开。

当未存储首选打开程序且未提供命令行覆盖时，`workspace open` 应在交互式 schema 下提示。在非交互式 schema 下，它应失败并告诉用户传递 agent 覆盖或编辑器选项。

## 编辑器打开

`--editor` 打开 workspace 根目录加上每个具有有效本地路径的链接 repository 或文件夹。

对于 VS Code 风格的编辑器支持，OpenSpec 应作为 workspace 设置/链接/重新链接生命周期的一部分，创建和维护一个 `.code-workspace` 文件。`workspace open` 应针对现有 workspace 状态启动。

预期的本地 workspace 形状：

```text
workspace-root/
 changes/
 <workspace-name>.code-workspace
 .openspec-workspace/
 workspace.yaml
 local.yaml
```

`.code-workspace` 文件应包括 workspace 根目录和每个具有有效本地路径的链接 repository 或文件夹。由于链接路径来自机器本地 workspace 状态，OpenSpec 创建的 workspace 应默认忽略维护的 `.code-workspace` 文件。

忽略规则应针对特定的维护文件，并让其他 `*.code-workspace` 文件可供用户编写追踪：

```text
<workspace-name>.code-workspace
```

这让团队以后在有共享的相对路径布局时，可以添加单独的用户编写的可移植 `.code-workspace`。

`workspace setup`、`workspace link` 和 `workspace relink` 都应在变更 workspace 状态后运行相同的打开表面同步。该同步负责：

- `AGENTS.md`
- `<workspace-name>.code-workspace`
- 机器本地文件的 workspace 忽略规则

即使命令只更改本地状态，如 `workspace relink`，它也应刷新整个可打开的 workspace 表面，以免面向用户的文件产生差异。

`--agent github-copilot` 可能使用相同的编辑器 workspace 机制，但它还需要 Copilot 提示上下文。纯 `--editor` 保持正常的编辑器 workspace 意图。

`--agent github-copilot` 仍应打开 VS Code。与 `--editor` 的区别在于意图：`--editor` 将 workspace 作为正常编辑器 workspace 打开，而 `--agent github-copilot` 打开相同的编辑器 workspace，供用户使用 VS Code Copilot agent 体验。

## workspace 指导

workspace 设置应在 workspace 根目录安装稳定的指导，最好是 `AGENTS.md`。

指导应解释持久的 workspace 规则：

- workspace 根目录是 planning 主目录
- `changes/` 包含 workspace 级别的 planning
- 链接的 repository 和文件夹可用于探索和 planning
- 可见性支持探索和 planning
- 实施编辑在用户显式要求实施工作后开始

受管理的 `AGENTS.md` 文本应保持简短和持久，涵盖稳定的 workspace 指导，而运行时细节仍可从 workspace 状态发现。一个初始形状：

```markdown
# OpenSpec workspace 指导

此目录是 OpenSpec workspace，用于跨链接的 repository 或文件夹进行 planning。

- 使用 `changes/` 进行 workspace 级别的 planning。
- 链接的 repository 和文件夹可用于探索和 planning。
- repository 或文件夹的可见性支持探索和 planning。
- 在用户显式要求实施工作后进行实施编辑。
- 将链接的 repository 和文件夹视为其拥有代码的实施主目录。
- 使用 OpenSpec workspace 命令，而不是手动编辑 `.openspec-workspace/*.yaml`。
```

`workspace open` 是一个启动功能。它应针对现有 workspace 文件启动所选打开程序。

对于 Claude 和 Codex，`workspace open` 可能仍需要在启动时将 workspace 和链接的目录参数传递给 agent 进程，因为这些工具不直接消费 `.code-workspace`。如果打开程序需要初始提示参数，它应保持最小，例如 `打开这个 OpenSpec workspace。`

动态 workspace 事实通常应从现有文件中发现：

- 链接路径：`.openspec-workspace/local.yaml`
- 稳定的链接名称：`.openspec-workspace/workspace.yaml`
- 活动的 workspace 变更：`changes/`
- 编辑器工作集：`<workspace-name>.code-workspace`

仅在实际写入和使用文件时报告命令文件或提示文件路径。

OpenSpec 应拥有 `AGENTS.md` 内部标记的 workspace 指导块：

```markdown
<!-- OPENSPEC:WORKSPACE-GUIDANCE:START -->
# OpenSpec workspace 指导

...
<!-- OPENSPEC:WORKSPACE-GUIDANCE:END -->
```

`workspace setup`、`workspace link` 和 `workspace relink` 可以在打开表面同步期间重写该标记块。标记块之外的内容应被保留，以便用户在同一文件中保留自己的 workspace 笔记。

如果 `AGENTS.md` 缺失，OpenSpec 应重新创建它。如果 `AGENTS.md` 存在但标记缺失，OpenSpec 应在保留现有内容的同时附加受管理块。

## 链接路径

根 workspace 打开应附加每个具有有效本地路径的链接 repository 或文件夹。

在 workspace 打开期间跳过损坏的链接。OpenSpec 应在人类输出中显示清晰的状态，以 `openspec workspace doctor` 作为修复路径。

在打开 workspace 时，具有缺失的 repository 本地 `openspec/` 状态的链接仍然有效。缺失的 repository 本地 OpenSpec 状态以后可能对实施准备工作很重要，但在此阶段仍允许探索和 planning 的可见性。

## 安全边界

打开提示或编辑器指导应说：

```text
链接的 repository 和文件夹可见，用于探索和 planning。
在用户显式要求实施工作后进行实施编辑。
```

对于此切片，提示指导是可接受的，因为应用/验证/archive 位于打开表面之外。后来的实施 workflow 应通过显式的上下文提供者和提示措辞来强制 schema 和范围。
