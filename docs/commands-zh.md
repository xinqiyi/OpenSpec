# 命令

这是 OpenSpec 斜杠命令的参考。这些命令在您的 AI 编码助手的聊天界面中调用（例如 Claude Code、Cursor、Windsurf）。

有关工作流模式及何时使用每个命令，请参阅[工作流](workflows.md)。有关 CLI 命令，请参阅[CLI](cli.md)。

## 快速参考

### 默认快速路径（`core` 配置）

| 命令 | 用途 |
|---------|---------|
| `/opsx:propose` | 一步创建变更并生成规划产物 |
| `/opsx:explore` | 在提交变更之前思考想法 |
| `/opsx:apply` | 根据变更实施任务 |
| `/opsx:sync` | 将 delta specs 合并到主 specs |
| `/opsx:archive` | 归档已完成的变更 |

### 扩展工作流命令（自定义工作流选择）

| 命令 | 用途 |
|---------|---------|
| `/opsx:new` | 启动新的变更 scaffold |
| `/opsx:continue` | 根据依赖关系创建下一个产物 |
| `/opsx:ff` | 快进：一次性创建所有规划产物 |
| `/opsx:verify` | 验证实施是否匹配产物 |
| `/opsx:bulk-archive` | 一次归档多个变更 |
| `/opsx:onboard` | 引导式教程，贯穿完整工作流 |

默认全局配置是 `core`。要启用扩展工作流命令，运行 `openspec config profile`，选择工作流，然后在项目中运行 `openspec update`。

---

## 命令参考

### `/opsx:propose`

创建新变更并一步生成规划产物。这是 `core` 配置中的默认启动命令。

**语法：**
```text
/opsx:propose [变更名称或描述]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称或描述` | 否 | Kebab-case 名称或通俗语言的变更描述 |

**作用：**
- 创建 `openspec/changes/<变更名称>/`
- 生成实施前所需的产物（对于 `spec-driven`：proposal、specs、design、tasks）
- 在变更准备好供 `/opsx:apply` 时停止

**示例：**
```text
你：/opsx:propose add-dark-mode

AI：已创建 openspec/changes/add-dark-mode/
    ✓ proposal.md
    ✓ specs/ui/spec.md
    ✓ design.md
    ✓ tasks.md
    准备实施。运行 /opsx:apply。
```

**提示：**
- 这是最快的端到端路径
- 如果您想要逐步控制产物，启用扩展工作流并使用 `/opsx:new` + `/opsx:continue`

---

### `/opsx:explore`

在提交变更之前思考想法、调查问题、明确需求。

**语法：**
```
/opsx:explore [主题]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `主题` | 否 | 您想探索或调查的内容 |

**作用：**
- 开启探索性对话，无需结构化要求
- 调查代码库以回答问题
- 比较选项和方法
- 创建可视化图表以澄清思路
- 当思路明确时，可以过渡到 `/opsx:propose`（默认）或 `/opsx:new`（扩展工作流）

**示例：**
```text
你：/opsx:explore

AI：您想探索什么？

你：我们应该如何处理移动应用的身份认证？

AI：让我调查您当前的认证设置...
    [分析代码库]

    我看到您对 Web 应用使用基于会话的认证。
    对于移动端，我们有三个主要选项：

    1. JWT 令牌（无状态，可离线工作）
    2. OAuth2（如果您需要第三方登录）
    3. 扩展现有会话（更简单，但需要网络连接）

    您的 API 已经配置了 CORS。您对哪个方向感兴趣？

你：我们选择 JWT。可以为此创建一个变更吗？

