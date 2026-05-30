# 让工作区打开倡议

## 状态

产品决策已锁定。剩余工作是实现设计和交付。

## 真实依据

从 `../../direction.md` 和边界开始：

```text
上下文存储同步真实信息。
集合塑造真实信息。
倡议协调工作。
工作区打开本地视图。
变更实现仓库拥有的切片。
```

Item 9 拒绝了独立的倡议解析。倡议发现属于 `initiative show`；本地路径映射属于工作区本地视图状态。

## 锁定方向

工作区不包含工作本身。它记住此运行时如何打开工作。

```text
私有本地视图记录
  -> 生成的运行时文件
  -> 开启器特定的启动
  -> 倡议上下文 + 选定的本地仓库/文件夹
```

持久化的部分是用户的私有本地视图选择。生成的部分是代理和编辑器的运行时支持。

## 产品目标

让用户在其自己的本地运行时中打开共享倡议，包含他们关心的上下文和仓库。

示例：

- 团队 A 的开发者使用本地仓库 A 和仓库 B 打开 `platform/billing-launch`。
- 团队 B 的开发者仅使用本地仓库 C 打开同一倡议。
- 用户仅打开倡议上下文，稍后链接仓库，仍然获得有用的代理指导。

## 非目标

- 不克隆仓库。
- 不创建分支或工作树。
- 不使用 Git 子模块作为工作区原语。
- 不从 Git 远程或磁盘扫描推断所有参与的仓库。
- 不将生成的代理文件写入已链接的仓库或上下文存储。
- 不将工作区级别的 `changes/` 作为持久的规划模型。
- 不在 Item 10 中强制执行编辑权限。

## 决策登记表

### 命令 UX

状态：已决定。

使用 `workspace open` 进行倡议本地视图实现：

```bash
openspec workspace open --initiative platform/billing-launch
openspec workspace open --initiative billing-launch --store platform
openspec workspace open --initiative billing-launch
openspec workspace open team-a-billing --initiative platform/billing-launch
```

理由：执行的操作是本地视图实现，因此命令属于 `workspace open` 而非 `initiative open`。

查找行为：

- 如果用户提供了 `<store>/<initiative>`，使用该确切存储选择器。
- 如果用户提供了 `<initiative> --store <store>`，使用该确切存储选择器。
- 如果用户仅提供了 `<initiative>`，搜索已注册的上下文存储，并在恰好有一个完全匹配时继续。
- 如果多个存储包含相同的倡议 id，停止并显示匹配的存储，提示使用 `<store>/<initiative>` 或 `--store` 重试。
- 如果没有完全匹配，不要静默打开最接近的匹配。在可用时显示少量可能的匹配，加上运行 `openspec initiative list` 的提示。
- 如果某些已注册的存储无法读取，保持结果保守。除非用户提供了显式的存储选择器，否则不要选择在不可读的存储后面可能存在歧义的匹配。

交互式 UX 可以让人类从建议中选择。JSON 和非交互式 UX 应返回结构化的错误和建议，而不进行提示。

工作区名称行为：

- 可选的位置参数工作区名称保持为本地视图标识。
- 如果用户使用 `--initiative` 提供了工作区名称，创建或重用该命名的本地视图。
- 如果用户省略了工作区名称，在无歧义时创建或重用从倡议 id 派生的友好默认名称。
- 对于名称冲突或同一倡议存在多个现有本地视图的情况，让人类交互式选择，或在非交互式模式下要求显式的工作区名称。

### 打开目标

状态：已决定。

默认打开倡议目录，而非整个上下文存储。

面向用户的行为：

```bash
openspec workspace open --initiative billing-launch
```

打开一个聚焦的本地视图：

```text
工作区根目录中的生成文件
context-store/initiatives/billing-launch/
选定的本地仓库/文件夹
```

默认不应打开整个上下文存储。

理由：

- 用户询问的是某个倡议，因此打开的上下文应聚焦于该倡议。
- 代理接收较少的无关共享上下文。
- 不相关的倡议和共享文件默认不暴露。
- 本地视图更易于理解：生成的工作区根加上此倡议加上选定的实现根。

生成的指导和 JSON 输出仍应报告上下文存储根以及更广泛的上下文存在。后续的显式选项可以打开完整的上下文存储，例如 `--context-scope store` 或 `--include-store`，但广泛的存储范围不是 Item 10 的默认设置。

### 本地视图记录

状态：已决定。

