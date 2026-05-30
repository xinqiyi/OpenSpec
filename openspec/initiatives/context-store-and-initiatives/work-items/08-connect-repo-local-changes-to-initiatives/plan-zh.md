# 连接仓库本地变更与倡议

## 状态

已实现。下方的原始决策文本保留作为设计记录；当前的完成实证见 `tasks.md` 和 `evidence.md`。

## 真实依据

从 `../../direction.md` 和 Item 8 路线图条目开始。

相关边界为：

```text
倡议协调共享上下文。
仓库本地变更拥有实现计划。
工作区打开本地视图。
```

## 目标

让代理能够创建或链接仓库本地的 OpenSpec 变更到共享倡议，而无需复制倡议正文、存储机器本地路径或使倡议拥有仓库实现产物。

示例用户提示：

```text
使用倡议 billing-launch，为 API 工作创建一个提案。
```

## 决策

### 1. 倡议链接位置

决策：将倡议链接存储在仓库本地变更的 `.openspec.yaml` 中。

建议的元数据形态：

```yaml
schema: spec-driven
created: 2026-05-22
initiative:
  store: platform
  id: billing-launch
```

规则：

- 仅存储上下文存储 id 和倡议 id。
- 不存储本地上下文存储路径。
- 不存储本地仓库路径。
- 默认不创建已检入的 `initiative.md` 快照。
- 不向倡议写入反向链接。

理由：

- `.openspec.yaml` 已经是每个变更的机器可读元数据文件。
- 该链接是持久的仓库上下文，应与变更一起检入。
- 规范化的倡议上下文仍保留在上下文存储中。
- 元数据在团队成员和机器之间保持可移植。

### 2. 创建命令形态

决策：通过 `--initiative` 将倡议链接添加到仓库本地变更创建命令。

第一个切片支持的形式：

```bash
openspec new change add-billing-api --initiative billing-launch --json
openspec new change add-billing-api --initiative platform/billing-launch --json
openspec new change add-billing-api --initiative billing-launch --store platform --json
```

规则：

- 命令从 `new change` 出发，因为变更归仓库所有。
- `--initiative` 修改仓库本地变更创建；它不会让倡议创建或拥有该变更。
- `--json` 应添加到 `new change`，用于代理可读的交接输出。
- 单独的倡议拥有的创建命令不在第一个切片的范围内。

理由：

- 预期的用户流程是代理优先："使用倡议 X，为仓库工作创建一个提案。"
- 代理需要一个普通的仓库本地创建命令，同时也能写入倡议引用。
- 将动词根植于 `new change` 保持了变更实现仓库所有切片的边界。

### 3. 倡议查找行为

决策：为 `--initiative` 重用 `initiative show` 的查找语义。

规则：

- 裸 `--initiative <id>` 搜索所有已注册的上下文存储。
- 裸查找仅在恰好一个已注册的可读存储包含该倡议 id 时成功。
- 跨存储的重复倡议 id 因歧义而失败。
- 任何不可读的已注册存储使裸查找不完整，并在写入变更元数据之前失败。
- `--initiative <store>/<id>` 按 id 选择一个已注册的存储。
- `--initiative <id> --store <store>` 也按 id 选择一个已注册的存储。
- `--initiative <id> --store-path <path>` 验证显式的本地上下文存储路径，读取其存储 id，并仅将 `{ store, id }` 写入元数据。
- `--store-path` 不会自动注册上下文存储。
- 在查找完成且无歧义之前，不写入仓库本地倡议元数据。

理由：

- 代理可以在安全的情况下使用简短形式。
- 持久的仓库本地链接不应基于部分知识创建。
- 该行为与现有的代理优先发现语义一致。

### 4. V1 仅限仓库本地

决策：Item 8 仅支持仓库本地变更的倡议链接。

规则：

- `openspec new change <id> --initiative ...` 仅当当前规划家园是仓库本地时才创建倡议关联的变更。
- 如果命令从工作区规划家园运行，v1 拒绝并提供清晰指导，告知用户从拥有实现计划的仓库运行该命令。
- 现有的工作区规划变更保持兼容性行为，在此切片中不扩展倡议链接功能。

理由：

- 当前产品边界分配实现计划给仓库本地的 OpenSpec 变更。
- 工作区是本地视图，而非倡议工作的持久规划所有者。
- 扩展工作区规划变更将复活已被取代的工作区拥有计划模型。

### 5. 仓库拥有权匹配

决策：v1 中不尝试仓库拥有权匹配。