AI：准备好了就开始。运行 /opsx:propose add-jwt-auth 开始。
```

**提示：**
- 在需求不明确或需要调查时使用
- 探索期间不创建产物
- 适合在决定前比较多种方法
- 可以读取文件和搜索代码库

---

### `/opsx:new`

启动新的变更 scaffold。创建变更文件夹并等待您使用 `/opsx:continue` 或 `/opsx:ff` 生成产物。

此命令属于扩展工作流集（不包含在默认的 `core` 配置中）。

**语法：**
```
/opsx:new [变更名称] [--schema <schema名称>]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 变更文件夹的名称（未提供时提示） |
| `--schema` | 否 | 要使用的工作流 schema（默认：来自配置或 `spec-driven`） |

**作用：**
- 创建 `openspec/changes/<变更名称>/` 目录
- 在变更文件夹中创建 `.openspec.yaml` 元数据文件
- 显示准备创建的第一个产物模板
- 如果未提供，提示输入变更名称和 schema

**创建的内容：**
```
openspec/changes/<变更名称>/
└── .openspec.yaml    # 变更元数据（schema、创建日期）
```

**示例：**
```
你：/opsx:new add-dark-mode

AI：已创建 openspec/changes/add-dark-mode/
    Schema：spec-driven

    准备创建：proposal
    使用 /opsx:continue 创建它，或使用 /opsx:ff 创建所有产物。
```

**提示：**
- 使用描述性名称：`add-feature`、`fix-bug`、`refactor-module`
- 避免通用名称，如 `update`、`changes`、`wip`
- Schema 也可以在项目配置中设置（`openspec/config.yaml`）

---

### `/opsx:continue`

创建依赖链中的下一个产物。一次创建一个产物，逐步推进。

**语法：**
```
/opsx:continue [变更名称]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 要继续的变更（未提供时从上下文推断） |

**作用：**
- 查询产物依赖关系图
- 显示哪些产物已就绪或被阻塞
- 创建第一个就绪的产物
- 读取依赖文件以获取上下文
- 显示创建后变得可用的内容

**示例：**
```
你：/opsx:continue

AI：变更：add-dark-mode

    产物状态：
    ✓ proposal    (完成)
    ◆ specs       (就绪)
    ◆ design      (就绪)
    ○ tasks       (被阻塞 - 需要：specs)

    正在创建 specs...

    [读取 proposal.md，根据需求创建 specs]

    ✓ 已创建 openspec/changes/add-dark-mode/specs/ui/spec.md

    现在可用：tasks
    运行 /opsx:continue 创建下一个产物。
```

**提示：**
- 当您想在继续前审查每个产物时使用
- 适合想要掌控的复杂变更
- 多个产物可能同时变为就绪状态
- 您可以在继续之前编辑已创建的产物

---

### `/opsx:ff`

快进产物创建。一次性创建所有规划产物。

**语法：**
```
/opsx:ff [变更名称]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 要快进的变更（未提供时从上下文推断） |

**作用：**
- 按依赖顺序创建所有产物
- 通过待办事项列表跟踪进度
- 当所有 `apply-required` 产物完成时停止
- 在创建下一个产物之前读取每个依赖

**示例：**
```
你：/opsx:ff add-dark-mode

AI：正在快进 add-dark-mode...

    ✓ 创建 proposal.md
    ✓ 创建 specs/ui/spec.md
    ✓ 创建 design.md
    ✓ 创建 tasks.md

    所有规划产物完成！
    准备实施。运行 /opsx:apply 开始。
```

**提示：**
- 当您清楚要构建什么时使用
- 对于直接了当的变更，比 `/opsx:continue` 更快
- 事后仍可编辑产物
- 适合中小型功能

---

### `/opsx:apply`

根据变更实施任务。逐项完成任务列表，编写代码并勾选项目。

**语法：**
```
/opsx:apply [变更名称]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 要实施的变更（未提供时从上下文推断） |

**作用：**
- 读取 `tasks.md` 并识别未完成的任务
- 逐个完成任务
- 根据需要编写代码、创建文件、运行测试
- 使用复选框 `[x]` 标记任务完成

**示例：**
```
你：/opsx:apply

