# 快速入门

本指南解释在您安装并初始化 OpenSpec 后如何使用它。有关安装说明，请参阅[主 README](../README.md#快速开始)。

## 工作原理

OpenSpec 帮助您和您的 AI 编码助手在编写任何代码之前就构建内容达成一致。

**默认快速路径（core 配置）：**

```text
/opsx:propose ──► /opsx:apply ──► /opsx:sync ──► /opsx:archive
```

**扩展路径（自定义工作流选择）：**

```text
/opsx:new ──► /opsx:ff 或 /opsx:continue ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

默认全局配置是 `core`，包括 `propose`、`explore`、`apply`、`sync` 和 `archive`。您可以通过 `openspec config profile` 然后 `openspec update` 来启用扩展工作流命令。

## OpenSpec 创建的内容

运行 `openspec init` 后，您的项目具有此结构：

```
openspec/
├── specs/              # 唯一真相来源（您系统的行为）
│   └── <领域>/
│       └── spec.md
├── changes/            # 提议的更新（每个变更一个文件夹）
│   └── <变更名称>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/      # Delta specs（正在更改的内容）
│           └── <领域>/
│               └── spec.md
└── config.yaml         # 项目配置（可选）
```

**两个关键目录：**

- **`specs/`** - 唯一真相来源。这些 specs 描述您的系统当前的行为方式。按领域组织（例如 `specs/auth/`、`specs/payments/`）。

- **`changes/`** - 提议的修改。每个变更获得自己的文件夹，包含所有相关产物。当变更完成时，其 specs 合并到主 `specs/` 目录中。

## 理解产物

每个变更文件夹包含指导工作的产物：

| 产物 | 用途 |
|----------|---------|
| `proposal.md` | "为什么"和"什么" - 捕获意图、范围和方法 |
| `specs/` | 显示已添加/已修改/已移除需求的 Delta specs |
| `design.md` | "如何" - 技术方法和架构决策 |
| `tasks.md` | 带复选框的实施检查清单 |

**产物相互构建：**

```
proposal ──► specs ──► design ──► tasks ──► implement
   ▲           ▲          ▲                    │
   └───────────┴──────────┴────────────────────┘
           边学习边更新
```

您始终可以在实施过程中了解更多信息时回过头来改进早期的产物。

## Delta Specs 如何工作

Delta specs 是 OpenSpec 中的关键概念。它们显示相对于您当前 specs 正在更改的内容。

### 格式

Delta specs 使用部分来指示更改的类型：

```markdown
# 身份认证的 Delta

## 已添加的需求

### 需求：双因素身份认证
系统必须在登录时需要第二因素认证。

#### 场景：需要 OTP
- GIVEN 一个已启用 2FA 的用户
- WHEN 用户提交有效凭据
- THEN 显示 OTP 挑战

## 已修改的需求

### 需求：会话超时
系统应在 30 分钟不活动后使会话过期。
（之前：60 分钟）

#### 场景：空闲超时
- GIVEN 一个已认证的会话
- WHEN 30 分钟没有活动
- THEN 会话失效

## 已移除的需求

### 需求：记住我
（已弃用，改用 2FA）
```

### 归档时发生的情况

当您归档变更时：

1. **已添加**的需求被追加到主 spec
2. **已修改**的需求替换现有版本
3. **已移除**的需求从主 spec 中删除

变更文件夹移至 `openspec/changes/archive/` 以供审计历史。

## 示例：您的第一个变更

让我们逐步演示如何为应用程序添加暗色模式。

### 1. 启动变更（默认）

```text
你：/opsx:propose add-dark-mode

AI：已创建 openspec/changes/add-dark-mode/
    ✓ proposal.md — 我们为什么这样做，正在更改什么
    ✓ specs/       — 需求和场景
    ✓ design.md    — 技术方法
    ✓ tasks.md     — 实施检查清单
    准备实施！
```

如果您已启用扩展工作流配置，您也可以分两步完成：`/opsx:new` 然后 `/opsx:ff`（或逐步使用 `/opsx:continue`）。

### 2. 创建的内容

**proposal.md** - 捕获意图：

```markdown
# 提案：添加暗色模式

## 意图
用户要求添加暗色模式选项，以减少夜间使用时的眼睛疲劳。

## 范围
- 在设置中添加主题切换开关
- 支持系统偏好检测
- 在 localStorage 中持久化偏好

## 方法
使用 CSS 自定义属性进行主题化，使用 React Context
进行状态管理。
```

**specs/ui/spec.md** - 显示新需求的 Delta：

```markdown
# UI 的 Delta

## 已添加的需求

### 需求：主题选择
系统应允许用户在亮色和暗色主题之间选择。

#### 场景：手动切换
- GIVEN 一个在任何页面上的用户
- WHEN 用户点击主题切换开关
- THEN 主题立即切换
- AND 偏好跨会话持久化

#### 场景：系统偏好
- GIVEN 一个没有保存偏好的用户
- WHEN 应用程序加载
- THEN 使用系统的首选配色方案
```

**tasks.md** - 实施检查清单：

```markdown
# 任务

## 1. 主题基础设施
- [ ] 1.1 创建具有亮/暗状态的 ThemeContext
- [ ] 1.2 添加颜色相关的 CSS 自定义属性
- [ ] 1.3 实现 localStorage 持久化

## 2. UI 组件
- [ ] 2.1 创建 ThemeToggle 组件
- [ ] 2.2 将切换开关添加到设置页面
- [ ] 2.3 更新 Header 以包含快速切换

## 3. 样式
- [ ] 3.1 定义暗色主题调色板
- [ ] 3.2 更新组件以使用 CSS 变量
```

### 3. 实施

```
你：/opsx:apply

AI：正在逐项完成任务...
    ✓ 1.1 创建了具有亮/暗状态的 ThemeContext
    ✓ 1.2 在 globals.css 中添加了 CSS 自定义属性
    ✓ 1.3 实现了 localStorage 持久化
    ✓ 2.1 创建了 ThemeToggle 组件
    ...
    所有任务完成！
```

在实施过程中，如果您发现设计需要调整，只需更新产物并继续。

### 4. 归档

```
你：/opsx:archive

AI：正在归档 add-dark-mode...
    ✓ 已将 specs 合并到 openspec/specs/ui/spec.md
    ✓ 已移至 openspec/changes/archive/2025-01-24-add-dark-mode/
    完成！准备下一个功能。
```

您的 delta specs 现在已成为主 specs 的一部分，记录了您的系统如何工作。

## 验证和审查

使用 CLI 检查您的变更：

```bash
# 列出活跃变更
openspec list

# 查看变更详情
openspec show add-dark-mode

# 验证 spec 格式
openspec validate add-dark-mode

# 交互式仪表板
openspec view
```

## 下一步

- [工作流](workflows.md) - 常见模式及何时使用每个命令
- [命令](commands.md) - 所有斜杠命令的完整参考
- [概念](concepts.md) - 更深入地理解 specs、变更和 schema
- [自定义](customization.md) - 让 OpenSpec 按您的方式工作
