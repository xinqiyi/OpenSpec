# 拒绝倡议解析

## 状态

最终决定：现在或以后都不实现独立的 `openspec initiative resolve` 命令。

## 唯一真实来源

从 `../../direction.md` 和边界开始：

```text
上下文存储同步真相。
集合塑造真相。
倡议协调工作。
workspace 打开本地视图。
变更实现 repository 拥有的切片。
```

事项 8 已经确立了 repository 本地变更可以通过可移植的检入元数据引用倡议：

```yaml
initiative:
 store: platform
 id: billing-launch
```

## 最终决定

在此切片或任何未来切片中，都不发布 `openspec initiative resolve <id>` 作为面向用户的命令。

早期的命令框架过于宽泛。它试图将倡议身份、workspace 本地路径、显式 repository 根目录和链接的 repository 本地变更合并到一个新的 CLI 界面中。这使得该命令看起来具有权威性，尽管倡议并不拥有本地 repository 路径、repository 参与或实施状态。

## 为什么不需要该命令

如果用户只有上下文存储的克隆，OpenSpec 已经可以通过以下方式解析 spec 倡议：

```bash
openspec initiative show billing-launch --json
```

这回答了：

```text
这是什么倡议，哪个上下文存储包含它，spec 倡议文件夹在哪里？
```

它无法回答：

```text
哪些本地实施 repository 应存在于这台机器上？
```

因为这些信息不在上下文存储中。

如果用户有 workspace，workspace 已经是本地视图。它已经将本地 repository 和文件夹映射到这台机器上的路径。一个单独的 `initiative resolve` 命令大多会重新描述用户已经在使用的 workspace。

如果用户在 repository 中，repository 本地变更命令和状态命令已经在该 repository 中运行。用户或 agent 可以直接检查当前 repository 的变更。

## 产品规则

不要创建一个主要工作是发现 workspace 已经代表的本地路径的新命令。

规则：

- `initiative show` 仍然是 spec 倡议发现的命令。
- workspace 仍然是 repository、文件夹、上下文存储和倡议的本地视图。
- repository 本地变更仍然是实施构件。
- agent 应使用当前 workspace 或当前 repository 上下文，而不是要求独立的倡议命令推断本地可用性。
- OpenSpec 不应推断 repository 所有权、扫描任意 repository、克隆 repository、创建工作树或写入反向链接以使解析看起来比实际更智能。

## 应做之事

保持各部分独立：

- 使用 `openspec initiative show <id> --json` 定位 spec 的共享上下文。
- 使用 workspace 命令来设置、链接、重新链接、列出、打开、更新和诊断本地视图。
- 使用 repository 本地的 `openspec new change ... --initiative ...` 和 `openspec set change ... --initiative ...` 创建从 repository 工作到倡议上下文的持久链接。
- 在拥有 repository 内使用 `openspec status --change <id> --json` 检查实施进度。

如果未来的 workspace workflow 需要打开特定倡议的视图，它应设计为 workspace 行为的一部分，而不是作为独立的倡议解析命令。

## 推迟或替换的范围

以下想法不属于事项 9 的实施：

- `openspec initiative resolve <id>`
- 扫描所有已注册的 workspace
- 扫描磁盘上的所有 repository
- 基于显式 `--path` 的倡议解析
- Git 远程匹配
- repository 所有权推断
- 克隆、获取、拉取、推送
- 分支或工作树创建
- 倡议反向链接
- 进度仪表板
- 本地可用性仪表板

## 路线图处理

事项 9 是一个仅决策的检查点。它记录了独立的倡议解析被永久拒绝。

路线图框架：

```text
事项 9. 拒绝倡议解析

决定：现在或以后都不添加 `openspec initiative resolve`。倡议发现属于
`initiative show`；本地路径映射属于 workspace；实施进度属于 repository 本地变更。
```

## 下一个有用的工作

下一个有用的实施切片是 workspace 倡议打开，无需独立的解析先决条件。
