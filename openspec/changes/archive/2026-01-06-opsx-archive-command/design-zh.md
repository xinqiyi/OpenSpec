## 背景

实验性 workflow（OPSX）提供了创建变更的完整生命周期：
- `/opsx:new` - 使用 schema 搭建新变更
- `/opsx:continue` - 创建下一个产物
- `/opsx:ff` - 快进所有产物
- `/opsx:apply` - 实施任务
- `/opsx:sync` - 将 delta spec 同步到主 spec

缺失的部分是 archive。现有的 `openspec archive` 命令可以工作，但是：
1. 以编程方式应用 spec（非 Agent 驱动）
2. 不使用产物图谱进行完成检查
3. 不与 OPSX workflow 理念集成

## 目标 / 非目标

**目标：**
- 添加 `/opsx:archive` skill 以完成 OPSX workflow 生命周期
- 使用产物图谱进行 schema 感知的完成检查
- 与 `/opsx:sync` 集成以实现 Agent 驱动的 spec 同步
- 在 archive 中保留 `.openspec.yaml` schema 元数据

**非目标：**
- 替换现有的 `openspec archive` CLI 命令
- 更改 CLI 命令中 spec 的应用方式
- 修改产物图谱或 schema 系统

## 决策

### 决策 1：仅 skill 实现（无新 CLI 命令）

`/opsx:archive` 将仅作为斜杠命令/skill，而不是新的 CLI 命令。

**理由**：现有的 `openspec archive` CLI 命令已经处理了核心 archive 功能（移动到 archive 文件夹、日期前缀）。OPSX 版本只需要不同的 archive 前检查和可选的同步提示，这些是更适合 skill 形式的 Agent 行为。

**考虑的替代方案**：
- 向 `openspec archive` 添加标志（例如 `--experimental`）- 被拒绝：增加了 CLI 的复杂性，更难维护两个代码路径
- 新 CLI 命令 `openspec archive-experimental` - 被拒绝：不必要的重复，Agent skill 是 OPSX schema

### 决策 2：archive 前提示同步

skill 将检查未同步的 delta spec，并在 archive 前提示用户。

**理由**：OPSX 理念是通过 `/opsx:sync` 进行 Agent 驱动的智能合并。我们不像常规 archive 命令那样以编程方式应用 spec，而是提示用户首先进行同步（如果需要）。这保持了 workflow 的灵活性（用户可以拒绝并仅 archive）。

**流程**：
1. 检查变更中是否存在 `specs/` 目录
2. 如果存在，询问："此变更有 delta spec。是否要在 archive 前将其同步到主 spec？"
3. 如果用户说是，执行 `/opsx:sync` 逻辑
4. 无论答案如何，继续进行 archive

### 决策 3：使用产物图谱进行完成检查

skill 将使用 `openspec status --change "<name>" --json` 检查产物完成情况，而不仅仅是验证 proposal.md 和 spec。

**理由**：实验性 workflow 是 schema 感知的。不同的 schema 有不同的必需产物。产物图谱知道当前 schema 的哪些产物已完成/未完成。

**行为**：
- 如果任何产物未完成，显示警告
- 不阻止 archive（用户可能有提前 archive 的正当理由）
- 列出未完成的产物，以便用户做出明智决定

### 决策 4：重用常规 archive 的 tasks.md 完成检查

skill 将解析 tasks.md 并警告不完整的任务，与常规 archive 相同。

**理由**：无论 workflow 如何，任务完成检查都是有价值的。逻辑很简单（统计 `- [ ]` vs `- [x]`），不需要特殊的 OPSX 处理。

### 决策 5：将变更移动到 archive/ 并带日期前缀

与常规命令相同的 archive 行为：移动到 `openspec/changes/archive/YYYY-MM-DD-<name>/`。

**理由**：与现有 archive 约定一致。`.openspec.yaml` 文件随变更一起移动，保留 schema 元数据。

## 风险 / 权衡

**风险**：用户对何时使用 `/opsx:archive` 与 `openspec archive` 感到困惑
→ **缓解措施**：文档应澄清：如果你一直在使用 OPSX workflow，使用 `/opsx:archive`；否则使用 `openspec archive`。两者产生相同的 archive 结果。

**风险**：如果用户拒绝并且有 delta spec，同步不完整
→ **缓解措施**：提示是信息性的；用户有完全的控制权。他们可能想在不同步的情况下 archive（例如，放弃的变更）。在输出中记录一条备注。

**权衡**：OPSX archive 中没有程序化 spec 应用
→ **已接受**：这是有意为之。OPSX 理念是 Agent 驱动的合并。如果用户想要程序化应用，请改用 `openspec archive`。
