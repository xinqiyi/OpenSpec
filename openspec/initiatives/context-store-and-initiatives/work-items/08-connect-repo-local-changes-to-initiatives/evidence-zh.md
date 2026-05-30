# 连接 repository 本地变更与倡议的实证

## 决策 1：倡议链接位置

倡议链接应位于 repository 本地变更的 `.openspec.yaml` 中。

示例：

```yaml
schema: spec-driven
created: 2026-05-22
initiative:
 store: platform
 id: billing-launch
```

这既保持了 repository 的实现所有权，又保留了对 spec 化倡议上下文的持久引用。

链接不应包含本地路径、复制的倡议正文或倡议存储中的反向链接。

## 研究笔记

- `createChange()` 已经为每个变更写入 `.openspec.yaml`。
- `ChangeMetadataSchema` 当前允许 schema、created、goal 和 affected-area 字段。Item 8 可以使用 `initiative` 扩展该 schema。
- archive 操作会移动整个变更目录，因此倡议链接将随已 archive 的变更一起移动。
- 在此切片中，apply、validate 和 archive 不应要求上下文存储可用。

## 决策 2：创建命令形态

倡议关联的创建应使用 `openspec new change` 配合 `--initiative`。

第一个切片支持的形式：

```bash
openspec new change add-billing-api --initiative billing-launch --json
openspec new change add-billing-api --initiative platform/billing-launch --json
openspec new change add-billing-api --initiative billing-launch --store platform --json
```

这保持操作归 repository 所有。倡议是变更上的一个引用，而非创建或拥有变更的行为者。

第一个切片还应为 `new change` 添加 `--json`，以便 agent 能够捕获创建的变更路径、元数据路径和倡议引用。

## 决策 3：倡议查找行为

裸 `--initiative <id>` 应重用 `initiative show` 的查找语义。

它搜索所有已注册的上下文存储，仅当查找完成且恰好有一个可读存储包含该倡议时成功。

显式的存储选择器可缩小查找范围：

```bash
openspec new change add-billing-api --initiative platform/billing-launch
openspec new change add-billing-api --initiative billing-launch --store platform
openspec new change add-billing-api --initiative billing-launch --store-path ./context
```

`--store-path` 验证显式路径并读取其存储 id，但不会自动注册该存储。元数据仍仅存储可移植的存储 id 和倡议 id。

在倡议查找完成且无歧义之前，不应写入 repository 本地元数据。

## 决策 4：V1 仅限 repository 本地

Item 8 应仅支持 repository 本地变更的倡议链接。

如果 `openspec new change <id> --initiative ...` 从 workspace planning 家园运行，v1 应拒绝并告知用户从拥有实现计划的 repository 运行该命令。

现有的 workspace planning 变更保持兼容性行为，在此切片中不应获得倡议链接功能。

这保持了边界：倡议协调共享上下文，repository 本地变更拥有实现计划，workspace 打开本地视图。

## 决策 5：V1 中无 repository 拥有权匹配

Item 8 不应验证当前 repository 是否被倡议命名、拥有或从中推断。

创建带有倡议链接的 repository 本地变更记录的是参与该倡议的行为。它不证明拥有权、repository 影响或倡议区域的覆盖范围。

repository 拥有权匹配可以在倡议解析或显式倡议元数据拥有真实的 repository/区域模型后再行考虑。

## 决策 6：JSON 和人类可读输出

创建输出应保持事实性且最小化。

人类可读输出应确认：

- 创建的变更 id 和位置
- schema
- 倡议链接 `{ store, id }`

JSON 输出应包含：

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

输出不应包含 `next` 或其他建议的 workflow 操作。API 响应应报告操作结果或错误；选择下一步操作是 agent 的责任，取决于更广泛的上下文。

## 决策 7：现有变更恢复

Item 8 应包含一个友好的恢复命令，用于现有 repository 本地变更：

