# 事项 9 决定：拒绝倡议解析

## 最终决定

现在或以后都不实现独立的 `openspec initiative resolve <id>` 命令。

该命令不必要，因为它试图做已经属于其他概念的工作：

- `initiative show` 找到 spec 倡议。
- workspace 是 repository 和文件夹的本地视图。
- repository 本地变更将自己链接到倡议。
- repository 本地状态报告工作进度。

## 决定 1：无命令

不需要独立的倡议命令。

如果用户只有上下文存储，`initiative show` 就足够了。如果用户有 workspace，本地视图已经由该 workspace 代表。如果用户在 repository 内部，repository 本地命令就足够了。

## 决定 2：本地解析属于 workspace

workspace 将本地 repository 和文件夹映射到一台机器上的路径。未来能感知倡议的本地打开应属于 workspace 行为。

## 决定 3：agent 行为

agent 应：

- 对共享上下文使用 `openspec initiative show <id> --json`。
- 当用户在 workspace 中工作时，使用当前 workspace 视图。
- 当用户在 repository 中工作时，使用 repository 本地命令。
- 让用户决定哪些 repository 在本地存在。

## 决定 4：被拒绝的范围

移除所有独立的解析行为：

- 没有 `initiative resolve`
- 没有全 repository 扫描
- 没有全 workspace 扫描
- 没有 `--path` 搜索根
- 没有 Git 远程匹配
- 没有克隆
- 没有工作树或分支创建
- 没有倡议反向链接
- 没有本地可用性仪表板

## 决定 5：路线图更新

将事项 9 转换为仅决策的检查点。

替换为：

```text
事项 9. 拒绝倡议解析

决定：现在或以后都不添加 `openspec initiative resolve`。倡议发现属于
`initiative show`；本地路径映射属于 workspace；实施进度属于 repository 本地变更。
```
