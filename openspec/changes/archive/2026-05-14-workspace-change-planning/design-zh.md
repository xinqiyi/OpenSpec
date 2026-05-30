## 上下文

workspace 设置已经创建了 planning 主目录，记录了链接的 repository 或文件夹，存储了首选打开程序，并维护了根打开表面。为了使 workspace 变更 planning 在实践中起作用，打开的 agent 还需要从该 workspace 根目录获得可用的 OpenSpec workflow skill。

repository 本地的 `openspec init` 和 `openspec update` 已经为选择 agent 表面和生成 skill 提供了用户模型。workspace 设置应感觉类似，但安装目标是 workspace 根目录，而不是任何链接的 repository 或文件夹。

现有的 artifact workflow 假设变更位于 repository 本地的 `openspec/changes/<id>` 路径下。workspace planning 需要相同的 workflow 词汇，但 planning 主目录可能是 workspace 根目录，而实施主目录可能是链接的 repository 或文件夹。

## 目标 / 非目标

**目标：**
- 在 workspace 设置期间将 OpenSpec agent skill 安装到 workspace 根目录。
- 使用活动的全局配置文件选择在 workspace 中安装哪些 workflow skill。
- 让用户使用熟悉的 `--tools` 语义选择哪些 agent 接收 skill。
- 持久化 workspace 本地 agent skill 选择，以便后续更新可以刷新相同的 agent。
- 让用户稍后通过 `workspace update` 刷新、添加或移除 workspace 本地 skill。
- 检测并报告 workspace 本地 skill 与活动全局配置文件的差异。
- 让 `openspec config profile` 在 workspace 内部运行时提供将已更改的配置文件设置应用到当前 workspace 的选项。
- 将 workspace 用户从 repository 本地的 `openspec update` 重定向到 `openspec workspace update`。
- 为 workspace 范围的变更添加内置的 workspace planning schema。
- 在 workspace planning 路径下创建 workspace 变更。
- 表示受影响的区域，而无需将实施 artifact 强制放入链接的 repository。
- 通过状态/说明输出为 agent 提供机器可读的 planning 上下文。
- 保持 workspace 边界：设置/更新期间链接的 repository 和文件夹保持未触及。

**非目标：**
- 在 workspace 设置中生成斜杠命令。
- 通过生成 workspace 命令文件来遵守全局 `delivery: commands`。
- 将 skill 安装到链接的 repository 或文件夹。
- 添加独立于全局配置的 workspace 本地 workflow 配置文件。
- 在第一个设置 skill 步骤中解决 workspace 范围的 artifact 路径发现。
- 在第一个版本中添加单独的 artifact 上下文 CLI 命令。
- 端到端实现 workspace 应用、验证或 archive 语义。
- 更改 repository 本地的 `openspec init` 或 `openspec update` 行为。

## 决策

### 在 workspace UX 中使用 agent skill 语言

workspace 设置应询问"哪些 agent 应在此 workspace 中获得 OpenSpec skill？"，而不是使用更宽泛的"AI 工具"措辞。用户可见的操作是为编码 agent 安装 skill，目标是 workspace planning 主目录。

考虑的替代方案：直接复用 `init` 的措辞。这虽熟悉，但它隐藏了打开 workspace 和向 workspace 安装 skill 之间的重要区别。

### 复用现有的工具 ID 模型

CLI 应对非交互式设置和更新使用现有的 `--tools all|none|<ids>` 语法。复用现有工具 ID 避免了为相同的已配置 agent 发明第二个命名系统。

考虑的替代方案：添加 `--agents`。这单独看可读性更好，但它会在 `openspec init --tools` 旁边产生不必要的并行词汇。

### 让配置文件选择 workflow，工具选择 agent

workspace 设置/更新应使用活动的全局配置文件来决定安装哪些 OpenSpec workflow skill。配置文件回答"哪些操作可用？"，而 `--tools` 回答"哪些 agent 获得这些操作？"保持这些关注点分离，保留了现有的配置文件模型，并避免了在此切片中添加 workspace 本地 workflow 选择。

如果全局配置是 `core`，workspace skill 应包括核心 workflow 集。如果全局配置是 `custom`，workspace skill 应仅包括已配置的自定义 workflow。`--tools none` 仍应意味着不安​​装任何 agent skill，无论配置文件如何。

