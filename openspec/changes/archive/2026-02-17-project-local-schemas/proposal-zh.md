# 项目本地模式

## 摘要

在模式查找链中增加项目本地模式解析（`./openspec/schemas/`）作为最高优先级。这使得团队能够将自定义工作流模式与其代码仓库一起进行版本控制。

## 动机

目前，模式解析分为两级：
1. 用户覆盖：`~/.local/share/openspec/schemas/<name>/`
2. 包内置：`<npm-package>/schemas/<name>/`

这给团队带来了不便：
- 自定义模式必须通过 XDG 路径在每台机器上设置
- 无法通过版本控制共享模式
- 团队工作流缺乏单一的权威来源

## 设计决策

### 三级解析顺序

```
1. ./openspec/schemas/<name>/                    # 项目本地（新增）
2. ~/.local/share/openspec/schemas/<name>/       # 用户全局（XDG）
3. <npm-package>/schemas/<name>/                 # 包内置
```

项目本地具有最高优先级，实现：
- 版本控制的自定义工作流
- 通过 git 自动团队共享
- 无需每台机器单独设置

### 分支模型（非继承）

自定义模式是完整的定义，而非扩展。不支持 `extends` 关键字。

**理由：** 简单性。继承增加了复杂性（冲突解决、部分覆盖、调试"这是从哪里来的？"）。需要自定义工作流的用户可以完整定义。这保持了简单的思维模型：
- 使用预设 → 配置路径（参见项目配置变更）
- 需要不同结构 → 分支路径（自行定义）

### 目录结构

```
openspec/
├── schemas/                      # 项目本地模式
│   └── my-workflow/
│       ├── schema.yaml           # 完整模式定义
│       └── templates/
│           ├── artifact1.md
│           ├── artifact2.md
│           └── ...
└── changes/
```

### 模式命名

项目本地模式通过其目录名称引用：
- `openspec/schemas/my-workflow/` → 引用为 `my-workflow`
- 适用于 `--schema my-workflow` 标志
- 适用于 config.yaml 中的 `schema: my-workflow`（参见项目配置变更）

## 范围

### 范围内

- 向解析器添加 `getProjectSchemasDir()` 函数
- 更新 `getSchemaDir()` 以优先检查项目本地
- 更新 `listSchemas()` 以包含项目模式
- 更新 `listSchemasWithInfo()` 以包含 `source: 'project'`
- 更新 `schemasCommand` 输出以显示项目模式

### 范围外

- 模式管理 CLI（`openspec schema copy/which/diff/reset`）- 未来增强
- 模式继承/extends - 明确不支持
- 模板级覆盖（部分分支）- 明确不支持

## 用户体验

### 创建自定义模式

```bash
# 创建模式目录
mkdir -p openspec/schemas/my-workflow/templates

# 定义模式
cat > openspec/schemas/my-workflow/schema.yaml << 'EOF'
name: my-workflow
version: 1
description: 我们团队的规划工作流

artifacts:
  - id: research
    generates: research.md
    template: research.md
    description: 背景研究
    requires: []

  - id: proposal
    generates: proposal.md
    template: proposal.md
    description: 变更提案
    requires: [research]

  - id: tasks
    generates: tasks.md
    template: tasks.md
    description: 实施任务
    requires: [proposal]
EOF

# 创建模板
echo "# 研究\n\n..." > openspec/schemas/my-workflow/templates/research.md
# ... 等等
```

### 使用自定义模式

```bash
# 通过 CLI 标志
openspec new change add-feature --schema my-workflow
openspec status --change add-feature --schema my-workflow

# 通过 config.yaml（需要项目配置变更）
# schema: my-workflow
```

### 团队共享

```bash
# 提交到仓库
git add openspec/schemas/
git commit -m "添加自定义工作流模式"
git push

# 团队成员自动获取
git pull
openspec status --change add-feature --schema my-workflow  # 直接可用
```

## 实施说明

### 需要修改的文件

| 文件 | 变更 |
|------|---------|
| `src/core/artifact-graph/resolver.ts` | 添加 `getProjectSchemasDir()`，更新解析顺序 |
| `src/commands/artifact-workflow.ts` | 更新 `schemasCommand` 以显示来源 |

### 项目根检测

使用现有的 `findProjectRoot()` 模式或当前工作目录。项目本地模式目录始终是相对于项目根的 `./openspec/schemas/`。

### 来源指示

`listSchemasWithInfo()` 返回 `source: 'project' | 'user' | 'package'`。更新类型定义和实现。

## 测试考虑

- 创建包含本地模式的临时项目，验证解析优先级
- 验证本地模式覆盖同名的用户覆盖
- 验证 `listSchemas()` 包含项目模式
- 验证 `schemasCommand` 显示正确的来源标签

## 相关变更

- **项目配置**：添加包含 `schema` 字段的 `config.yaml`，可引用项目本地模式
