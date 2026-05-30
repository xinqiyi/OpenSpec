## 为什么

用户抱怨 skill/命令太多（目前 10 个），新用户感到不知所措。我们希望在保留高级用户能力和向后兼容性的同时简化默认体验。

目标：**让用户在 1 分钟内达到"顿悟时刻"**。

```text
0:00 $ openspec init
 ✓ 完成。运行 /opsx:propose "你的想法"

0:15 /opsx:propose "添加用户认证"

0:45 agent 创建 proposal.md、design.md、tasks.md
 "哇，它帮我计划了整件事" ← 顿悟

1:00 /opsx:apply
```

此外，用户对 workflow 的交付方式有不同的偏好（skill vs 命令 vs 两者兼有），但这应该是高级用户的配置，而不是新用户需要考虑的事情。

## 变更内容

### 1. 智能默认 Init

Init 自动检测工具并要求确认：

```text
$ openspec init

检测到的工具：
 [x] Claude Code
 [x] Cursor
 [ ] Windsurf

按 Enter 确认，或按 Space 切换

正在设置 OpenSpec...
✓ 完成

开始你的第一个变更：
 /opsx:propose "添加暗色 schema"
```

**没有配置文件或 delivery 的提示。** 默认值为：
- 配置文件：core
- 交付方式：both

高级用户可以通过 `openspec config profile` 自定义。

### 2. 工具检测行为

Init 扫描现有的工具目录（`.claude/`、`.cursor/` 等）：
- **检测到工具（交互式）：** 显示预选复选框，用户确认或调整
- **未检测到工具（交互式）：** 提示进行完整的工具选择
- **非交互式（CI）：** 自动使用检测到的工具，如果未检测到则失败

### 3. 修复工具选择 UX

当前行为让用户困惑：
- Tab 键确认（不符合预期）

新行为：
- **空格键** 切换选择
- **回车键** 确认

### 4. 引入配置文件

配置文件定义要安装的 workflow：

- **core**（默认）：`propose`、`explore`、`apply`、`archive`（4 个 workflow）
- **custom**：用户选择的 workflow 子集

`propose` workflow 是新的——它结合了 `new` + `ff` 成为一个命令，创建变更并生成所有 artifact。

### 5. 改进的 Propose UX

`/opsx:propose` 应通过解释正在执行的操作来自然地引导用户：

```text
我将创建一个包含 3 个 artifact 的变更：
- proposal.md（什么和为什么）
- design.md（如何）
- tasks.md（实现步骤）

准备实施时，运行 /opsx:apply
```

它边做边教——大多数用户不需要单独的入门引导。

### 6. 引入交付配置

交付控制 workflow 的安装方式：

- **both**（默认）：skill 和命令
- **skills**：仅 skill
- **commands**：仅命令

存储在现有的全局配置中（`~/.config/openspec/config.json`）。init 期间不提示。

### 7. 新的 CLI 命令

```shell
# 配置文件配置（交付 + workflow 的交互式选择器）
openspec config profile # 交互式选择器
openspec config profile core # 预设快捷方式（core workflow，保留 delivery）
```

交互式选择器允许用户在一个界面中配置交付方式和 workflow 选择：

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
[ ] continue
[ ] verify
[ ] sync
[ ] bulk-archive
[ ] onboard
```

### 8. 向后兼容性与迁移

**现有用户保留他们的当前设置。** 当 `openspec update` 在具有现有 workflow 且全局配置中没有 `profile` 的项目上运行时，它会执行一次性迁移：

1. 扫描项目中所有工具目录中已安装的 workflow 文件
2. 将 `profile: "custom"`、`delivery: "both"`、`workflows: [<检测到的>]` 写入全局配置
3. 刷新 template，但不添加或移除任何 workflow
4. 显示："已迁移：包含 N 个现有 workflow 的自定义配置文件"

迁移后，后续的 `init` 和 `update` 命令将尊重已迁移的配置。

**关键行为：**
- 现有用户的 workflow 完全按原样保留（不会自动添加 `propose`）
- 如果未设置配置文件，`init`（重新初始化）和 `update` 都会在现有项目上触发迁移
- 在**新**项目（无现有 workflow）上运行 `openspec init` 时使用全局配置，默认为 `core`
- 使用自定义配置文件的 `init` 直接应用已配置的 workflow（无配置文件确认提示）
- `init` 验证 `--profile` 值（`core` 或 `custom`），对无效输入报错
- 迁移消息提及 `propose` 并建议运行 `openspec config profile core` 以选择加入
- 迁移后，用户可以通过 `openspec config profile core` 选择加入 `core` 配置文件
- workflow template 在"后续步骤"指导中仅条件性引用已安装的 workflow
- 交付更改会被应用：切换到 `skills` 移除命令文件，切换到 `commands` 移除 skill 文件
- 重新运行 `init` 会在现有项目上应用 delivery 清理（移除不再匹配 delivery 的文件）
- 即使 template 版本已经是最新的，`update` 也将配置文件/delivery 漂移视为需要更新
- `update` 将仅命令安装视为已配置的工具
- 所有 workflow 仍可通过自定义配置文件使用

## 能力

### 新能力

- `profiles`：workflow 配置文件（core、custom）、交付偏好、全局配置存储、交互式选择器
- `propose-workflow`：创建变更 + 生成所有 artifact 的组合 workflow

### 修改的能力

- `cli-init`：带有工具自动检测、基于配置文件/配置文件的 skill/命令生成的智能默认值
- `cli-update`：配置文件支持、交付更改、现有用户的一次性迁移

## 影响

### 新文件
- `src/core/templates/workflows/propose.ts` - 新的 propose workflow template
- `src/core/profiles.ts` - 配置文件定义和逻辑
- `src/core/available-tools.ts` - 从目录检测用户拥有哪些 AI 工具

### 修改的文件
- `src/core/init.ts` - 智能默认值、自动检测、工具确认
- `src/core/config.ts` - 添加配置文件（profile）和交付（delivery）类型
- `src/core/global-config.ts` - 向 schema 添加配置文件、交付、workflow 字段
- `src/core/shared/skill-generation.ts` - 按配置文件筛选，尊重 delivery
- `src/core/shared/tool-detection.ts` - 更新 SKILL_NAMES 和 COMMAND_IDS 以包含 propose
- `src/commands/config.ts` - 添加带有交互式选择器的 `profile` 子命令
- `src/core/update.ts` - 添加配置文件/delivery 支持，delivery 更改的文件删除
- `src/prompts/searchable-multi-select.ts` - 修复快捷键（空格/回车）

### 全局配置 schema 扩展
```json
// ~/.config/openspec/config.json（扩展现有）
{
 "telemetry": { ... }, // 现有
 "featureFlags": { ... }, // 现有
 "profile": "core", // 新增：core | custom
 "delivery": "both", // 新增：both | skills | commands
 "workflows": ["propose", ...] // 新增：仅当 profile: custom 时
}
```

## 配置文件参考

| 配置文件 | workflow | 描述 |
|---------|--------|------|
| core | propose, explore, apply, archive | 面向大多数用户的精简流程（默认） |
| custom | 用户定义 | 通过 `openspec config profile` 精确选择你需要的内容 |