考虑的替代方案：添加 workspace 本地配置文件。对于团队共享的 workspace 默认值，这可能在以后有用，但此切片已存储机器本地 agent 路径，应在全局配置文件行为生效之前避免引入另一个配置权限。

### 尽可能预选首选打开程序

交互式设置应在首选打开程序映射到具备 skill 能力的 agent 时预选它。用户可以接受默认值、添加更多 agent 或取消选择。

考虑的替代方案：仅为首选打开程序安装 skill。这更简单，但打开程序选择意味着"我应该如何打开这个 workspace"，而 skill 选择意味着"哪些 agent 应该理解这里的 OpenSpec"。

### 持久化所选的 workspace skill agent 本地状态

workspace 设置应将所选的有 skill 能力的 agent 存储在 `.openspec-workspace/local.yaml` 中，因为 agent 路径和已安装的工具表面是机器本地的。当用户未传递 `--tools` 或进行新的交互式选择时，workspace 更新应使用该存储的选择。

workspace 设置/更新上的显式 `--tools` 应替换存储的选择。`--tools none` 应存储空选择，并仅移除已知的 OpenSpec 管理 workspace skill 目录。

本地状态还应记录足够的最后应用信息以支持差异检测，例如为每个所选 agent 安装的 workflow ID 以及最后成功同步时的有效全局配置文件/交付。这是诊断状态，不是第二真实源。

考虑的替代方案：通过扫描 `.codex/skills/`、`.claude/skills/` 等目录来推断所选 agent。扫描作为回退方案很有用，但持久化的选择提供了可预测的更新行为，并避免将用户自建的文件视为 OpenSpec 管理的状态。

### 保持非交互式设置向后兼容

`openspec workspace setup --no-interactive` 不应要求 `--tools`。如果省略 `--tools`，设置应创建 workspace 并跳过 skill 安装，保留现有的脚本化 workspace 设置行为。人类和 JSON 输出应说明未安装 workspace skill，以及 `openspec workspace update --tools <ids>` 可以稍后添加它们。

不带 `--tools` 的 `openspec workspace update --no-interactive` 应刷新存储的 workspace skill agent 选择。如果未存储选择，它应在不安装 skill 的情况下完成，并报告清晰的无操作指导，要求传递 `--tools`。

考虑的替代方案：只要 workspace 设置/更新是非交互式的，就要求 `--tools`。这镜像了 repository 本地 init，但会破坏早于 workspace 本地 skill 安装的现有 workspace 设置脚本。

### 仅生成 workspace 本地 skill

workspace 设置/更新应在 workspace 根目录下生成 skill，例如 `.codex/skills/` 或 `.claude/skills/`。在此切片中不应生成斜杠命令，因为某些命令适配器解析到全局位置，而 workspace 设置应保持本地和可预测。

当全局交付为 `commands` 或 `both` 时，workspace 设置/更新仍应仅生成 skill，并报告 workspace 命令生成不在此切片范围内。这保持了配置文件 workflow 选择的有用性，而无需 workspace 设置执行全局或 repository 本地命令写入。

考虑的替代方案：完全镜像 `init`，同时生成 skill 和命令。这有风险，可能会产生意外的全局写入，并使设置边界更难解释。

### 添加 `workspace update` 用于 skill 刷新

`openspec workspace update` 应在设置后刷新、添加或移除 workspace 本地的 OpenSpec skill。从 workspace 内部运行时，它应解析当前 workspace，并支持命名和非交互式形式。

workspace 更新应将活动全局配置文件的 workflow 选择与最后应用的 workspace skill 状态进行比较。如果不同，更新应为所选 agent 仅添加/移除 OpenSpec 管理的 workflow skill 目录。workspace doctor/list/status 表面可以将差异报告为警告，workspace 内部的 `openspec config profile` 无操作应使用相同的差异检查来提供指导。

考虑的替代方案：从 workspace 内部复用 `openspec update`。该命令当前意味着 repository/项目更新，而 workspace 更新需要 workspace 选择、workspace JSON/状态行为和链接 repository 安全规则。

### 使 `config profile` 感知 workspace

`openspec config profile` 应保持为全局配置命令。当它在 repository 本地 OpenSpec 项目内部运行且用户选择应用更改时，它应继续运行 `openspec update`。

