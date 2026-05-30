## 产品形态

`workspace open` 应感觉像打开一个多根工作集。

用户模型是：

```text
workspace setup = 创建规划主目录并选择默认打开程序
workspace links = OpenSpec 可以跨这些仓库或文件夹进行规划
workspace open = 打开该链接的工作集
--agent = 为这一次会话使用不同的代理
--editor = 将工作集作为编辑器工作区打开
```

仓库或文件夹的可见性支持探索和规划。打开工作区使代理或编辑器能够访问链接的路径，实施通过显式的后续工作流开始。

## 命令表面

支持的 v1 形式：

```bash
openspec workspace open
openspec workspace open platform
openspec workspace open --agent codex
openspec workspace open platform --agent github-copilot
openspec workspace open --editor
```

位置参数的工作区名称是 `open` 的主要显式选择表面。面向用户的文档应偏好位置参数形式，因为像 `--workspace <name>` 这样的标志重复了名词。

为了与其他工作区命令和脚本保持一致，`workspace open` 也可以支持 `--workspace <name>` 作为位置参数的别名：

```bash
openspec workspace open platform
openspec workspace open --workspace platform
```

面向用户的文档应偏好位置参数形式。如果两者都提供且不同，OpenSpec 应以清晰的冲突错误失败。

`--prepare-only` 不应包含在内。POC 使用它来构建和打印启动表面而不启动外部工具，但这不能清晰映射到面向用户的意图。

`--json` 不应包含在此切片中。如果未来的集成需要机器可读的已解析打开上下文，将其设计为单独的上下文/查询表面，而不是重载启动命令。

`--change` 应被推迟。变更范围的打开取决于工作区变更规划和目标语义，此切片不应发明这些。

## 工作区选择

选择应遵循以下顺序：

1. 如果提供了位置参数的工作区名称，打开该已知工作区。
2. 否则，如果命令从工作区内部运行，打开当前工作区。
3. 否则，如果本地恰好知道一个工作区，打开它。
4. 否则，如果知道多个工作区且终端是交互式的，显示选择器。
5. 否则，以清晰消息失败，列出已知工作区并要求用户传递工作区名称。

这使常见情况保持直接，同时仍支持全局使用。

## 首选打开程序

工作区设置应询问用户默认使用哪个打开程序。答案是机器本地状态，因为不同机器可能安装了不同的代理或编辑器。

`workspace open` 在没有传递覆盖时使用保存的打开程序。

`--agent <tool>` 是一次会话的覆盖，保持保存的偏好不变。如果需要，在后续的切片中，持久化更改的默认值需要显式的偏好/配置操作。

此切片不应添加全局工作区打开程序配置。OpenSpec 已有全局配置系统，如果重复设置使本地提示显得嘈杂，可以在以后在此处添加工作区级别的默认值。

本地偏好的形状应使未来的全局默认值可以平滑迁移。预期的优先级是：

```text
命令覆盖
  -> 工作区本地首选打开程序
  -> 未来的全局工作区默认打开程序
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

该结构使代理/编辑器区别清晰，并为未来的打开程序变体留下空间，而无需更改本地状态形状。

交互式设置应显示所有受支持的打开程序选择，但应首先排列已检测到/可用的打开程序。不可用的选择仍应可见，并带有说明，如 `未在 PATH 中找到`。

设置应在需要交互式选择器的回退默认值时，优先选择纯编辑器选项而非代理。

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

初始打开表面的受支持代理值应限于具有真实启动或附加机制的工​​具：

```text
claude
codex
github-copilot
```

纯编辑器打开应由 `--editor` 配合显式的编辑器种类表示。

对于此切片，`--editor` 指 VS Code 编辑器。`.code-workspace` 格式是 VS Code 特定的，因此提示和错误应称其为 `VS Code 编辑器`，而不是暗示通用编辑器支持。

`github-copilot` 指 VS Code Copilot 体验。它应在 VS Code 中打开维护的 `.code-workspace`，因为这是该 Copilot 模式可用的产品表面。

如果 OpenSpec 以后支持 Copilot CLI 代理，它应使用不同的值，如 `github-copilot-cli`，并直接启动 CLI 代理。VS Code Copilot 和 CLI 代理具有不同的打开程序机制，因此它们应保持为不同的打开程序值。

## 打开程序可用性

当所选打开程序在当前机器上不可用时，`workspace open` 应清晰失败。

所选打开程序保持必需，因为它代表用户意图，无论它来自本地偏好还是命令行覆盖。

错误应指明缺少的可执行文件或不可用的打开程序，并建议具体的下一步。对于基于编辑器的打开，错误应包括 `.code-workspace` 路径，以便用户必要时手动打开。

当未存储首选打开程序且未提供命令行覆盖时，`workspace open` 应在交互式模式下提示。在非交互式模式下，它应失败并告诉用户传递代理覆盖或编辑器选项。

## 编辑器打开

`--editor` 打开工作区根目录加上每个具有有效本地路径的链接仓库或文件夹。

对于 VS Code 风格的编辑器支持，OpenSpec 应作为工作区设置/链接/重新链接生命周期的一部分，创建和维护一个 `.code-workspace` 文件。`workspace open` 应针对现有工作区状态启动。

预期的本地工作区形状：

```text
workspace-root/
  changes/
  <workspace-name>.code-workspace
  .openspec-workspace/
    workspace.yaml
    local.yaml
