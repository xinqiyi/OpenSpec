## 目的

propose 工作流应将变更创建和制品生成合并到单个命令中，减少新用户的摩擦，同时通过嵌入式指导向他们教授 OpenSpec 工作流。

## 新增需求

### 需求：Propose 工作流创建
系统应提供一个 `propose` 工作流，一步创建变更并生成所有制品。

#### 场景：基本的 propose 调用
- **当** 用户调用 `/opsx:propose "add user authentication"`
- **则** 系统应使用 kebab-case 名称创建变更目录
- **则** 系统应在变更目录中创建 `.openspec.yaml`（通过 `openspec new change`）
- **则** 系统应生成实施所需的所有制品：proposal.md、design.md、specs/、tasks.md

#### 场景：使用已存在的变更名称调用 Propose
- **当** 用户调用 `/opsx:propose` 时使用已存在的名称
- **则** 系统应询问用户是继续现有变更还是创建新变更
- **则** 如果"继续"：系统应从最后一个完成的状态恢复制品生成
- **则** 如果"创建新"：系统应提示输入新名称
- **则** 在非交互模式下：系统应失败并显示错误，建议使用不同的名称

### 需求：Propose 工作流入门 UX
`propose` 工作流应包含解释性输出，帮助新用户理解流程。

#### 场景：首次用户指导
- **当** 用户调用 `/opsx:propose`
- **则** 系统应解释将创建的制品（proposal.md、design.md、specs/、tasks.md）
- **则** 系统应指示下一步（`/opsx:apply` 实施）

#### 场景：制品创建进度
- **当** 系统创建每个制品时
- **则** 系统应显示进度（例如，"✓ 已创建 proposal.md"）

### 需求：Propose 工作流结合 new 和 ff
`propose` 工作流应执行与运行 `new` 后跟 `ff` 相同的操作。

#### 场景：等同于 new + ff
- **当** 用户调用 `/opsx:propose "feature name"`
- **则** 结果应在功能上等同于调用 `/opsx:new "feature-name"` 后跟 `/opsx:ff feature-name`
- **则** 应创建相同的目录结构和制品
- **则** 控制台输出可能不同（propose 包含入门解释）
