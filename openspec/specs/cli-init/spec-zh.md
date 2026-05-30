# CLI Init spec

## 目的

`openspec init` 命令应在任何项目中创建完整的 OpenSpec 目录结构，支持立即采用 OpenSpec 约定，并兼容多种 AI 编码助手。

## 需求
### 需求：进度指示器

该命令应在初始化过程中显示进度指示器，为每个步骤提供清晰的反馈。

#### 场景：显示初始化进度

- **WHEN** 执行初始化步骤时
- **THEN** 在后台静默验证环境（无输出，除非出错）
- **AND** 使用 ora 旋转器显示进度：
 - 显示旋转器："正在创建 OpenSpec 结构..."
 - 然后成功："已创建 OpenSpec 结构"
 - 显示旋转器："正在配置 AI 工具..."
 - 然后成功："已配置 AI 工具"

### 需求：目录创建

该命令应创建包含配置文件的 OpenSpec 目录结构。

#### 场景：创建 OpenSpec 结构

- **WHEN** 执行 `openspec init` 时
- **THEN** 创建以下目录结构：
```
openspec/
├── config.yaml
├── specs/
└── changes/
 └── archive/
```

### 需求：AI 工具配置

该命令应使用可搜索的多选体验来配置 AI 编码助手的 skill 和斜杠命令。

#### 场景：提示 AI 工具选择

- **WHEN** 以交互 schema 运行时
- **THEN** 显示带有 OpenSpec 标志的动画欢迎页面
- **AND** 呈现一个可搜索的多选列表，显示所有可用工具
- **AND** 已配置的工具标记为"（已配置 ✓）"指示器
- **AND** 预选已配置的工具以便轻松刷新
- **AND** 将已配置的工具排序到列表顶部
- **AND** 允许通过输入进行搜索过滤

#### 场景：选择要配置的工具

- **WHEN** 用户选择工具并确认时
- **THEN** 为每个选中的工具在 `.<tool>/skills/` 目录中生成 skill
- **AND** 为每个选中的工具在 `.<tool>/commands/opsx/` 目录中生成斜杠命令
- **AND** 创建带有默认架构设置的 `openspec/config.yaml`

### 需求：交互 schema
该命令应提供带有清晰导航说明的 AI 工具选择交互菜单。

#### 场景：显示交互菜单
- **WHEN** 在全新或扩展 schema 下运行时
- **THEN** 呈现一个循环选择菜单，让用户通过空格切换工具，通过回车确认选择
- **AND** 当在已高亮但未选中的可选中工具上按下回车时，自动将其添加到选择中，然后再进入审查，以便高亮显示的工具被配置
- **AND** 将已配置的工具标记为"（已配置）"，同时将禁用的选项标记为"即将推出"
- **AND** 在扩展 schema 下将提示文案改为"您想要添加或刷新哪些 AI 工具？"
- **AND** 显示内联说明，说明空格切换工具，回车在选择工具后进入审查界面

### 需求：安全检查
该命令应执行安全检查，以防止覆盖现有结构并确保适当的权限。

#### 场景：检测已有初始化
- **WHEN** `openspec/` 目录已存在时
- **THEN** 通知用户 OpenSpec 已初始化，跳过重新创建基础结构，并进入扩展 schema
- **AND** 继续到 AI 工具选择步骤，以便可以配置额外的工具
- **AND** 仅在用户拒绝添加任何 AI 工具时显示已初始化的错误消息

### 需求：成功输出

该命令应在成功初始化后提供清晰、可操作的后续步骤。

#### 场景：显示成功消息

- **WHEN** 初始化成功完成时
- **THEN** 显示分类摘要：
 - "已创建：<工具>"用于新配置的工具
 - "已刷新：<工具>"用于已更新配置的工具
 - 生成的 skill 和命令数量
- **AND** 显示入门部分，包括：
 - `/opsx:new` - 开始新的变更
 - `/opsx:continue` - 创建下一个 artifact
 - `/opsx:apply` - 实施任务
- **AND** 显示文档和反馈的链接

#### 场景：显示重启提示

- **WHEN** 初始化成功完成并且工具已创建或刷新时
- **THEN** 显示提示，要求重启 IDE 以使斜杠命令生效

### 需求：退出码

该命令应使用一致的退出码来指示不同的失败 schema。

#### 场景：返回退出码

- **WHEN** 命令完成时
- **THEN** 返回适当的退出码：
 - 0：成功
 - 1：一般错误（包括 OpenSpec 目录已存在的情况）
 - 2：权限不足（保留供将来使用）
 - 3：用户取消操作（保留供将来使用）

### 需求：额外 AI 工具初始化
`openspec init` 应允许用户在初始设置后为新的 AI 编码助手添加配置文件。

#### 场景：初始设置后配置额外工具
- **GIVEN** `openspec/` 目录已存在且至少有一个 AI 工具文件存在
- **WHEN** 用户运行 `openspec init` 并选择不同的受支持 AI 工具时
- **THEN** 以与首次初始化相同的方式生成该工具的配置文件，并包含 OpenSpec 标记
- **AND** 保留现有工具配置文件不变，除需要刷新的托管部分外
- **AND** 以代码 0 退出，并显示成功摘要，突出显示新添加的工具文件

### 需求：成功输出增强
`openspec init` 应在初始化或扩展 schema 完成时总结工具操作。

#### 场景：显示工具摘要
- **WHEN** 命令成功完成时
- **THEN** 显示已创建、已刷新或已跳过（包括已配置的跳过）工具的分类摘要
- **AND** 使用选定工具的名称个性化"下一步"标题，当没有剩余工具时默认为通用标签

