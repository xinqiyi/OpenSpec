# docs-agent-instructions spec

## 目的
定义生成的 agent 指令文档的编写标准，使 template、示例和验证检查清单清晰且可直接复制使用。

## 需求
### 需求：快速参考放置
AI 指令应以快速参考部分开头，在任何叙述性指导之前展示所需的文件结构、template 和格式化规则。

#### 场景：在顶部加载 template
- **WHEN** `openspec/AGENTS.md` 被重新生成或更新时
- **THEN** 标题后的第一个实质性部分应提供 `proposal.md`、`tasks.md`、spec delta 和场景格式化的可直接复制标题
- **AND** 将每个 template 链接到对应的 workflow 步骤以供深入阅读

### 需求：嵌入的 template 和示例
`openspec/AGENTS.md` 应包括完整的复制/粘贴 template 和内联示例，位置正好在 agent 进行相应编辑的地方。

#### 场景：提供文件 template
- **WHEN** 作者阅读到起草 proposal 和 delta 的 workflow 指导时
- **THEN** 提供与所需结构匹配的围栏 Markdown template（`## Why`、`## 新增需求`、`#### Scenario:` 等）
- **AND** 每个 template 附带一个简短的示例，显示正确的标题用法和场景要点

### 需求：预验证检查清单
`openspec/AGENTS.md` 应提供一个简洁的预验证检查清单，在运行 `openspec validate` 之前突出常见的格式化错误。

#### 场景：突出常见的验证失败
- **WHEN** 读者阅读到验证指导时
- **THEN** 提供检查清单，提醒他们验证需求标题、场景格式化和 delta 部分
- **AND** 包括至少关于 `#### Scenario:` 用法和在场景之前添加描述性需求文本的提醒

### 需求：workflow 指导的渐进式披露
文档应将初学者必备内容与高级主题分开，使新手能够专注于核心步骤，同时不失去对高级 workflow 的访问。

#### 场景：组织初学者和高级部分
- **WHEN** 重新组织 `openspec/AGENTS.md` 时
- **THEN** 将介绍部分限制在最小步骤（搭建、起草、验证、请求审查）
- **AND** 将高级主题（多能力变更、archive 细节、工具深入探讨）移至清晰标记的后续部分
- **AND** 从快速参考提供指向这些高级部分的锚链接

### 需求：行为优先的 spec 编写指导
Agent 指令文档应明确教授 spec 捕获可观察的行为契约，而实现细节属于设计/任务。

#### 场景：区分 spec 与实现内容
- **WHEN** `openspec/AGENTS.md` 解释如何编写 `spec.md`
- **THEN** 应指导 agent 包含外部可验证的行为、输入/输出、错误和约束
- **AND** 应指导 agent 避免在 spec 中包含内部库/框架选择和类/函数级别的实现细节

#### 场景：将细节路由到正确的 artifact
- **WHEN** 需要实现细节时
- **THEN** 指令应将 agent 引导至将其放在 `design.md` 或 `tasks.md` 中，而不是放在 `spec.md` 的行为需求部分

### 需求：默认轻量级指导
Agent 指令文档应推广最小仪式和适度的严谨性用于 spec 编写。

#### 场景：应用渐进式严谨性
- **WHEN** agent 为常规变更起草 spec 时
- **THEN** 指令应倾向于简洁、轻量级的需求和场景
- **AND** 将更深入、更全面的 spec 风格保留给更高风险的变更（如 API 破坏、迁移、跨团队或安全/隐私敏感的工作）

#### 场景：时间到清晰度优化
- **WHEN** 指导讨论起草 workflow 时
- **THEN** 应强调生成仍然可测试和可审查的最小 spec
