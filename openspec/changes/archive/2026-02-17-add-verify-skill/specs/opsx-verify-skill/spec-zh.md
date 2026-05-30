# opsx-verify-skill spec

## 目的
定义用于验证实现是否与变更 artifact（spec、任务、设计）匹配的 agent skill。

## 新增需求

### 需求：验证 skill 调用
系统应提供 `/opsx:verify` skill，用于验证实现与变更 artifact 的一致性。

#### 场景：提供变更名称时验证
- **WHEN** agent 执行 `/opsx:verify <change-name>`
- **THEN** agent 验证该特定变更的实现
- **AND** 生成验证报告

#### 场景：未提供变更名称时验证
- **WHEN** agent 执行 `/opsx:verify` 而不带变更名称
- **THEN** agent 提示用户从可用变更中选择
- **AND** 仅显示具有实现任务的变更

#### 场景：变更没有任务
- **WHEN** 选定的变更没有 tasks.md 或任务为空
- **THEN** agent 报告 "No tasks to verify"
- **AND** 建议运行 `/opsx:continue` 以创建任务

### 需求：完成度验证
agent 应验证所有必需的工作是否已完成。

#### 场景：任务完成检查
- **WHEN** 验证完成度
- **THEN** agent 读取 tasks.md
- **AND** 统计标记为 `- [x]`（已完成）和 `- [ ]`（未完成）的任务
- **AND** 报告完成状态，列出具体的未完成任务

#### 场景：spec 覆盖检查
- **WHEN** 验证完成度
- **AND** 差异 spec 存在于 `openspec/changes/<name>/specs/` 中
- **THEN** agent 从差异 spec 中提取所有需求
- **AND** 在代码库中搜索每个需求的实现
- **AND** 报告哪些需求似乎已实现，哪些缺失

#### 场景：所有任务完成
- **WHEN** 所有任务标记为完成
- **THEN** 报告 "Tasks: N/N complete"
- **AND** 将完成度维度标记为通过

#### 场景：发现未完成的任务
- **WHEN** 某些任务未完成
- **THEN** 报告 "Tasks: X/N complete"
- **AND** 列出每个未完成的任务
- **AND** 标记为严重问题
- **AND** 建议："Complete remaining tasks or mark as done if already implemented"

### 需求：正确性验证
agent 应验证实现与 spec 匹配。

#### 场景：需求实现映射
- **WHEN** 验证正确性
- **THEN** 对于差异 spec 中的每个需求：
 - 在代码库中搜索实现
 - 识别相关文件和行号
 - 评估实现是否满足需求

#### 场景：场景覆盖检查
- **WHEN** 验证正确性
- **THEN** 对于差异 spec 中的每个场景：
 - 检查场景的条件是否在代码中处理
 - 检查是否存在覆盖该场景的测试
 - 报告覆盖状态

#### 场景：实现与 spec 匹配
- **WHEN** 实现似乎满足需求
- **THEN** 报告哪些文件/行实现了它
- **AND** 将需求标记为已覆盖

#### 场景：实现与 spec 不一致
- **WHEN** 实现存在但不匹配 spec 意图
- **THEN** 将不一致报告为警告
- **AND** 解释差异之处
- **AND** 建议：更新实现或更新 spec 以匹配现实

#### 场景：缺失实现
- **WHEN** 未找到需求的实现
- **THEN** 报告为严重问题
- **AND** 建议："Implement requirement X" 并提供所需内容的指导

### 需求：连贯性验证
agent 应验证实现是否合理并遵循设计决策。

#### 场景：Design.md 遵循检查
- **WHEN** 验证连贯性
- **AND** 变更有 design.md
- **THEN** 从 design.md 提取关键决策
- **AND** 验证实现遵循这些决策
- **AND** 报告任何偏差

#### 场景：没有 design.md
- **WHEN** 验证连贯性
- **AND** 没有 design.md
- **THEN** 跳过设计遵循检查
- **AND** 注明 "No design.md to verify against"

#### 场景：设计决策被遵循
- **WHEN** 实现遵循设计决策
- **THEN** 报告为已确认
- **AND** 引用代码中的证据

#### 场景：设计决策被违反
- **WHEN** 实现与设计决策矛盾
- **THEN** 报告为警告
- **AND** 解释矛盾之处
- **AND** 建议：更新实现或更新 design.md

#### 场景：代码 schema 一致性
- **WHEN** 验证连贯性
- **THEN** 检查新代码是否遵循现有项目 schema
- **AND** 将任何重大偏差标记为建议

### 需求：验证报告格式
agent 应生成结构化的、按优先级排序的报告。

#### 场景：报告摘要
- **WHEN** 验证完成
- **THEN** 显示摘要评分卡：
 ```text
 ## Verification Report: <change-name>

 ### Summary
 | Dimension | Status |
 |--------------|----------|
 | Completeness | X/Y |
 | Correctness | X/Y |
 | Coherence | Followed |
 ```

#### 场景：问题优先级排序
- **WHEN** 发现问题
- **THEN** 按优先级分组并显示：
 1. 严重 - archive 前必须修复（缺失实现、未完成任务）
 2. 警告 - 应该修复（与 spec/设计的差异、缺失测试）
 3. 建议 - 修复更好（schema 不一致、小改进）

#### 场景：可操作的建议
- **WHEN** 报告问题
- **THEN** 包含具体的、可操作的修复建议
- **AND** 在适用时引用相关文件和行号
- **AND** 避免模糊的建议，如"考虑审查"

#### 场景：所有检查通过
- **WHEN** 在所有维度中未发现问题
- **THEN** 显示：
 ```text
 All checks passed. Ready for archive.
 ```

#### 场景：发现严重问题
- **WHEN** 存在严重问题
- **THEN** 显示：
 ```text
 X critical issue(s) found. Fix before archiving.
 ```
- **AND** 不建议运行 archive

#### 场景：仅有警告/建议
- **WHEN** 没有严重问题但存在警告
- **THEN** 显示：
 ```text
 No critical issues. Y warning(s) to consider.
 Ready for archive (with noted improvements).
 ```

### 需求：灵活的 artifact 处理
agent 应优雅地处理具有不同 artifact 完成度的变更。

#### 场景：最小变更（仅任务）
- **WHEN** 变更只有 tasks.md
- **THEN** 仅验证任务完成情况
- **AND** 跳过 spec 和设计检查
- **AND** 注明哪些检查被跳过

#### 场景：有 spec 但无设计的变更
- **WHEN** 变更有 tasks.md 和差异 spec 但没有 design.md
- **THEN** 验证完成度和正确性
- **AND** 跳过设计遵循检查
- **AND** 仍根据项目 schema 检查代码连贯性

#### 场景：完整变更（所有 artifact）
- **WHEN** 变更有 proposal、design、specs 和 tasks
- **THEN** 执行所有验证检查
- **AND** 交叉引用 artifact 以检查一致性
