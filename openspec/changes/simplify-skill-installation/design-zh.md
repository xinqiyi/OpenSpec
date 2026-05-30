## 背景

OpenSpec 目前为每个用户安装 10 个 workflow（skill + 命令），让新用户不知所措。Init 流程会问多个问题（配置文件、交付方式、工具），在用户体验到价值之前就造成了摩擦。

当前架构：
- `src/core/init.ts` - 处理工具选择和 skill/命令生成
- `src/core/config.ts` - 定义带有 `skillsDir` 映射的 `AI_TOOLS`
- `src/core/shared/skill-generation.ts` - 从 template 生成 skill 文件
- `src/core/templates/workflows/*.ts` - 各个 workflow template
- `src/prompts/searchable-multi-select.ts` - 工具选择 UI

全局配置存在于 `~/.config/openspec/config.json`，用于遥测/功能开关。配置文件/delivery 设置将扩展此现有配置。

## 目标 / 非目标

**目标：**
- 让新用户在 1 分钟内达到"顿悟时刻"
- 智能默认 init，带有自动检测和确认（core 配置文件，both 交付方式）
- 从现有目录自动检测已安装的工具
- 引入配置文件系统（core/custom）用于 workflow 选择
- 引入交付配置（skills/commands/both）作为高级用户设置
- 创建新的 `propose` workflow，结合 `new` + `ff`
- 修复工具选择 UX（空格选择，回车确认）
- 保持对现有用户的向后兼容性

**非目标：**
- 移除任何现有的 workflow（所有 workflow 仍可通过自定义配置文件使用）
- 每个项目的配置文件/delivery 设置（仅限用户级别）
- 更改 artifact 结构或 schema 系统
- 修改 skill/命令的格式或编写方式

## 决策

### 1. 扩展现有全局配置

将配置文件/delivery 设置添加到现有的 `~/.config/openspec/config.json`（通过 `src/core/global-config.ts`）。

**理由：** 全局配置已经存在，具有 XDG/APPDATA 跨平台路径处理、schema 演进和合并默认值行为。复用它可以避免第二个配置文件并利用现有基础设施。

**schema 扩展：**
```json
{
 "telemetry": { ... }, // 现有
 "featureFlags": { ... }, // 现有
 "profile": "core", // 新增
 "delivery": "both", // 新增
 "workflows": [...] // 新增（仅限自定义配置文件）
}
```

**考虑的替代方案：**
- 新的 `~/.openspec/config.yaml`：创建第二个配置文件，不同格式，路径混乱
- 项目配置：需要同步机制，用户直接编辑
- 环境变量：不太容易发现，更难持久化

### 2. 两层配置文件系统

```
core（默认）： propose, explore, apply, archive（4 个）
custom： 用户定义的 workflow 子集
```

**理由：** Core 覆盖了基本循环（propose → explore → apply → archive）。Custom 允许用户通过交互式选择器精确选择所需内容。

**配置 UX：**
```
$ openspec config profile

Delivery: [skills] [commands] [both]
 ^^^^^^

Workflows: (空格切换，回车保存)
[x] propose
[x] explore
[x] apply
[x] archive
[ ] new
[ ] ff
...
```

**考虑的替代方案：**
- 三层（core/extended/custom）：Extended 是冗余的——想要所有 workflow 的用户可以在 custom 中选择它们
- 单独的 profile 和 delivery 命令：合并到一个选择器中减少认知负担

### 3. Propose workflow = New + FF 合并

一个 workflow，一键创建变更并生成所有 artifact。

**理由：** 大多数用户希望从想法直接到可实现状态。将 `new`（创建文件夹）和 `ff`（生成 artifact）分开增加了不必要的步骤。想要控制的 power 用户可以通过自定义配置文件使用 `new` + `continue`。

**实现：** `src/core/templates/workflows/propose.ts` 中的新 template：
1. 通过 `openspec new change` 创建变更目录
2. 运行 artifact 生成循环（如同 ff）
3. 在输出中包括入门式解释

### 4. 自动检测并确认

扫描现有的工具目录，预选检测到的工具，要求确认。

**理由：** 在减少问题的同时仍然给用户控制权。比完全自动（无确认）可能安装不需要的工具更好，也比无检测（总是询问）增加摩擦更好。

**检测逻辑：**
```typescript
// 使用现有的 AI_TOOLS 配置获取目录映射
// AI_TOOLS 中的每个工具都有一个 skillsDir 属性（例如 '.claude'、'.cursor'、'.windsurf'）
// 扫描当前工作目录中与 skillsDir 值匹配的现有目录，预选匹配项
const detectedTools = AI_TOOLS.filter(tool =>
 fs.existsSync(path.join(cwd, tool.skillsDir))
);
```

### 5. 交付作为配置文件配置的一部分