AI：正在实施 add-dark-mode...

    读取 tasks.md：
    - [ ] 1.1 创建 ThemeContext
    - [ ] 1.2 添加 CSS 自定义属性
    - [ ] 1.3 实现 localStorage 持久化

    正在处理 1.1：创建 ThemeContext...
    [创建 src/context/ThemeContext.tsx]

    ✓ 1.1 完成

    正在处理 1.2：添加 CSS 自定义属性...
    [更新 src/styles/globals.css]

    ✓ 1.2 完成
    ...
```

**提示：**
- 如果中断，可以从上次暂停的地方继续
- 通过指定变更名称用于并行变更
- 完成状态在 `tasks.md` 复选框中跟踪

---

### `/opsx:verify`

验证实施是否与变更产物匹配。检查完整性、正确性和一致性。

**语法：**
```
/opsx:verify [变更名称]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 要验证的变更（未提供时从上下文推断） |

**作用：**
- 检查实施质量的三个维度
- 搜索代码库寻找实施证据
- 将问题分类为严重、警告或建议
- 不会阻止归档，但会暴露问题

**验证维度：**

| 维度 | 验证内容 |
|-----------|-------------------|
| **完整性** | 所有任务完成，所有需求已实施，场景已覆盖 |
| **正确性** | 实施符合 spec 意图，边界情况已处理 |
| **一致性** | 设计决策已反映在代码中，模式一致 |

**示例：**
```
你：/opsx:verify

AI：正在验证 add-dark-mode...

     完整性
     ✓ tasks.md 中的所有 8 项任务均已检查
     ✓ specs 中的所有需求都有对应代码
     ⚠ 场景"系统偏好检测"没有测试覆盖

     正确性
     ✓ 实施符合 spec 意图
     ✓ 已处理场景中的边界情况
     ✓ 错误状态符合 spec 定义

     一致性
     ✓ 设计决策已反映在代码结构中
     ✓ 命名约定与 design.md 一致
     ⚠ 设计提到"CSS 变量"但实施使用了 Tailwind 类

     摘要
     ─────────────────────────────
     严重问题：0
     警告：2
     可归档：是（带有警告）

     建议：
     1. 为系统偏好检测添加测试
     2. 更新 design.md 以反映 Tailwind 的使用，或重构使用 CSS 变量
```

**提示：**
- 在归档前运行，及早发现不匹配
- 警告不会阻止归档，但指示潜在问题
- 适合在提交前审查 AI 的工作
- 可以揭示产物与实施之间的偏差

---

### `/opsx:sync`

**可选命令。** 将变更的 delta specs 合并到主 specs。归档会在需要时提示同步，因此您通常不需要手动运行此命令。

**语法：**
```
/opsx:sync [变更名称]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 要同步的变更（未提供时从上下文推断） |

**作用：**
- 从变更文件夹读取 delta specs
- 解析 ADDED/MODIFIED/REMOVED/RENAMED 部分
- 将更改合并到主 `openspec/specs/` 目录
- 保留 delta 中未提及的现有内容
- 不会归档变更（保持活跃）

**示例：**
```text
你：/opsx:sync

AI：正在同步 add-dark-mode delta specs...

    读取：openspec/changes/add-dark-mode/specs/ui/spec.md
    目标：openspec/specs/ui/spec.md

    要应用的更改：
    ✓ 已添加：主题选择需求（2 个场景）
    ✓ 已添加：可访问性需求（1 个场景）

    正在合并...
    ✓ openspec/specs/ui/spec.md 已更新

    变更保持活跃。准备完成时运行 /opsx:archive。
```

**何时手动使用：**

| 场景 | 使用 sync？|
|----------|-----------|
| 长期运行的变更，希望在归档前将 specs 纳入主目录 | 是 |
| 多个并行变更需要更新后的基础 specs | 是 |
| 想要预览/审查单独的合并 | 是 |
| 快速变更，直接归档 | 否（归档会处理） |

**提示：**
- Sync 是智能的，不是简单复制粘贴
- 可以向现有需求添加场景而无需重复
- 变更在同步后保持活跃（未归档）
- 大多数用户永远不需要直接调用此命令——归档会在需要时提示

---

### `/opsx:archive`

归档已完成的变更。最终确定变更并将其移至归档文件夹。

**语法：**
```
/opsx:archive [变更名称]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 要归档的变更（未提供时从上下文推断） |