使用一个私有本地视图记录：根 `workspace.yaml` 文件。

```yaml
version: 1
name: billing-launch
context:
  kind: initiative
  store:
    id: platform
    selector:
      kind: registry
      id: platform
  initiative:
    id: billing-launch
links:
  repo-a: /Users/me/repos/repo-a
  repo-b: /Users/me/repos/repo-b
preferred_opener: codex
tools:
  - codex
```

此决策涵盖了概念上的记录形态，以及生成的运行时文件不是持久状态的事实。

如果用户通过本地路径选择了上下文存储，私有工作区记录可以保留该运行时本地的选择器，而不更改已检入的仓库元数据：

```yaml
context:
  kind: initiative
  store:
    id: platform
    selector:
      kind: path
      path: /Users/me/context/platform
      observed_id: platform
  initiative:
    id: billing-launch
```

上下文绑定是可选的。用户也可以创建不链接到任何倡议的工作区：

```yaml
version: 1
name: team-a-local
context: null
links:
  repo-a: /Users/me/repos/repo-a
  repo-b: /Users/me/repos/repo-b
preferred_opener: codex
tools:
  - codex
```

这是一个一等的工作区形态，而不仅仅是倡议打开的边缘情况。Item 10 应在添加倡议感知打开的同时保留自定义的非倡议工作区。

### 工作区存储和生成的文件

状态：已决定。

将每个私有工作区视图存储在用户的 OpenSpec 全局数据目录下，按工作区名称键控：

```text
getGlobalDataDir()/workspaces/<workspace-name>/
```

工作区名称是本地标识。选定的存储和倡议（如有）是私有记录内部的数据；它们不定义存储路径。这使工作区 API 足够通用，适用于非倡议链接的自定义本地视图。

初始形态：

```text
getGlobalDataDir()/workspaces/<workspace-name>/
  workspace.yaml
  AGENTS.md
  <workspace-name>.code-workspace
  .codex/
    skills/
  .claude/
    skills/
```

`workspace.yaml` 是持久的私有视图记录，也是 Item 10 中唯一的视图文件。其他文件是由 OpenSpec 拥有的生成运行时支持。它们可能被 `workspace open`、`workspace update` 或未来显式的准备界面覆盖。

不要为 Item 10 添加单独的生成输出目录。受管理的工作区根已经是私有的生成视图。

倡议打开默认值：

- 如果用户提供了工作区名称且没有工作区存在，创建绑定到选定倡议的工作区。
- 如果用户提供了工作区名称且它已指向同一倡议，重用它并重新生成运行时文件。
- 如果用户提供了工作区名称且它没有上下文绑定，仅在获得用户明确确认后将其绑定到选定倡议；在非交互式模式下，失败并要求显式的未来重新绑定/更新界面。
- 如果用户提供了工作区名称且它指向不同的倡议或上下文，不要静默重新指向。以清晰错误停止并要求显式的未来重新绑定/更新界面。
- 如果用户省略了工作区名称且恰好一个现有工作区指向选定倡议，重用它。
- 如果用户省略了工作区名称且没有现有工作区指向选定倡议，仅在派生名称未被使用时创建从倡议 id 派生的友好默认工作区名称。
- 如果派生的工作区名称与另一个工作区冲突，要求显式的工作区名称或显示匹配的工作区选择，而不是将冲突隐藏在路径约定背后。
- 如果多个工作区指向同一倡议，让用户选择或在非交互式模式下要求显式的工作区名称。

### 生成的运行时文件

状态：已决定。

在工作区根目录生成运行时文件，位于 `workspace.yaml` 旁边。

```text
getGlobalDataDir()/workspaces/<workspace-name>/
```

生成的文件可以包含 `AGENTS.md`、技能、启动提示和生成的编辑器工作区文件。

重新生成行为：

- `workspace open` 在启动开启器之前重新生成受管理的运行时文件。
- `workspace update` 重新生成受管理的运行时文件，而不更改持久的本地视图选择，除非用户要求状态变更。
- 生成的文件由 OpenSpec 拥有，每次可能被覆盖。
- `workspace.yaml` 不是生成输出，除非本地视图记录本身发生变化，否则不应被覆盖。

### 运行时标识

状态：已决定。

使用 `getGlobalDataDir()` 作为运行时本地边界。它已经是跨平台的，并解析为 macOS、Linux、Windows、Codespaces、WSL、SSH 主机和容器的适当用户数据目录。