当它在 OpenSpec workspace 内部运行且配置文件或交付设置实际更改时，它应提示将更改应用于当前 workspace。如果确认，它应为该 workspace 运行 `openspec workspace update`。如果拒绝，它应解释全局配置已更改，用户可以稍后运行 `openspec workspace update`。

预设快捷方式 `openspec config profile core` 应保持其非交互式特性，不启动应用提示。当从 workspace 内部运行时，它应保存全局配置并打印 workspace 特定的后续指导，提示运行 `openspec workspace update`。当在 repository 本地项目内部运行时，它应保持现有的 repository 本地指导。

在此切片中，自动 workspace 上下文应来自 workspace planning 主目录及其自己的子目录。从链接的 repository 或文件夹内部运行命令应保持该位置的 repository 本地行为，除非用户通过 workspace 命令选项显式选择 workspace。这避免了仅仅因为 repository 注册为 workspace 链接而使 repository 本地命令出现意外。

如果目录同时位于 workspace planning 主目录内部和 repository 本地 OpenSpec 项目内部，最近的主目录应确定应用提示。这避免了当用户有意从 workspace planning 主目录操作时，将 workspace 配置文件更改应用到链接的 repository。

考虑的替代方案：使 `openspec config profile` 更新所有已知的 workspace。在小规模设置中这很方便，但全局配置更改不应在没有显式的每个 workspace 操作的情况下扇出到多个 planning 主目录。

### 在操作前解析 planning 主目录

workflow 命令应在计算路径之前，解析当前变更属于 repository 本地 planning 主目录还是 workspace planning 主目录。解析器应识别 planning 根目录、变更根目录、存在的链接区域以及是否允许实施编辑。链接的 repository 不会仅仅因为它们在某个 workspace 中注册就被隐式视为 workspace planning 主目录；workspace 范围的行为是从 workspace planning 主目录或通过显式 workspace 选择来选择的。

考虑的替代方案：在用到路径的地方添加 workspace 特定的命令分支。这会使 workspace 模型泄漏到每个 workflow 中，并使生成的 skill 更加脆弱。

### 将 workspace 变更存储在 workspace planning 路径中

workspace 变更应位于 workspace planning 路径下，最初为 workspace 根目录下的 `changes/<id>`。创建 workspace 变更应一次性捕获共享意图，并可以记录受影响的区域，但不应在链接的 repository 中创建 repository 本地的 `openspec/changes/<id>` 目录。

考虑的替代方案：在 workspace 变更创建期间，在每个受影响的 repository 中物化一个 repository 本地变更。在 POC 中这很容易推理，但它过早提交，使探索看起来像实施。

### 添加 workspace planning schema

workspace 范围的变更默认应使用内置的 `workspace-planning` schema。这保持了 workflow 动词的熟悉性，同时让 workspace 变更具有适合跨区域 planning 的结构。

初始 artifact 结构：

```text
changes/<id>/
 .openspec.yaml # schema: workspace-planning
 proposal.md # 共享目标和范围
 design.md # 跨区域决策
 tasks.md # 协调任务，可选地按受影响的区域分组
 specs/
 <区域或 repository>/
 <能力>/spec.md
```

第一个 schema 应有意图地保持接近正常的 OpenSpec artifact 结构：proposal、spec、设计和任务。特定区域的需求位于 `specs/` 下，特定区域的工作可以用 `tasks.md` 中的章节表示。此切片不会在这些正常 planning artifact 之外引入另一个区域清单。

考虑的替代方案：不变地复用 `spec-driven`，并使所有 workspace 差异隐含在状态输出中。这隐藏了 workspace planning 需要不同指令来按受影响区域组织需求和任务的事实。

考虑的替代方案：创建单独的 workspace workflow skill 而不是 schema。这会重复 workflow 指导，并使 workspace schema 感觉像不同的产品。

### 在 schema 中支持嵌套的 workspace spec 路径

`workspace-planning` schema 应定义其 spec artifact，使嵌套的 workspace 路径成为一等公民，而不是偶然的。预期的输出 schema 是 `specs/**/*.md`，schema 说明应明确描述 `specs/<区域或 repository>/<能力>/spec.md` 作为区域特定需求的默认约定。

状态和说明输出应保留其发现的具体嵌套路径。假设 `specs/<能力>/spec.md` 的 repository 本地 spec 同步、archive 和验证路径，不应将 workspace 范围的 spec 视为 repository 本地能力 spec，直到后续的显式实施、同步或 archive workflow 选择受影响的区域并定义目标。

