# 面向代理的 OpenSpec CLI 操作手册

Beta 说明：工作区和 initiative 流程可用，但规模仍然较小。建议使用
简单的命令、清晰的路径和简短的状态报告。

## 首先解析上下文

在需要精确路径时使用 JSON。

```bash
openspec context-store list --json
openspec initiative list --json
openspec initiative show <store>/<initiative> --json
openspec workspace doctor --json
```

当用户从已打开的工作区工作时，将工作区视为
本地视图。使用 `workspace doctor --json` 读取链接的仓库/文件夹和
选中的 initiative。不要假设当前目录就是应该拥有
实现工件的仓库。

## 非交互式设置上下文存储

人类可以运行 `openspec context-store setup` 并回答提示。代理应
显式传递设置输入。

```bash
openspec context-store setup team-context --no-init-git --json
openspec context-store setup team-context --path /path/to/team-context --init-git --json
```

使用 `context-store unregister <id> --json` 忘记本地注册，同时
保留文件不变。仅当用户明确要求删除本地
context-store 文件夹时，才使用 `context-store remove <id> --yes --json`。

## 在上下文存储中创建 Initiative

在上下文存储中创建共享协调上下文。

```bash
openspec initiative create billing-launch --store team-context --title "计费启动" --summary "让计费系统上线而不丢失方向。"
```

然后编辑上下文存储中的 initiative 文件：

- `requirements.md`
- `design.md`
- `decisions.md`
- `questions.md`
- `tasks.md`

## 从工作区探索或提议

当用户要求从工作区探索或起草工作时：

1. 使用 `openspec workspace doctor --json` 解析工作区。
2. 使用 `openspec initiative show <store>/<initiative> --json` 解析 initiative。
3. 检查链接的仓库或文件夹，确定可能的所有者仓库。
4. 如果所有权不明确，询问用户哪个链接的仓库应拥有
   仓库本地的 OpenSpec 变更。
5. 从所有者仓库运行 explore/propose 工作流命令，而非从
   工作区根目录。

工作区是对话的驾驶舱。它不是实现计划的
持久归宿。

## 从所有者仓库创建变更

仓库本地的变更属于拥有该项工作的仓库。

```bash
openspec new change add-billing-api --initiative team-context/billing-launch
```

以所有者仓库作为当前工作目录运行此命令。不要
要求用户输入，也不要从工作区根目录运行与 initiative 关联的变更创建。
如果你只知道工作区，先解析链接的仓库路径。

创建变更后，报告所创建文件的绝对路径以及
你使用的 initiative 链接。

## 在猜测之前使用 Doctor

```bash
openspec workspace doctor --workspace billing-launch --json
openspec context-store doctor --json
```

## 暂不承诺

- 自动同步、拉取、推送或冲突处理。
- 克隆仓库。
- 创建分支、工作树或子模块。
- 工作区 apply、verify 或 archive。
- 进度仪表板。
- 强制编辑边界。