`workspace.yaml` 中的本地路径仅在写入它们的运行时中有效。如果同一用户从另一个运行时打开同一倡议，他们在该运行时创建或重新链接该运行时的的工作区。Item 10 不应添加路径转换、共享机器标识或额外的 `<runtime-id>` 路径段。

### Prepare/JSON 界面

状态：已决定。

保留 `workspace open --json` 作为同一打开操作的机器面向收据。不要为 Item 10 添加 `--prepare-only`。

JSON 响应应对代理和桌面集成有用，而不仅仅是一个成功布尔值。它应包含工作区名称、工作区根、生成的文件路径、选定的上下文、打开的根、跳过或缺失的根、开启器、启动状态和警告。

面向人类的行为保持为正常的 `workspace open` 输出。JSON 模式适用于在 OpenSpec 准备好工作区根并尝试请求的打开后需要结构化事实的工具。

### 打开时缺失路径

状态：已决定。

工作区打开应对选定的倡议/上下文严格，对可选的已链接本地路径宽容。

- 如果选定的倡议无法解析，在启动前失败。
- 如果上下文存储或倡议路径不可用，在启动前失败并指向上下文存储注册/doctor 指导。
- 如果已链接的仓库或文件夹缺失，警告并跳过该根；不要阻塞仅上下文或部分链接的打开。
- 人类输出应列出跳过的链接并建议 `workspace doctor` 或重新链接指导。
- JSON 输出应包含跳过或缺失的根以及警告。

### Codex Desktop

状态：已决定。

将生成的工作区根作为 Codex Desktop 项目打开。通过生成的指导和 `workspace open --json` 响应展示附加的倡议路径和已链接的仓库/文件夹路径。

不要依赖 Desktop 多根自动化来完成 Item 10。如果 Desktop 后续有更清晰的多根契约，它可以在不改变工作区存储模型的情况下作为增强功能。

### 编辑边界

状态：已决定。

Item 10 仅发出建议性的边界。生成的上下文应区分协调上下文与实现目标，但不应强制执行写入限制。

生成的视图应将倡议/上下文存储文件标记为共享协调上下文，将已链接的仓库/文件夹标记为选定时的本地实现上下文。强制执行可以稍后添加。

## 首次运行 UX 草图

状态：推迟到第一个实现切片之后。

此草图捕获最终的人类交互流程。Item 10 不应依赖构建完整的引导式设置向导；第一个实现可以先使用显式标志和结构化错误。

```text
找到倡议：platform/billing-launch
此运行时不存在本地工作区视图。

创建本地视图？
> 仅打开上下文
  链接现有的本地仓库/文件夹
  取消
```

此首次运行流程中的任何选项都不应克隆、创建分支、创建工作树或创建子模块。

## 机器可读的打开契约

`workspace open --json` 是生成的运行时上下文的机器可读契约。Item 10 不应创建单独的机器可读视图文件；持久的视图记录是 `workspace.yaml`。

JSON 响应应告知代理：

- schema 版本
- 工作区名称和工作区根
- 选定的倡议 id、标题和路径
- 选定的上下文存储 id 和路径
- 生成的文件路径
- 打开的根
- 跳过或缺失的根
- 已知时已链接的仓库本地变更
- 建议性的编辑边界
- 下一步修复命令
- `workspace open --json` 产生时的警告和启动状态

如果未选择实现目标，`allowedEditRoots` 应为空或显式建议性。

确切的 schema 可以在实现过程中演进，但 JSON 响应应使生成的视图足够自我描述，以便代理和桌面集成无需解析人类输出。

## 向前兼容

初始的 `context` 记录支持选定的上下文存储和倡议。不要将 YAML 解析器设计得过于狭窄，以至于未来的记录无法添加可配置变更家园、产物家园、目标绑定或其他集合/视图元数据的字段。

## 兼容性说明

当前的 beta 工作区实现创建了一个包含 `changes/`、`AGENTS.md`、`.gitignore`、`.openspec-workspace/workspace.yaml`、`.openspec-workspace/local.yaml` 和持久 `.code-workspace` 文件的受管理根。

Item 10 预期的新形态是根 `workspace.yaml` 加上受管理工作区根处的生成运行时文件。现有的 beta 工作区应被视为兼容性输入。除非实现切片有意包含该迁移，否则所有 beta 内部内容的迁移或移除均推迟。

对于倡议打开模型，生成的运行时文件是派生产物，而非工作区的真实依据。