### 需求：退出码调整
`openspec init` 应将没有新原生工具选择的扩展 schema 视为成功的刷新。

#### 场景：允许空的扩展运行
- **WHEN** OpenSpec 已初始化且用户未选择额外的原生支持工具时
- **THEN** 成功完成，无需额外工具设置
- **AND** 保留现有的 OpenSpec 结构和配置文件
- **AND** 以代码 0 退出

### 需求：非交互 schema

该命令应通过命令行选项支持非交互式操作。

#### 场景：非交互式选择所有工具

- **WHEN** 使用 `--tools all` 运行时
- **THEN** 自动选择每个可用的 AI 工具，无需提示
- **AND** 继续进行 skill 和命令生成

#### 场景：非交互式选择特定工具

- **WHEN** 使用 `--tools claude,cursor` 运行时
- **THEN** 解析逗号分隔的工具 ID
- **AND** 仅为指定的工具生成 skill 和命令

#### 场景：非交互式跳过工具配置

- **WHEN** 使用 `--tools none` 运行时
- **THEN** 仅创建 openspec 目录结构
- **AND** 跳过 skill 和命令生成
- **AND** 仅在满足配置创建条件时创建配置

#### 场景：无效的工具指定

- **WHEN** 使用 `--tools invalid-tool` 运行时
- **THEN** 以退出码 1 失败
- **AND** 显示列出可用值（`all`、`none` 和受支持的工具 ID）的错误信息

#### 场景：保留值与工具 ID 组合

- **WHEN** 使用 `--tools all,claude` 或 `--tools none,cursor` 运行时
- **THEN** 以退出码 1 失败
- **AND** 显示错误，说明保留值不能与特定工具 ID 组合

#### 场景：非交互 schema 下缺少 --tools

- **GIVEN** 非交互执行中提示不可用
- **WHEN** 用户运行 `openspec init` 而不带 `--tools` 时
- **THEN** 以退出码 1 失败
- **AND** 提示使用 `--tools all`、`--tools none` 或显式工具 ID

### 需求：skill 生成

该命令应为选定的 AI 工具生成 Agent skill。

#### 场景：为工具生成 skill

- **WHEN** 在初始化期间选择了工具时
- **THEN** 在 `.<tool>/skills/` 下创建 9 个 skill 目录：
 - `openspec-explore/SKILL.md`
 - `openspec-new-change/SKILL.md`
 - `openspec-continue-change/SKILL.md`
 - `openspec-apply-change/SKILL.md`
 - `openspec-ff-change/SKILL.md`
 - `openspec-verify-change/SKILL.md`
 - `openspec-sync-specs/SKILL.md`
 - `openspec-archive-change/SKILL.md`
 - `openspec-bulk-archive-change/SKILL.md`
- **AND** 每个 SKILL.md 应包含带有名称和描述的 YAML frontmatter
- **AND** 每个 SKILL.md 应包含 skill 指令

### 需求：斜杠命令生成

该命令仅应为已注册命令适配器的选定工具生成 opsx 斜杠命令，同时使无适配器的工具仍可用于 skill 生成。

#### 场景：为具有已注册适配器的工具生成斜杠命令

- **WHEN** 在初始化期间选择了具有已注册命令适配器的工具时
- **THEN** 使用该工具的命令适配器创建 9 个斜杠命令文件：
 - `/opsx:explore`
 - `/opsx:new`
 - `/opsx:continue`
 - `/opsx:apply`
 - `/opsx:ff`
 - `/opsx:verify`
 - `/opsx:sync`
 - `/opsx:archive`
 - `/opsx:bulk-archive`
- **AND** 使用工具特定的路径约定（例如，Claude 使用 `.claude/commands/opsx/`）
- **AND** 包含工具特定的 frontmatter 格式

#### 场景：选定的工具没有命令适配器

- **GIVEN** 选定的工具已配置 `skillsDir` 但没有已注册的命令适配器
- **WHEN** 初始化包含命令生成时
- **THEN** 该工具的 skill 生成仍然有效
- **AND** 该工具的命令文件生成将被跳过
- **AND** 命令输出应包含 `已跳过 <tool-id> 的命令（无适配器）`

#### 场景：Kimi CLI 跳过命令文件生成

- **WHEN** 用户在初始化期间选择 Kimi CLI 时
- **THEN**OpenSpec 将其视为具有 `skillsDir: '.kimi'` 的受支持工具
- **AND** 由于没有已注册的 Kimi 适配器，跳过命令文件生成

### 需求：配置文件生成

该命令应创建带有架构设置的 OpenSpec 配置文件。

#### 场景：创建 config.yaml

- **WHEN** 初始化完成时
- **AND**config.yaml 不存在
- **THEN** 创建带有默认架构设置的 `openspec/config.yaml`
- **AND** 在输出中显示配置位置

#### 场景：保留现有 config.yaml

- **WHEN** 在扩展 schema 下运行初始化时
- **AND** `openspec/config.yaml` 已存在
- **THEN** 保留现有的配置文件
- **AND** 在输出中显示"（已存在）"指示器

### 需求：实验性命令别名

该命令应保持与实验性命令的向后兼容性。

#### 场景：运行 openspec experimental

- **WHEN** 用户运行 `openspec experimental` 时
- **THEN** 委托给 `openspec init`
- **AND** 该命令应从帮助输出中隐藏

## 原因

手动创建 OpenSpec 结构容易出错，并会产生采用摩擦。标准化的 init 命令确保：
- 所有项目结构一致
- 始终包含正确的 AI 指令文件
- 新项目快速上手
- 从一开始就有清晰的约定
