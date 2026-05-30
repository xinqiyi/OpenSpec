# 添加以 agent 为先的倡议发现

## 状态

实施完成；验证进行中。

## 权威来源

从 `../../direction.md` 开始。

此项目之所以存在，是因为预期的 workflow 是以 agent 为先的：

```text
使用倡议 billing-launch，探索 API 工作并创建 proposal。
```

在 repository 本地链接、本地解析或 workspace 打开可以工作之前，agent 需要一个能够回答以下问题的小型命令：

- 用户指的是哪个倡议？
- 哪个上下文存储包含权威倡议？
- 倡议元数据在哪里，agent 应检查哪个根目录？

## 目标

添加以 agent 为先的倡议发现，而不将 `show` 变成阅读器、进度仪表板、repository 解析器或 workspace 启动器。

## 已锁定的方向

- `initiative show <id>` 是一个定位/发现命令。
- 它应返回身份、上下文存储位置、倡议位置和倡议元数据路径。
- 它不应拼接 markdown、总结文件内容、计算进度、解析 repository、列出关联变更或打开 workspace。
- 默认查找搜索所有本地注册的上下文存储。
- `--store <id>` 过滤到某个已注册的存储。
- `--store-path <path>` 保留为显式本地路径的应急出口。
- 跨存储的重复倡议 ID 是歧义的。命令不应自动选择一个匹配项。
- 在默认全存储查找中，不可读的存储使查找不完整。命令应失败，而不是静默返回可能错误的唯一匹配。
- 显式 `--store` 和 `--store-path` schema 只考虑所选存储。

## 输出合约方向

第一个 JSON 合约应是解析器/读取指针投影，而非 `initiative.yaml` 的完整序列化。

建议的成功形状：

```json
{
 "context_store": {
 "id": "platform",
 "root": "/path/to/platform-context"
 },
 "initiative": {
 "version": 1,
 "id": "billing-launch",
 "title": "Billing Launch",
 "summary": "协调计费启动工作。",
 "created": "2026-05-21",
 "root": "/path/to/platform-context/initiatives/billing-launch",
 "store_path": "initiatives/billing-launch",
 "metadata_path": "/path/to/platform-context/initiatives/billing-launch/initiative.yaml"
 },
 "status": []
}
```

已锁定的字段决策：

- 保留 `initiative.version`。
- 保留 `initiative.created`。
- 保留 `initiative.id`、`title`、`summary`、`root`、`store_path` 和 `metadata_path`。
- 保留 `context_store.id` 和 `root`。
- 从 `initiative show` v1 中省略 `context_store.source`。它是选择器来源，而非上下文存储身份。现有的 create/list 输出可以暂时保持不变。
- 从 v1 中省略顶级 `resolution` 字段。
- 从 v1 投影中省略 `initiative.status`。
- 从 v1 投影中省略 `initiative.owners`。
- 从 v1 投影中省略任意 `initiative.metadata`。
- 从 v1 投影中省略 `files` 列表。
- 省略顶级 `matches`。
- 将歧义和不完全查找候选者放在相关的诊断条目下，如 `status[0].details.matches`。
- 保留顶级 `status` 仅作为命令诊断，而非倡议工作进度。

## 仍需决定

- 最小 v1 切片无待定项。

## 人类输出方向

成功输出应保持定位器聚焦：

```text
OpenSpec 倡议：Billing Launch

ID：billing-launch
摘要：协调计费启动工作。
上下文存储：platform
位置：/path/to/platform-context/initiatives/billing-launch

文件：
 元数据：/path/to/platform-context/initiatives/billing-launch/initiative.yaml
```

错误输出应保持简洁：

- 未找到：说明在注册的上下文存储中未找到该倡议，并建议 `openspec initiative list`。
- 歧义：显示匹配的存储和路径，然后建议 `openspec initiative show <id> --store <store>`。
- 查找不完整：说明某些上下文存储无法读取，包含部分匹配（如有），然后建议 `openspec context-store doctor`。

## 文件列表方向

`initiative show` 不应在 v1 中列出倡议文件夹内容。

只有 `initiative.yaml` 是识别和验证倡议所必需的。所有其他文件都是 schema/配置相关的，可能因团队而异。一旦命令解析了 `initiative.root`，agent 可以使用常规文件系统工具检查文件夹。以后基于 schema 的视图可以暴露重要文件，而无需硬编码当前的默认 template 文件名。

## 补全方向

为以下内容添加静态 shell 补全元数据：

```text
initiative show <id> --store <id> --store-path <path> --json
```

在此切片中不添加已注册存储 ID 或倡议 ID 的动态补全。

## 核心读取操作方向

添加一个专注的 `readInitiative` 操作用于精确查找。

行为：

- 当倡议文件夹或 `initiative.yaml` 不存在时返回 `null`。
- 当 `initiative.yaml` 存在但无效时抛出异常。
- 当解析后的 `initiative.yaml` ID 与文件夹 ID 不匹配时抛出异常。
- 不扫描不相关的倡议文件夹。

## 查找错误优先级

对于默认全存储查找，任何不可读的已注册存储都使查找不完整。

如果一个或多个可读存储包含该倡议，同时一个或多个其他存储无法读取，主要错误仍应为 `initiative_lookup_incomplete`，而非成功或歧义。在诊断细节中包含任何可读的部分匹配。

显式 `--store` 和 `--store-path` schema 限定于所选存储，不检查不相关的已注册存储。

无效的确切倡议文件夹是损坏的共享状态，而非"未找到"。

如果 `initiatives/<id>/initiative.yaml` 存在但无效或 ID 不匹配，`initiative show` 应以无效倡议诊断失败。在默认全存储查找中，不可读的存储仍然优先作为 `initiative_lookup_incomplete`，因为完整的候选集不可知。

## 明确排除在外

- 顶级 `openspec show` 集成。
- Markdown 内容包或生成的上下文包。
- repository 本地变更中检入的倡议快照。
- repository 本地变更链接。
- 本地 repository/workspace 解析。
- workspace 打开。
- Git 同步状态、脏状态、远程 repository、拉取、推送或冲突。
- 倡议进度或状态仪表板。
