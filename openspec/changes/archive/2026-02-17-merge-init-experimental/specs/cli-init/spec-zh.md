## 被修改的需求

### 需求：目录创建

命令应创建带有配置文件的 OpenSpec 目录结构。

#### 场景：创建 OpenSpec 结构

- **当** 执行 `openspec init`
- **则** 创建以下目录结构：
```
openspec/
├── config.yaml
├── specs/
└── changes/
    └── archive/
```

### 需求：AI 工具配置

命令应通过可搜索的多选体验配置 AI 编程助手的技能和斜杠命令。

#### 场景：提示 AI 工具选择

- **当** 以交互方式运行
- **则** 显示带有 OpenSpec 标志的动画欢迎界面
- **且** 呈现一个可搜索的多选列表，显示所有可用工具
- **且** 已配置的工具标记为"（已配置 ✓）"
- **且** 预选已配置的工具，便于刷新
- **且** 已配置的工具排在列表前面
- **且** 允许通过输入进行搜索过滤

#### 场景：选择要配置的工具

- **当** 用户选择工具并确认
- **则** 在 `.<tool>/skills/` 目录中为每个选中的工具生成技能
- **且** 在 `.<tool>/commands/opsx/` 目录中为每个选中的工具生成斜杠命令
- **且** 使用默认 schema 设置创建 `openspec/config.yaml`

### 需求：技能生成

命令应为选中的 AI 工具生成代理技能。

#### 场景：为工具生成技能

- **当** 在初始化期间选中一个工具
- **则** 在 `.<tool>/skills/` 下创建 9 个技能目录：
  - `openspec-explore/SKILL.md`
  - `openspec-new-change/SKILL.md`
  - `openspec-continue-change/SKILL.md`
  - `openspec-apply-change/SKILL.md`
  - `openspec-ff-change/SKILL.md`
  - `openspec-verify-change/SKILL.md`
  - `openspec-sync-specs/SKILL.md`
  - `openspec-archive-change/SKILL.md`
  - `openspec-bulk-archive-change/SKILL.md`
- **且** 每个 SKILL.md 应包含带有名称和描述的 YAML frontmatter
- **且** 每个 SKILL.md 应包含技能指令

### 需求：斜杠命令生成

命令应为选中的 AI 工具生成 opsx 斜杠命令。

#### 场景：为工具生成斜杠命令

- **当** 在初始化期间选中一个工具
- **则** 使用该工具的命令适配器创建 9 个斜杠命令文件：
  - `/opsx:explore`
  - `/opsx:new`
  - `/opsx:continue`
  - `/opsx:apply`
  - `/opsx:ff`
  - `/opsx:verify`
  - `/opsx:sync`
  - `/opsx:archive`
  - `/opsx:bulk-archive`
- **且** 使用工具特定的路径约定（例如 Claude 使用 `.claude/commands/opsx/`）
- **且** 包含工具特定的 frontmatter 格式

### 需求：成功输出

命令应在初始化成功时提供清晰、可操作的后续步骤。

#### 场景：显示成功消息

- **当** 初始化成功完成
- **则** 显示分类摘要：
  - "已创建：<tools>" 用于新配置的工具
  - "已刷新：<tools>" 用于已更新重写的已配置工具
  - 生成的技能和命令数量
- **且** 显示入门部分：
  - `/opsx:new` - 开始新的变更
  - `/opsx:continue` - 创建下一个工件
  - `/opsx:apply` - 实现任务
- **且** 显示文档和反馈的链接

#### 场景：显示重启指示

- **当** 初始化成功完成且工具被创建或刷新
- **则** 显示重启 IDE 以使斜杠命令生效的指示

### 需求：配置文件生成

命令应创建带有 schema 设置的 OpenSpec 配置文件。

#### 场景：创建 config.yaml

- **当** 初始化完成
- **且** config.yaml 不存在
- **则** 使用默认 schema 设置创建 `openspec/config.yaml`
- **且** 在输出中显示配置位置

#### 场景：保留已有的 config.yaml

- **当** 以扩展模式运行初始化
- **且** `openspec/config.yaml` 已存在
- **则** 保留现有的配置文件
- **且** 在输出中显示"（已存在）"指示

### 需求：非交互模式

命令应通过命令行选项支持非交互操作。

#### 场景：非交互式选择所有工具

- **当** 使用 `--tools all` 运行
- **则** 自动选择每个可用的 AI 工具，无需提示
- **且** 继续进行技能和命令生成

#### 场景：非交互式选择特定工具

- **当** 使用 `--tools claude,cursor` 运行
- **则** 解析逗号分隔的工具 ID
- **且** 仅为指定的工具生成技能和命令

#### 场景：非交互式跳过工具配置

- **当** 使用 `--tools none` 运行
- **则** 仅创建 openspec 目录结构和 config.yaml
- **且** 跳过技能和命令生成

### 需求：实验性命令别名

命令应保持与实验性命令的向后兼容性。

#### 场景：运行 openspec experimental

- **当** 用户运行 `openspec experimental`
- **则** 委托给 `openspec init`
- **且** 该命令应在帮助输出中隐藏

## 已移除的需求

### 需求：文件生成

**原因**：不再生成 AGENTS.md 和 project.md。技能包含所有必要的指令。

**迁移**：`.<tool>/skills/` 中的技能提供所有 OpenSpec 工作流指令。无需手动创建文件。

### 需求：AI 工具配置详情

**原因**：配置文件（CLAUDE.md、.cursorrules 等）已被技能替代。

**迁移**：使用 `.<tool>/skills/` 中的技能替代配置文件。技能提供更丰富、工具特定的指令。

### 需求：斜杠命令配置

**原因**：旧的 `/openspec:*` 斜杠命令已被功能更丰富的 `/opsx:*` 命令替代。

**迁移**：使用 `/opsx:new`、`/opsx:continue`、`/opsx:apply` 替代 `/openspec:proposal`、`/openspec:apply`、`/openspec:archive`。

### 需求：根指令存根

**原因**：根 AGENTS.md 存根不再需要。技能提供工具特定的指令。

**迁移**：支持的工具会自动加载技能。无需根存根。