交付偏好（skills/commands/both）存储在全局配置中，默认为 "both"。

**理由：** 大多数用户不知道或不关心这个区别。有偏好的高级用户可以通过 `openspec config profile` 交互式选择器设置。不值得在 init 期间询问。

### 6. 文件系统作为已安装 workflow 的事实源

安装在 `.claude/skills/`（等）中的内容是事实源，而不是配置。

**理由：**
- 向后兼容现有安装
- 用户可以手动添加/删除 skill 目录
- 配置文件是"安装什么"的 template，而不是约束

**行为：**
- `openspec init` 设置新项目或重新初始化现有项目（选择工具，生成 workflow）
- `openspec update` 刷新现有项目以匹配当前配置（不进行工具选择）
- `openspec config profile` 仅更新全局配置，如果项目内则提供运行 update 的选项
- 额外的 workflow（不在配置文件中）被保留
- 交付更改被应用：切换到 `skills` 移除命令，切换到 `commands` 移除 skill

**为什么不使用单独的工具清单？**

工具选择（项目使用哪些助手）既是每个用户的也是每个项目的，但两个配置位置要么是仅限用户的（全局配置），要么是项目共享的（检入的项目配置）。曾探索并拒绝了一个单独的清单：

- *路径键控的全局配置*（`projects: { "/path": { tools: [...] } }`）：在目录移动/重命名/删除时脆弱，符号链接歧义，项目行为取决于不可见的外部状态。
- *Git 忽略的本地文件*（`.openspec.local`）：在新克隆时丢失，增加文件管理开销。
- *检入的项目配置*（`openspec/config.yaml` 带有 `tools` 字段）：将工具选择强加给整个团队——Alice 使用 Claude Code，Bob 使用 Cursor，双方都不希望对方的工具被强制使用。

文件系统方法避免了所有三个问题。对于团队来说，实际上是有益的：检入的 skill 文件意味着任何团队成员运行 `openspec update` 都会刷新项目支持的所有工具的 skill。生成的文件既作为交付物，也作为隐式的工具清单。

已知缺陷：将配置存储在项目树之外的工具（没有要扫描的本地目录）需要特定工具的处理，因为项目中没有什么可扫描的。如果支持此类工具，届时再处理。

**何时使用 init vs update：**
- `init`：首次设置，或想要更改配置了哪些工具时
- `update`：更改配置后，或想将 template 刷新到最新版本时

### 8. 现有用户迁移

当 `openspec init` 或 `openspec update` 遇到具有现有 workflow 但全局配置中没有 `profile` 字段的项目时，它执行一次性迁移以保留用户的当前设置。

**理由：** 没有迁移，现有用户将默认为 `core` 配置文件，导致 `propose` 被添加到他们现有的 10 个 workflow 之上——使情况更糟，而不是更好。迁移确保现有用户精确保留他们拥有的内容。

**触发条件：** 同时由 `init`（在现有项目上重新初始化）和 `update` 触发。迁移检查是一个共享函数，在两个命令的早期、配置文件解析之前调用。

**检测逻辑：**
```typescript
// 共享的迁移检查，由 init 和 update 调用：
function migrateIfNeeded(projectPath: string, tools: AiTool[]): void {
 const globalConfig = readGlobalConfig();
 if (globalConfig.profile) return; // 已迁移或已显式设置

 const installedWorkflows = scanInstalledWorkflows(projectPath, tools);
 if (installedWorkflows.length === 0) return; // 新用户，使用 core 默认值

 // 现有用户——迁移到自定义配置文件
 writeGlobalConfig({
 ...globalConfig,
 profile: 'custom',
 delivery: 'both',
 workflows: installedWorkflows,
 });
}
```

**扫描逻辑：**
- 扫描所有工具目录（`.claude/skills/`、`.cursor/skills/` 等）以查找 workflow 目录/文件
- 仅匹配 `ALL_WORKFLOWS` 常量——忽略用户创建的自定义 skill/命令
- 将目录名称映射回 workflow ID（例如 `openspec-explore/` → `explore`、`opsx-explore.md` → `explore`）
- 取跨所有工具的检测到的 workflow 名称的并集

**边界情况：**
- **用户手动删除了一些 workflow：** 迁移扫描实际安装的内容，尊重用户的选择
- **具有不同 workflow 集的多个项目：** 第一个触发迁移的项目设置全局配置；后续项目使用它
- **用户在目录中有自定义（非 OpenSpec）skill：** 被忽略——扫描器仅匹配 `ALL_WORKFLOWS` 中已知的 workflow ID
- **迁移是幂等的：** 如果配置中已设置 `profile`，不会发生重新迁移
- **非交互式（CI）：** 相同的迁移逻辑，不需要确认——它在保留现有状态