### 使用受影响的区域，而非目标或 repository 切片

planning 模型应将所有权或实施边界称为"受影响的区域"。受影响的区域可以从已注册的 workspace 链接名称开始，但语言应留有空间给文件夹、包、服务、应用或文档站点。交付分解仍然是独立的概念，不应被称为区域。

考虑的替代方案：保留"目标"，因为它映射到旧的 POC 标志。该术语是实施优先的，鼓励用户在计划明确之前选择 repository。

### 使状态 JSON 成为 agent 上下文契约

`openspec status --change <id> --json` 应成为机器可读操作上下文的主要来源。它应包括 planning 主目录、变更根目录、具体的 artifact 路径、受影响的区域、下一步和约束，例如当实施在范围内时的允许编辑根。

考虑的替代方案：立即创建一个单独的上下文命令。状态已被生成的 workflow skill 使用，因此首先丰富它给 agent 提供了一个单一的查找位置。

### 保持生成的 skill 路径无关

生成的 workflow skill 应询问 OpenSpec artifact 的存放位置，而不是嵌入 repository 本地路径，例如 `openspec/changes/<name>`。标准 skill schema 应为：

```text
1. 运行 `openspec status --change "<name>" --json`。
2. 使用返回的 planning 主目录、artifact、下一步和操作上下文。
3. 在编写 artifact 之前运行 `openspec instructions <artifact> --change "<name>" --json`。
4. 写入 CLI 返回的解析路径。
```

这使同一 skill 在 repository 本地和 workspace 范围的变更中可用。如果状态/说明输出后来变得过于拥挤，可以在未来的变更中引入单独的上下文命令，而无需更改高级 skill 规则。

考虑的替代方案：立即添加新的 `openspec context` 命令。这以后可能有用，但它在证明丰富的状态/说明不足之前添加了新的表面。

### 保护不受支持的 workspace workflow 操作

全局配置文件可能选择在此切片中尚未实现 workspace 范围行为的 workflow，例如完整的 workspace 应用、验证或 archive。为这些 workflow 生成的本地 skill 应是安全的：它们应检查状态/说明，解释不受支持的 workspace 操作，并避免编辑链接的 repository，除非后来的显式实施 workflow 提供了允许的编辑根。

这使 workspace skill 集与用户的配置文件保持一致，同时防止 repository 本地回退假装实现 workspace 语义。

考虑的替代方案：过滤掉 workspace skill 生成中不受支持的 workflow。这可以避免不受支持的命令，但会使 workspace skill 集与用户的配置安静地产生分歧，并使差异更难解释。

### 从 workspace 根重定向 repository 更新

`openspec update` 应保持为 repository/项目更新命令。当从 OpenSpec workspace planning 主目录运行时，它不应尝试将 workspace 视为 repository 本地项目。它应失败或重定向，并给出清晰的指导，提示运行 `openspec workspace update`。

考虑的替代方案：使 `openspec update` 多态，在 workspace 内执行 workspace 更新。这很方便，但它模糊了此变更试图明确的 repository/项目与 workspace 边界。

### 更新文档、帮助和补全

CLI 帮助、命令注册表/补全和用户文档应包括 `openspec workspace update`、其 `--tools` 行为、全局配置文件关系以及仅 skill workspace 交付规则。

考虑的替代方案：仅在实施后记录。由于配置文件/更新行为容易与 repository 本地更新混淆，因此文档和帮助更新是面向用户功能的一部分。

### 将验收和 UX 审查视为阶段关口

每个阶段应产生用户可测试的 delta，即使大部分工作是内部的。在用户可以通过 CLI 行使命名的行为、检查输出或文件并理解变更内容之前，该阶段不算完成。

每个实施阶段除了自动化测试外，还应包括手动验收。手动验收应行使真实的 CLI 流程，检查生成的文件或输出，并在合同要求时确认链接的 repository 或文件夹保持未触及。

每个阶段还应包括对提示、命令形式、人类输出、JSON 输出、artifact 路径和下一步指导的轻度 UX 审查。审查中发现任何令人困惑的 UX 应在同一阶段修复，或记录为有意的后续事项，然后该阶段才被视为完成。