规则：

- 创建带有倡议链接的仓库本地变更记录的是对倡议的参与。
- 该链接不声明 OpenSpec 已验证了仓库拥有权、仓库影响或倡议区域覆盖范围。
- 命令不应仅因为当前仓库不在倡议内容中而阻塞或警告。

理由：

- Item 8 不应发明仓库拥有权或单体仓库区域语义。
- 拥有权匹配属于后续的倡议解析或显式倡议元数据。
- 保持 v1 小巧让团队在添加策略门控之前测试关联的仓库本地变更是否有用。

### 6. JSON 和人类可读输出

决策：保持创建输出事实性且最小化。

规则：

- 输出应报告命令执行的操作，而非推荐工作流下一步。
- 人类可读输出应确认创建的变更位置、schema 和倡议链接。
- JSON 输出应包含已创建变更和倡议链接的稳定字段。
- JSON 输出不应包含 `next` 命令或建议的工作流操作。
- 输出不应包含倡议摘要、仓库拥有权声明、已解析的本地上下文存储路径或进度/状态类字段。

建议的 JSON 形态：

```json
{
  "change": {
    "id": "add-billing-api",
    "path": "/repo/openspec/changes/add-billing-api",
    "metadataPath": "/repo/openspec/changes/add-billing-api/.openspec.yaml",
    "schema": "spec-driven"
  },
  "initiative": {
    "store": "platform",
    "id": "billing-launch"
  }
}
```

理由：

- CLI/API 风格的响应应陈述操作结果或错误。
- 准确选择下一步操作取决于代理上下文，应保持为代理的责任。
- 保持输出事实性可避免将变更创建与后续生命周期设计耦合。

### 7. 现有变更恢复

决策：包含一个恢复命令，用于在现有仓库本地变更上设置倡议链接。

命令形态：

```bash
openspec set change add-billing-api --initiative billing-launch --json
openspec set change add-billing-api --initiative platform/billing-launch --json
openspec set change add-billing-api --initiative billing-launch --store platform --json
openspec set change add-billing-api --initiative billing-launch --store-path ../context --json
```

规则：

- `openspec set change <id> --initiative ...` 是一个经过验证的仓库本地变更元数据设置器。
- 在 Item 8 中，唯一支持的设置字段是倡议链接。
- 该命令仅修改 `openspec/changes/<id>/.openspec.yaml`。
- 该命令不编辑 proposal、design、tasks、specs 或倡议存储文件。
- 该命令使用与 `openspec new change <id> --initiative ...` 相同的倡议查找语义。
- 如果相同的倡议链接已存在，该命令作为幂等的无操作成功返回。
- 如果不同的倡议链接已存在，该命令失败而不写入。替换、重新链接、取消链接和 dry-run 行为不属于 v1。
- 如果命令从工作区规划家园运行，它拒绝的原因与倡议关联的 `new change` 相同。

理由：

- 代理可能在变更创建时忘记传递 `--initiative`；v1 需要一个友好的恢复路径。
- `set change` 描述了实际操作：设置已检入的变更元数据，而非创建倡议拥有的关系。
- 将命令限制在 `.openspec.yaml` 可避免宽泛的编辑面。
- 避免 `openspec change ...` 因为该命名空间当前已弃用。
- 避免 `edit` 因为它暗示打开编辑器，避免 `update` 因为 OpenSpec 已将 update 用于本地指导/工具刷新。

### 8. 状态和指令可见性

决策：在状态和指令输出中显示倡议链接，但不解析或显示倡议本身。

规则：

- 人类可读的状态输出应显示变更已链接到某项倡议。
- JSON 状态输出应包含存储的倡议 `{ store, id }`。
- 指令输出应包含一条简洁的事实性说明，告知该变更已链接到倡议。
- 在 v1 中，状态和指令不得从上下文存储中读取、总结、验证或解析倡议。
- 缺失或不可用的上下文存储不得导致仓库本地状态或指令失败。
- 输出不应添加下一步建议。

理由：

- 倡议链接应在普通仓库本地工作流输出中可见，以便用户和代理不会错过该关系。
- 将可见性限制为存储的元数据可避免将上下文存储可用性引入为仓库本地工作流命令的依赖。
- 倡议解析属于倡议专用命令，而非此切片中的状态或指令。

## 未决决策

无。决策通过完成；在实现前确认决策。

## 最新建议解决方案

这些是带入实现的建议答案：

- 在状态和指令中显示存储的倡议链接，但不读取或显示倡议本身。
