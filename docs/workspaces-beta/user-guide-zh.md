# 将 OpenSpec 与你的编程代理一起使用

Beta 说明：这是最小的可用路径。你完成本地设置。你的代理
管理 OpenSpec 工作。

## 1. 创建共享空间

```bash
openspec context-store setup
```

OpenSpec 询问上下文存储的名称、存放位置以及是否
初始化 Git。如果你不希望将存储放在特定位置，请按回车键使用管理的本地数据目录。

## 2. 让你的代理创建 Initiative

> 在 `team-context` 中创建一个名为 `billing-launch` 的 OpenSpec initiative。
> 保持简短有用。

## 3. 打开本地工作台

```bash
openspec workspace open
```

从选择器中选择 initiative。如果你还没有本地工作区视图，
OpenSpec 会为你创建一个。在创建新视图时，它还会询问
要包含哪些本地仓库或文件夹。

打开的编辑器视图首先显示链接的仓库和文件夹，附加 initiative 上下文
之后显示，最后显示一个小型的 `OpenSpec workspace` 文件夹，包含 `AGENTS.md`、
`workspace.yaml` 和生成的 `.code-workspace` 文件。

当你想要跳过选择器时，使用 `openspec workspace open --initiative team-context/billing-launch --editor`。
当你想要直接打开代理时，使用 `--agent codex-cli`、`--agent claude` 或
`--agent github-copilot` 替代 `--editor`。

## 4. 检查本地上下文

在规划工作之前，请你的代理检查已打开的工作区：

> 检查这个 OpenSpec 工作区。解析选中的 initiative，列出
> 链接的仓库或文件夹，并告诉我是否有重要的内容遗漏，
> 然后我们再探索工作。

如果缺少仓库或文件夹，告诉代理应链接哪个本地路径。
OpenSpec 不会克隆任何内容。

## 5. 在创建工件之前进行探索

将工作区作为对话发生的地方：

> 使用 initiative `team-context/billing-launch`，在这个
> 工作区中探索工作。首先阅读 initiative 上下文和链接的仓库上下文。不要
> 立即创建变更；帮助我决定应该提议什么以及
> OpenSpec 工件应该存放在哪里。

## 6. 准备就绪时要求草稿

当探索已收敛时，请代理在正确的位置创建正确的
工件：

> 为所有者链接仓库创建一个草稿仓库本地 OpenSpec 提案，
> 并将其链接到 `team-context/billing-launch`。自行解析工作区和 initiative
> 上下文，从正确的仓库运行所需的 OpenSpec 命令，并
> 报告你创建的文件。

## 小提示框

在此 Beta 流程中，OpenSpec 不会克隆、同步、分支或跟踪进度仪表板。
它为你提供共享的 initiative 上下文、本地工作区视图，
以及链接回更大目标的仓库本地计划。工作区是
你和代理协作的地方；可持久化的计划工件应存放在
上下文存储的 initiative 或所有者仓库中，而非工作区根目录。