**考虑的替代方案：**
- 在 `init` 而非 `update` 期间迁移：Init 已有自己的流程（工具选择等）。将迁移混入 init 会造成混乱的 UX
- 不迁移，仅仅默认为 core：破坏现有用户，添加 `propose` 并显示"额外 workflow"警告
- 在全局配置读取时迁移：过于隐式，难以向用户显示反馈

### 9. template 中的通用下一步指导

workflow template 使用通用的、基于概念的下一步指导，而不是引用特定的 workflow 命令。例如，template 说"创建变更 proposal"而不是"运行 `/opsx:propose`"。

**理由：** 条件性交叉引用（每个 template 检查安装了哪些其他 workflow 并渲染不同的命令名称）给 template 生成、测试和维护增加了显著复杂度。通用指导完全避免了这个问题，同时仍然有用——用户已经知道他们安装了哪些 workflow。

**注意：** 如果发现用户始终难以将概念映射到命令，我们可以重新审视条件性交叉引用。目前，简洁性胜出。

### 7. 修复多选快捷键

从 Tab 键确认改为行业标准的空格/回车。

**理由：** Tab 键确认不符合标准且让用户困惑。大多数 CLI 工具使用空格切换，回车确认。

**实现：** 修改 `src/prompts/searchable-multi-select.ts` 的快捷键配置。

### 10. 更新同步必须考虑配置漂移，而不仅仅是版本漂移

`openspec update` 不能仅依赖 `generatedBy` 版本检查来决定是否需要工作。

**理由：** 配置文件和 delivery 更改可能需要文件添加/移除操作，即使现有的 skill template 是最新的。如果我们只检查 template 版本，update 可能错误地返回"已是最新"并跳过所需的同步。

**实现：**
- 保留版本检查用于 template 刷新决策
- 为配置文件/delivery 添加文件状态漂移检查（缺失预期文件或来自已移除 delivery schema 的过期文件）
- 将版本漂移或配置漂移视为需要更新

### 11. 工具配置检测包括仅命令安装

用于 update 的已配置工具检测必须包括命令文件，而不仅仅是 skill 文件。

**理由：** 使用 `delivery: commands`，一个项目可以在没有 skill 文件的情况下完全配置。仅 skill 检测会错误地报告"未找到已配置的工具。"

**实现：**
- 对于 update 流程，如果某个工具有生成的 skill 或生成的命令，则视其为已配置
- 保持迁移 workflow 扫描行为不变（skill 仍然是迁移的事实源）

### 12. Init 配置文件覆盖被严格验证

`openspec init --profile` 必须在继续之前验证允许的值。

**理由：** 静默接受未知的配置文件值会隐藏用户错误并产生隐式的回退行为。

**实现：** 仅接受 `core` 和 `custom`；对无效值抛出清晰的 CLI 错误。

## 风险 / 权衡

**风险：破坏现有用户的 workflow 程**
→ 缓解措施：文件系统是事实源，现有安装保持不变。所有 workflow 可通过自定义配置文件使用。

**风险：Propose workflow 重复 ff 逻辑**
→ 缓解措施：将共享的 artifact 生成提取为可复用的函数，`propose` 和 `ff` 都调用它。

**风险：全局配置文件管理**
→ 缓解措施：首次使用时创建目录/文件。优雅处理缺失文件（使用默认值）。

**风险：自动检测误报**
→ 缓解措施：显示检测到的工具并要求确认，不静默自动安装。

**权衡：Core 配置文件只有 4 个 workflow**
→ 可接受：这些覆盖了主要循环。需要更多 workflow 的用户可以使用 `openspec config profile` 选择额外的 workflow。

## 迁移计划

1. **第一阶段：添加基础设施**
 - 用配置文件/delivery/workflows 字段扩展 global-config.ts
 - 配置文件定义和解析
 - 工具自动检测

2. **第二阶段：创建 propose workflow**
 - 结合 new + ff 的新 template
 - 带解释性输出的增强 UX

3. **第三阶段：更新 init 流程**
 - 带有工具确认的智能默认值
 - 自动检测并确认工具
 - 尊重配置文件/delivery 设置

4. **第四阶段：添加 config profile 命令**
 - `openspec config profile` 交互式选择器
 - `openspec config profile core` 预设快捷方式

5. **第五阶段：更新 update 命令**
 - 读取全局配置中的配置文件/delivery
 - 从配置文件中添加缺失的 workflow
 - 当 delivery 更改时删除文件（例如，如果为 `skills` 则移除命令）
 - 显示更改摘要

6. **第六阶段：修复多选 UX**
 - 更新 searchable-multi-select 中的快捷键

**回滚：** 所有更改都是 delta 式的。现有行为通过选择所有 workflow 的自定义配置文件得以保留。