考虑的替代方案：仅在最终验证阶段保留审查。这会在端到端方面发现问题的较晚，但 workspace planning 主要是 workflow 和面向 agent 的 UX，因此每个阶段需要在行为仍新鲜时进行各自的人工检查。

### 用基于证据的审查减少自我验证偏见

实施应在标记任务完成前定义验收证据。对于每个阶段，实施者应捕获确切的手动命令或交互路径、预期观察和实际观察。一个任务不能仅仅因为实施者认为代码符合设计就算完成。

当可行时，单独的审查者或新的 agent 上下文应仅使用变更 artifact、CLI 输出和观察到的文件系统状态来运行手动验收检查清单和 UX 审查。如果没有单独的审查者，实施者应从干净的临时 workspace 重新运行检查清单，并在变更说明或最终实施摘要中记录证据。

考虑的替代方案：依赖自动化测试加上实施者的最终审查。自动化测试是必要的，但此变更是 workflow 密集型和面向 agent 的，因此独立证据比仅有信心更有用。

## 推迟的方向

早期的产品说明指向比此切片交付的更丰富的 workspace 模型。将该方向保持为后续材料，而不是竞争的当前范围。

- 完整的 workspace 应用应在实施前选择或确认一个工作焦点。第一个工作焦点应是具有允许编辑根的受影响区域；后续工作可以在大型变更需要排序时添加可选的交付阶段。在此模型存在之前，workspace 应用/验证/archive skill 保持受保护。
- workspace 验证和 archive 应等待部分区域完成、最终整体变更完成以及 workspace 范围 spec 如何成为 repository 本地 spec 标准的清晰模型。
- 作用域计划文件最终可能附加在变更、阶段、受影响区域或工作焦点级别。此切片有意使第一个 workspace schema 接近正常的 OpenSpec artifact：proposal、spec、设计和任务。
- 受影响的区域可以从已注册的 workspace 链接名称开始，但未来的流程可以完善或从 planning artifact 中推导它们。该推导应避免重新引入目标优先或 repository 切片语言。
- workflow skill 以后可能将通用 OpenSpec workflow 语义与特定于 agent 的功能（如提问、跟踪待办事项或委派工作）分开。此切片仅使生成的 workflow skill 路径无关。
- OpenSpec 可能需要一个命名的探索性笔记约定，用于在将其提升为 proposal、设计、spec 或任务之前保留未确定的思考。此清理使当前变更文件夹专注于标准 artifact。

## 风险 / 权衡

- skill 生成逻辑可能与 `init/update` 有差异 → 在实际可行时共享相同的 template 生成和工具验证助手。
- 移除未选中的 skill 可能移除用户修改的文件 → 仅按显式 workflow 列表移除已知的 OpenSpec 管理 workflow skill 目录。
- `--tools` 在 workspace UX 中不如 `--agents` 精确 → 保持 `--tools` 以实现 CLI 一致性，但在提示和人类输出中使用"agent"。
- 全局交付可以说 `commands` 而 workspace 更新保持仅 skill → 显式报告此情况，以便用户知道命令生成被推迟，而非静默失效。
- `config profile` 可能从已打开 workspace 内的链接 repository 运行 → 仔细解析当前 planning 主目录并仅应用于该主目录。
- 存储的 workspace skill 状态可能过时或手动编辑 → 将其视为诊断性的机器本地状态，并在更新期间始终从活动全局配置文件协调管理的文件。
- 配置文件选中的 workflow 可能尚未具备完整的 workspace 语义 → 生成的 skill 必须保护不支持的操作并避免 repository 本地回退。
- 现有的生成 skill 仍包含 repository 本地路径假设 → 在 workspace 本地 skill 可以安装后，将其作为后来的 artifact 上下文步骤处理。
- 状态 JSON 可能变得过于宽泛 → 保持字段简洁且以操作为导向，例如 `planningHome`、`artifacts`、`affectedAreas`、`nextSteps` 和 `actionContext`。
- 受影响区域发现可能模糊 → 从显式的已注册 workspace 链接开始，并允许后续精炼，而不是将自由格式的 Markdown 标题解析为唯一的真实源。
- 新 schema 可能与 repository 本地 workflow 期望有差异 → 保持 artifact ID 简洁，让状态/说明携带 schema 特定的路径。
- skill 说明可能落后于 CLI 行为 → 审计源 workflow template 中硬编码的 repository 本地路径，并用路径无关的状态/说明 schema 替换它们。