**作用：**
- 检查产物完成状态
- 检查任务完成情况（未完成时警告）
- 如果 delta specs 尚未同步，提供同步选项
- 将变更文件夹移至 `openspec/changes/archive/YYYY-MM-DD-<名称>/`
- 保留所有产物以供审计追踪

**示例：**
```text
你：/opsx:archive

AI：正在归档 add-dark-mode...

    产物状态：
    ✓ proposal.md 存在
    ✓ specs/ 存在
    ✓ design.md 存在
    ✓ tasks.md 存在（8/8 任务完成）

    Delta specs：尚未同步
    → 现在同步？（推荐）

你：是

AI：✓ 已将 specs 同步到 openspec/specs/ui/spec.md
    ✓ 已移至 openspec/changes/archive/2025-01-24-add-dark-mode/

    变更已成功归档。
```

**提示：**
- 归档不会阻止不完整的任务，但会给出警告
- Delta specs 可以在归档期间或提前同步
- 已归档的变更保留在历史记录中
- 先使用 `/opsx:verify` 来发现潜在问题

---

### `/opsx:bulk-archive`

一次归档多个已完成的变更。处理变更之间的 spec 冲突。

**语法：**
```
/opsx:bulk-archive [变更名称...]
```

**参数：**
| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `变更名称` | 否 | 要归档的特定变更（未提供时提示选择） |

**作用：**
- 列出所有已完成的变更
- 在归档前验证每个变更
- 检测跨变更的 spec 冲突
- 通过检查实际实施情况解决冲突
- 按时间顺序归档

**示例：**
```
你：/opsx:bulk-archive

AI：发现 3 个已完成的变更：
    - add-dark-mode（8/8 任务完成）
    - fix-login-bug（3/3 任务完成）
    - update-footer（2/2 任务完成）

    正在检查 spec 冲突...
    ⚠ add-dark-mode 和 update-footer 都涉及 specs/ui/

    正在检查代码库以解决冲突...
    两项变更均已实施。将按时间顺序合并：
    1. add-dark-mode（创建于 1 月 20 日）
    2. update-footer（创建于 1 月 22 日）

    归档所有 3 个变更？

你：是

AI：✓ 已归档 add-dark-mode
    ✓ 已归档 fix-login-bug
    ✓ 已归档 update-footer
    Specs 已合并：add-dark-mode → update-footer
```

**提示：**
- 适合并行工作流
- 冲突解决是智能的（检查代码库）
- 变更按创建顺序归档
- 覆盖 spec 内容前会提示

---

### `/opsx:onboard`

引导式入职，贯穿完整的 OpenSpec 工作流。使用您实际代码库的交互式教程。

**语法：**
```
/opsx:onboard
```

**作用：**
- 带解说的完整工作流周期演示
- 扫描您的代码库寻找真实的改进机会
- 创建具有真实产物的实际变更
- 实施实际工作（小型、安全的变更）
- 归档已完成的变更
- 每个步骤进行中解释

**阶段：**
1. 欢迎和代码库分析
2. 寻找改进机会
3. 创建变更（`/opsx:new`）
4. 编写 proposal
5. 创建 specs
6. 编写 design
7. 创建 tasks
8. 实施任务（`/opsx:apply`）
9. 验证实施
10. 归档变更
11. 总结和后续步骤

**示例：**
```
你：/opsx:onboard

AI：欢迎使用 OpenSpec！

    我将使用您的实际代码库演示完整工作流。
    我们会找到一些可以改进的小地方，为其创建合适的变更，
    实施它，然后归档。

    让我扫描您的代码库寻找机会...

    [分析代码库]

    我找到了一些可以处理的内容：
    1. 为联系表单添加输入验证
    2. 改进认证流程中的错误消息
    3. 为异步按钮添加加载状态

    您对哪个感兴趣？（或提出其他建议）
```