```

`.code-workspace` 文件应包括工作区根目录和每个具有有效本地路径的链接仓库或文件夹。由于链接路径来自机器本地工作区状态，OpenSpec 创建的工作区应默认忽略维护的 `.code-workspace` 文件。

忽略规则应针对特定的维护文件，并让其他 `*.code-workspace` 文件可供用户编写追踪：

```text
<workspace-name>.code-workspace
```

这让团队以后在有共享的相对路径布局时，可以添加单独的用户编写的可移植 `.code-workspace`。

`workspace setup`、`workspace link` 和 `workspace relink` 都应在变更工作区状态后运行相同的打开表面同步。该同步负责：

- `AGENTS.md`
- `<workspace-name>.code-workspace`
- 机器本地文件的工作区忽略规则

即使命令只更改本地状态，如 `workspace relink`，它也应刷新整个可打开的工作区表面，以免面向用户的文件产生差异。

`--agent github-copilot` 可能使用相同的编辑器工作区机制，但它还需要 Copilot 提示上下文。纯 `--editor` 保持正常的编辑器工作区意图。

`--agent github-copilot` 仍应打开 VS Code。与 `--editor` 的区别在于意图：`--editor` 将工作区作为正常编辑器工作区打开，而 `--agent github-copilot` 打开相同的编辑器工作区，供用户使用 VS Code Copilot 代理体验。

## 工作区指导

工作区设置应在工作区根目录安装稳定的指导，最好是 `AGENTS.md`。

指导应解释持久的工作区规则：

- 工作区根目录是规划主目录
- `changes/` 包含工作区级别的规划
- 链接的仓库和文件夹可用于探索和规划
- 可见性支持探索和规划
- 实施编辑在用户显式要求实施工作后开始

受管理的 `AGENTS.md` 文本应保持简短和持久，涵盖稳定的工作区指导，而运行时细节仍可从工作区状态发现。一个初始形状：

```markdown
# OpenSpec 工作区指导

此目录是 OpenSpec 工作区，用于跨链接的仓库或文件夹进行规划。

- 使用 `changes/` 进行工作区级别的规划。
- 链接的仓库和文件夹可用于探索和规划。
- 仓库或文件夹的可见性支持探索和规划。
- 在用户显式要求实施工作后进行实施编辑。
- 将链接的仓库和文件夹视为其拥有代码的实施主目录。
- 使用 OpenSpec 工作区命令，而不是手动编辑 `.openspec-workspace/*.yaml`。
```

`workspace open` 是一个启动功能。它应针对现有工作区文件启动所选打开程序。

对于 Claude 和 Codex，`workspace open` 可能仍需要在启动时将工作区和链接的目录参数传递给代理进程，因为这些工具不直接消费 `.code-workspace`。如果打开程序需要初始提示参数，它应保持最小，例如 `打开这个 OpenSpec 工作区。`

动态工作区事实通常应从现有文件中发现：

- 链接路径：`.openspec-workspace/local.yaml`
- 稳定的链接名称：`.openspec-workspace/workspace.yaml`
- 活动的工作区变更：`changes/`
- 编辑器工作集：`<workspace-name>.code-workspace`

仅在实际写入和使用文件时报告命令文件或提示文件路径。

OpenSpec 应拥有 `AGENTS.md` 内部标记的工作区指导块：

```markdown
<!-- OPENSPEC:WORKSPACE-GUIDANCE:START -->
# OpenSpec 工作区指导

...
<!-- OPENSPEC:WORKSPACE-GUIDANCE:END -->
```

`workspace setup`、`workspace link` 和 `workspace relink` 可以在打开表面同步期间重写该标记块。标记块之外的内容应被保留，以便用户在同一文件中保留自己的工作区笔记。

如果 `AGENTS.md` 缺失，OpenSpec 应重新创建它。如果 `AGENTS.md` 存在但标记缺失，OpenSpec 应在保留现有内容的同时附加受管理块。

## 链接路径

根工作区打开应附加每个具有有效本地路径的链接仓库或文件夹。

在工作区打开期间跳过损坏的链接。OpenSpec 应在人类输出中显示清晰的状态，以 `openspec workspace doctor` 作为修复路径。

在打开工作区时，具有缺失的仓库本地 `openspec/` 状态的链接仍然有效。缺失的仓库本地 OpenSpec 状态以后可能对实施准备工作很重要，但在此阶段仍允许探索和规划的可见性。

## 安全边界

打开提示或编辑器指导应说：

```text
链接的仓库和文件夹可见，用于探索和规划。
在用户显式要求实施工作后进行实施编辑。
```

对于此切片，提示指导是可接受的，因为应用/验证/归档位于打开表面之外。后来的实施工作流应通过显式的上下文提供者和提示措辞来强制模式和范围。
