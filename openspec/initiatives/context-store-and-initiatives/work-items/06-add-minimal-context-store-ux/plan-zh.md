# 添加最小上下文存储 UX

## 状态

最小 context-store CLI 和全存储倡议列表已实现。

## 真实源

从 `../../direction.md` 开始。

当前路线图顺序为：

```text
上下文存储同步事实。
集合塑造事实。
倡议协调工作。
workspace 打开本地视图。
变更实现 repository 自有切片。
```

该项目存在的原因是，agent 优先的倡议 workflow 在 repository 本地交接和 workspace 打开变得连贯之前，需要一个可用的共享存储。

## 目标

让用户或 agent 能够创建、注册、列出和诊断本地上下文存储，而无需了解内部注册表布局。

## agent 优先框架

预期的用户提示更接近：

```text
使用倡议 billing-launch，探索 API 工作并创建 proposal。
```

在 agent 能这样做之前，它需要回答：

- 本地注册了哪些上下文存储？
- 哪个存储包含指定的倡议？
- 已注册的存储路径是否有效？
- 存储元数据是否存在且一致？
- 如果还没有存储，应该如何创建一个？

该工作项应提供这些原语。它不应实现 repository 本地倡议关联、倡议解析、workspace 打开或进度/状态仪表板。

## 当前锁定的方向

- 目前保留面向用户的术语 `store`；命名完善被推迟。
- 在此切片中使用 `context-store` 作为顶层 CLI 命名空间。它对 agent 更明确，避免了重载宽泛的顶层 `store` 命令。仅在上下文已限定时保留 `store` 作为简写，例如 `initiative list --store <id>`。
- `context-store setup <id>` 应创建或使用本地文件夹，写入可移植的存储元数据，注册本地路径，并可选择初始化 Git。
- 当 `--path` 省略时，`context-store setup <id>` 应默认使用 `./<id>`。
- 使用当前目录应是显式的 `--path .`；设置不应将当前 repository 静默转换为上下文存储。
- 实际的共享上下文存储应在磁盘上可见，而不是隐藏在 XDG/全局数据下。XDG/全局数据仅用于机器本地注册表。
- `context-store register <path>` 应注册现有的克隆或文件夹。
- 注册意味着"此文件夹已存在于我的机器上；将其记住为已知的上下文存储。"它不应创建文件夹、初始化 Git、拉取、推送、提交或创建远程。
- 当元数据缺失时，默认从 repository 或文件夹名称推断存储 ID。
- 可移植的存储元数据确切为 `.openspec-store/store.yaml`。它应被检入上下文存储 repository，目前仅包含可移植标识：

```yaml
version: 1
id: team-context
```

- 不要将后端配置、本地路径、远程 URL、集合配置、同步策略或权限放在 `store.yaml` 中。
- 如果将来需要集合/存储配置，添加一个单独的显式文件，而不是默认扩展标识文件。
- 机器本地注册表状态应保持在检入的存储之外，并将存储 ID 映射到本地路径。
- 注册不应拉取、推送、提交或创建远程 repository。
- 远程 URL 注册或克隆糖语法可以在以后添加。
- `initiative list` 应默认在所有已注册存储中查找。`--store` 应过滤到一个存储，`--store-path` 应保留作为显式 escape hatch。
- 人类输出应保持紧凑，目前不显示"状态"列。

## 建议的命令格式

```bash
openspec context-store setup <id> [--path <path>] [--init-git|--no-init-git] [--json]
openspec context-store register <path> [--id <id>] [--json]
openspec context-store list [--json]
openspec context-store doctor [id] [--json]
openspec initiative list [--store <id>] [--store-path <path>] [--json]
```

## 命令行为

### `context-store setup`

`context-store setup <id>` 创建或使用可见的本地存储根目录，并在当前机器上注册它。

锁定的行为：

- 当 `--path` 省略时，默认路径为 `./<id>`。
- 仅允许通过显式的 `--path .` 进行当前目录设置。
- 缺失的文件夹将被创建。
- 当元数据缺失或与请求的 ID 匹配时，允许使用现有文件夹。
- 在此切片中，不支持没有上下文存储元数据的非空文件夹进行设置。
- 存在不同 ID 的现有元数据将失败。
- 文件路径将失败。
- 当 `.openspec-store/store.yaml` 缺失时写入。
- 存储在机器本地注册表中注册。
- 交互式 TTY schema 在既未提供 `--init-git` 也未提供 `--no-init-git` 时提示 Git 初始化；默认答案为是。
- `--json`、非 TTY 执行、`--init-git` 和 `--no-init-git` 不会提示。
- 仅在提示答案为是或传递了 `--init-git` 时才初始化 Git。
- 设置不提交、推送、拉取、创建远程或创建托管 repository。
- 如果用户想要初始化现有的非空文件夹，失败并给出清晰的消息，建议提交用例或对现有上下文存储使用 `context-store register`。

建议的人类输出：

```text
上下文存储设置完成

ID：team-context
位置：/Users/me/work/team-context
元数据：/Users/me/work/team-context/.openspec-store/store.yaml
注册表：/Users/me/.local/share/openspec/context-stores/registry.yaml
Git：已初始化
```

### `context-store register`

`context-store register <path>` 将现有的本地文件夹或克隆记录为当前机器上的已知上下文存储。

锁定的行为：