**提示：**
- 最适合学习工作流的新用户
- 使用真实代码，而非玩具示例
- 创建您可以保留或丢弃的真实变更
- 大约需要 15-30 分钟完成

---

## 各 AI 工具的命令语法

不同的 AI 工具使用略有不同的命令语法。使用与您的工具匹配的格式：

| 工具 | 语法示例 |
|------|----------------|
| Claude Code | `/opsx:propose`、`/opsx:apply` |
| Cursor | `/opsx-propose`、`/opsx-apply` |
| Windsurf | `/opsx-propose`、`/opsx-apply` |
| Copilot (IDE) | `/opsx-propose`、`/opsx-apply` |
| Kimi CLI | 基于 Skill 的调用，如 `/skill:openspec-propose`、`/skill:openspec-apply-change`（不生成 `opsx-*` 命令文件） |
| Trae | 基于 Skill 的调用，如 `/openspec-propose`、`/openspec-apply-change`（不生成 `opsx-*` 命令文件） |

不同工具的意图相同，但命令的呈现方式可能因集成而异。

> **注意：** GitHub Copilot 命令（`.github/prompts/*.prompt.md`）仅在 IDE 扩展中可用（VS Code、JetBrains、Visual Studio）。GitHub Copilot CLI 目前不支持自定义提示文件——有关详细信息和变通方法，请参阅[支持的工具](supported-tools.md)。

---

## 旧版命令

这些命令使用较旧的"一次性全部"工作流。它们仍然有效，但推荐使用 OPSX 命令。

| 命令 | 作用 |
|---------|--------------|
| `/openspec:proposal` | 一次性创建所有产物（proposal、specs、design、tasks） |
| `/openspec:apply` | 实施变更 |
| `/openspec:archive` | 归档变更 |

**何时使用旧版命令：**
- 使用旧工作流的现有项目
- 不需要增量产物创建的简单变更
- 偏好全有或全无的方法

**迁移到 OPSX：**
旧版变更可以使用 OPSX 命令继续。产物结构是兼容的。

---

## 故障排除

### "未找到变更"

命令无法识别要处理哪个变更。

**解决方案：**
- 显式指定变更名称：`/opsx:apply add-dark-mode`
- 检查变更文件夹是否存在：`openspec list`
- 确认您在正确的项目目录中

### "没有就绪的产物"

所有产物要么已完成，要么因缺少依赖而被阻塞。

**解决方案：**
- 运行 `openspec status --change <名称>` 查看阻塞原因
- 检查所需的产物是否存在
- 先创建缺少的依赖产物

### "未找到 Schema"

指定的 schema 不存在。

**解决方案：**
- 列出可用 schema：`openspec schemas`
- 检查 schema 名称的拼写
- 如果是自定义 schema，创建它：`openspec schema init <名称>`

### 命令不被识别

AI 工具不识别 OpenSpec 命令。

**解决方案：**
- 确保 OpenSpec 已初始化：`openspec init`
- 重新生成 skills：`openspec update`
- 检查 `.claude/skills/` 目录是否存在（对于 Claude Code）
- 重新启动您的 AI 工具以加载新的 skills

### 产物生成不正确

AI 创建不完整或不正确的产物。

**解决方案：**
- 在 `openspec/config.yaml` 中添加项目上下文
- 为特定指导添加按产物规则
- 在变更描述中提供更多细节
- 使用 `/opsx:continue` 而非 `/opsx:ff` 以获得更多控制

---

## 下一步

- [工作流](workflows.md) - 常见模式及何时使用每个命令
- [CLI](cli.md) - 用于管理和验证的终端命令
- [自定义](customization.md) - 创建自定义 schema 和工作流