```bash
openspec set change add-billing-api --initiative billing-launch --json
openspec set change add-billing-api --initiative platform/billing-launch --json
openspec set change add-billing-api --initiative billing-launch --store platform --json
openspec set change add-billing-api --initiative billing-launch --store-path ../context --json
```

此命令是一个经过验证的设置器，用于已检入的 repository 本地变更元数据。在 Item 8 中，唯一支持的设置字段是倡议链接，唯一可以修改的文件是 `openspec/changes/<id>/.openspec.yaml`。

该命令不应编辑 proposal、design、tasks、specs 或倡议存储文件。它不应存储本地路径或将反向链接写入倡议。

如果请求的倡议链接已存在，该命令应作为幂等的无操作成功返回。如果不同的倡议链接已存在，该命令应失败而不写入。替换、重新链接、取消链接和 dry-run 行为均推迟。

理由：

- agent 可能在创建时忘记链接变更，因此一流的恢复路径是有用的。
- `set change` 与实际的副作用相匹配：将已验证的变更元数据写入 `.openspec.yaml`。
- 将命令范围限定在 `.openspec.yaml` 可避免创建宽泛的变更编辑面。
- `openspec change ...` 当前已弃用，`edit` 暗示打开编辑器，而 `update` 已经表示刷新本地 OpenSpec 工具或指导。

## 决策 8：状态和指令可见性

状态和指令应显示 repository 本地变更已链接到某项倡议，但不应显示或解析倡议本身。

人类可读的状态输出应显示存储的倡议引用，JSON 状态输出应包含存储的倡议 `{ store, id }`。指令输出应包含一条简洁的事实性说明，告知该变更已链接到倡议。

在 v1 中，状态和指令不应从上下文存储中读取、总结、验证或解析倡议。缺失或不可用的上下文存储不应导致 repository 本地状态或指令失败。

这使该关系在普通 repository 本地 workflow 中保持可见，同时保留边界：倡议查找和上下文读取属于倡议专用命令。

## 最新已决决策说明

日期：2026-05-23。

Item 8 的所有决策现已确认可供实现。

实现应保持第一个切片小巧：

- 轻量发布应测试倡议关联的 repository 本地变更是否有用，然后再添加门控、拥有权推断或更广泛的 workflow 集成。
- 独立的 `initiative resolve` 后来被否决；workspace 本地视图状态拥有本地路径映射。
- 来源溯源、历史/导出、契约映射和目标绑定的倡议托管变更仍是有用的未来讨论点，但不应阻塞此初始切片。

## 实现实证

日期：2026-05-23。

已实现：

- `openspec new change <id> --initiative ...` 用于 repository 本地变更，支持 `--json`、`--store` 和 `--store-path`。
- `openspec set change <id> --initiative ...` 用于现有 repository 本地变更。
- 在 `initiative: { store, id }` 下的可检入可移植元数据。
- 仅从存储元数据中获取状态和指令可见性。
- workspace 拒绝、查找失败不写入、相同链接幂等性以及不同链接冲突保护。

验证：

```bash
pnpm run build
```

结果：通过。

```bash
pnpm exec eslint src/commands/workflow/new-change.ts src/commands/workflow/set-change.ts src/commands/workflow/initiative-link.ts src/commands/workflow/instructions.ts src/commands/workflow/status.ts src/commands/workflow/shared.ts src/commands/initiative.ts src/core/artifact-graph/types.ts src/core/artifact-graph/instruction-loader.ts src/utils/change-utils.ts src/cli/index.ts
```

结果：通过。

```bash
pnpm exec vitest run test/utils/change-metadata.test.ts test/commands/change-initiative-link.test.ts
```

结果：通过，39 个测试。

```bash
pnpm exec vitest run test/commands/artifact-workflow.test.ts test/commands/initiative.test.ts test/core/artifact-graph/instruction-loader.test.ts
```

结果：通过，110 个测试。