- 路径必须已存在且为目录。
- 如果 `.openspec-store/store.yaml` 存在，使用其 ID。
- `--id` 可以确认元数据 ID，但不能与其冲突。
- 如果元数据缺失，除非传递了 `--id`，否则从文件夹或 repository 名称推断 ID。
- 推断直接使用文件夹或 repository 名称原样，然后应用正常的上下文存储 ID 验证。在此切片中不要做巧妙的 spec 化。
- 缺失的元数据会被写入。
- 机器本地注册表会被更新。
- 相同 ID 和相同路径是幂等的成功。
- 相同 ID 和不同路径目前失败；未来的 `--replace` 可以使替换显式化。
- 相同路径已以不同 ID 注册目前失败。
- 注册不会创建文件夹、初始化 Git、拉取、推送、提交、创建远程或克隆。

建议的人类输出：

```text
上下文存储已注册

ID：team-context
位置：/Users/me/src/team-context
元数据：/Users/me/src/team-context/.openspec-store/store.yaml
注册表：/Users/me/.local/share/openspec/context-stores/registry.yaml
```

### `context-store list`

`context-store list` 是本地注册表的索引视图。

锁定的行为：

- 读取本地注册表。
- 仅显示已注册的 ID 和位置。
- 按存储 ID 排序。
- 不检查元数据、路径健康、Git、同步、远程、脏状态或冲突。
- 不修改任何内容。
- 不打印健康警告；健康属于 `context-store doctor`。

建议的人类输出：

```text
OpenSpec 上下文存储（2）

ID 位置
platform /Users/me/src/platform-context
team-context /Users/me/src/team-context
```

空输出：

```text
没有已注册的上下文存储。

下一步：
 openspec context-store setup team-context
 openspec context-store register /path/to/context-store
```

### `context-store doctor`

`context-store doctor [id]` 是不进行修改的健康和修复表面。

锁定的行为：

- 默认检查所有已注册的存储。
- 传递 `id` 时检查一个存储。
- 检查注册表存在性、路径存在性、目录格式、元数据存在性、元数据解析和元数据 ID 匹配。
- 包括简单的 Git repository 存在性检查。
- 在此切片中不检查脏状态、分支、远程、同步、拉取/推送或冲突。
- 不修改任何内容。

空输出：

```text
没有已注册的上下文存储。
```

建议的人类输出：

```text
上下文存储诊断

team-context
 位置：/Users/me/src/team-context
 元数据：正常
 Git：检测到 repository
 问题：无
```

### `initiative list`

`initiative list` 成为跨已注册存储的 agent 友好发现命令。

锁定的行为：

- 不带 `--store` 或 `--store-path` 时，列出所有可读已注册存储中的倡议。
- 如果没有已注册的上下文存储，打印简洁的空消息。
- 按存储 ID 排序，然后按倡议 ID 排序。
- 在人类输出中不显示"状态"列。
- 不打印详细的健康诊断。
- 如果某些存储无法读取，仍显示可读存储中的倡议，并打印一条指向 `context-store doctor` 的小警告。
- 如果所有已注册的存储都无法读取，打印简洁的失败/空消息并指向 `context-store doctor`。
- 使用 `--store <id>` 过滤到一个已注册的存储。
- 使用 `--store-path <path>` 从该显式存储路径列出。
- 过滤后的 `--store` 或 `--store-path` schema 在该存储无法读取时直接失败，因为没有后备存储。

建议的全存储输出：

```text
OpenSpec 倡议（3 个，来自 2 个存储）

ID Store 标题
billing-launch platform 计费启动
docs-refresh platform 文档刷新
api-cleanup team API 清理

某些已注册的上下文存储无法读取。
运行：openspec context-store doctor
```

无已注册存储的输出：

```text
未找到倡议，因为没有已注册的上下文存储。
```

建议的过滤输出：

```text
platform 中的 OpenSpec 倡议（2 个）

ID 标题
billing-launch 计费启动
docs-refresh 文档刷新

位置：/Users/me/src/platform-context
```

## 边界

不在此项中实现：

- 倡议 `show`
- repository 本地变更元数据
- `new change --initiative`
- 倡议本地解析
- workspace 倡议打开
- 同步、拉取、推送、远程 repository 创建或冲突处理

## 剩余决策

实施前无待定项。JSON 格式可以遵循现有命令 schema：顶层结果对象加上 `status` 诊断数组。部分成功返回退出码 0 并附带警告诊断；完全失败返回非零退出码。

## 已实现的切片

- 添加了 `openspec context-store setup/register/list/doctor`。
- 从顶层 CLI 注册了 `context-store` 命令。
- 初步将 shell 补全元数据排除在范围之外；静态元数据后来与已发布的命令表面一起添加。
- 实现了严格的 CLI 注册策略，未更改宽松的低级注册表面。
- 添加了默认 `./<id>`、显式 `--path .`、交互式 Git init 提示、非交互式/JSON 无提示行为、非空目录拒绝和元数据写入的设置行为。
- 添加了现有文件夹的注册行为、从文件夹名称推断 ID、元数据写入、ID/路径冲突拒绝和注册表更新。
- 添加了列表行为，仅作为注册表索引。
- 添加了 doctor 行为，用于注册表/路径/元数据健康和简单的 Git 存在性。
- 更新了 `initiative list`，使无选择器时遍历所有已注册存储，`--store` 过滤，`--store-path` 保持为 escape hatch，人类输出紧凑，全存储部分成功返回警告诊断。
