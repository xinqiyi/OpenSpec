## 新增的需求

### 需求：OPSX Onboard skill

系统应提供一个 `/opsx:onboard` skill，通过解说和真实代码库工作，引导用户完成他们的第一个完整 OpenSpec workflow 周期。

#### 场景：skill 调用

- **WHEN** 用户调用 `/opsx:onboard`
- **THEN** agent 检查 OpenSpec 是否已初始化
- **AND** 如果未初始化，提示用户先运行 `openspec init`
- **AND** 如果已初始化，继续执行入门流程

#### 场景：欢迎和预期

- **WHEN** 入门开始时
- **THEN** agent 显示欢迎消息，解释将要发生什么
- **AND** 设置约 15 分钟的时长预期
- **AND** 解释 workflow 阶段：探索 → 新建 → artifact → 应用 → archive

### 需求：用于任务建议的代码分析

skill 应分析用户的代码库，以建议范围适中的入门级任务。

#### 场景：代码扫描

- **WHEN** 入门到达任务选择阶段
- **THEN** agent 扫描代码库寻找小的改进机会
- **AND** 查找：TODO/FIXME 注释、缺失的错误处理、缺少测试的函数、过时的依赖、TypeScript 中的 type: any、生产代码中的 console.log、缺失的输入验证
- **AND** 检查最近的 git 提交以了解当前工作的上下文

#### 场景：任务建议展示

- **WHEN** agent 已分析代码库
- **THEN** agent 展示 3-4 个具体的任务建议，附带范围估算
- **AND** 每个建议包括：任务描述、估算范围（文件/行数）、为何是好的入门任务
- **AND** 提供让用户自行指定任务的选项

#### 场景：范围防护

- **WHEN** 用户选择或描述的任务过大
- **THEN** agent 温和地引导其转向较小的范围
- **AND** 建议拆分或推迟大任务
- **AND** 提供大小合适的替代方案

### 需求：探索阶段演示

skill 应在创建变更前简要演示探索 schema。

#### 场景：简要探索演示

- **WHEN** 任务已选择
- **THEN** agent 通过调查相关代码简要演示 `/opsx:explore`
- **AND** 解释探索 schema 是在行动之前的思考
- **AND** 保持此阶段简短（不是完整的探索会议）
- **AND** 过渡到变更创建

### 需求：引导式 artifact 创建

skill 应通过解说引导用户创建每个 artifact，解释其用途。

#### 场景：带解说的变更创建

- **WHEN** 创建变更目录时
- **THEN** agent 运行 `openspec new change "<name>"`，使用推导的 kebab-case 名称
- **AND** 解释什么是"变更"（思考和 planning 的容器）
- **AND** 显示已创建的文件夹结构
- **AND** 在继续前暂停等待用户确认

#### 场景：带解说的 proposal 创建

- **WHEN** 创建 proposal.md 时
- **THEN** agent 解释 proposal 记录我们为什么要做这个变更
- **AND** 基于选定的任务起草 proposal
- **AND** 在保存前向用户展示草稿以获批准
- **AND** 解释各部分（Why, What Changes, Capabilities, Impact）

#### 场景：带解说的 spec 创建

- **WHEN** 创建 spec 文件时
- **THEN** agent 解释 spec 详细定义我们要构建什么
- **AND** 解释需求/场景格式
- **AND** 基于 proposal 的能力创建 spec 文件
- **AND** 说明 spec 会成为保持同步的文档

#### 场景：带解说的设计创建

- **WHEN** 创建 design.md 时
- **THEN** agent 解释设计记录我们将如何构建
- **AND** 说明这是技术决策和权衡所在的地方
- **AND** 对于小的变更，承认设计可能很简短
- **AND** 基于 proposal 和 spec 创建设计

#### 场景：带解说的任务创建

- **WHEN** 创建 tasks.md 时
- **THEN** agent 解释任务将工作拆分为复选框
- **AND** 解释这些驱动 apply 阶段
- **AND** 从设计和 spec 生成任务列表
- **AND** 显示任务并询问是否准备好实现

### 需求：引导式实现

skill 应在实现任务时添加解说，将工作连接回 artifact。

#### 场景：带解说的实现

- **WHEN** 实现任务时
- **THEN** agent 在开始处理每个任务前宣布它
- **AND** 在代码库中实现变更
- **AND** 偶尔提及 spec/设计如何影响决策
- **AND** 完成每个任务时标记为完成
- **AND** 保持解说轻量（不过度解释）

#### 场景：实现完成

- **WHEN** 所有任务完成时
- **THEN** agent 宣布完成
- **AND** 总结完成了什么
- **AND** 过渡到 archive 阶段

### 需求：带解释的 archive

skill 应 archive 完成的变更并解释发生了什么。

#### 场景：带解说的 archive

- **WHEN** archive 变更时
- **THEN** agent 解释 archive 将变更移动到带日期的文件夹
- **AND** 运行 archive 过程
- **AND** 显示 archive 变更存放的位置
- **AND** 解释长期价值（以后查找决策）

### 需求：回顾和后续步骤

skill 应以回顾和命令参考结束。

#### 场景：最终回顾

- **WHEN** 入门完成时
- **THEN** agent 总结已完成的 workflow 阶段
- **AND** 强调这个节奏适用于任何规模的变更
- **AND** 提供命令参考表（/opsx:explore, /opsx:new, /opsx:ff, /opsx:continue, /opsx:apply, /opsx:verify, /opsx:archive）
- **AND** 建议下一步操作（尝试 /opsx:new 或 /opsx:ff）

### 需求：优雅退出处理

skill 应处理中途想要停止的用户。

#### 场景：用户想停止

- **WHEN** 用户在入门过程中表示想停止
- **THEN** agent 优雅地确认
- **AND** 说明进行中的变更已保存
- **AND** 解释以后如何通过 `/opsx:continue <name>` 继续
- **AND** 无压力退出

#### 场景：用户只想要快速参考

- **WHEN** 用户说只想查看命令
- **THEN** agent 提供命令速查表
- **AND** 优雅退出，鼓励尝试 `/opsx:new`
