## 新增需求
### 需求：快速参考放置
AI 指令应以快速参考部分开头，在叙述性指南之前展示所需的文件结构、template 和格式化规则。

#### 场景：在顶部加载 template
- **WHEN** `openspec/AGENTS.md` 被重新生成或更新时
- **THEN** 标题后的第一个实质性部分应提供 `proposal.md`、`tasks.md`、spec 差异和场景格式的可直接复制使用的标题
- **AND** 将每个 template 链接到对应的 workflow 步骤以便深入阅读

### 需求：嵌入式 template 和示例
`openspec/AGENTS.md` 应在 agent 人进行相应编辑的位置包含完整的可复制粘贴 template 和内联示例。

#### 场景：提供文件 template
- **WHEN** 作者进入起草 proposal 和差异的 workflow 指南时
- **THEN** 提供与所需结构（`## Why`、`## ADDED Requirements`、`#### Scenario:` 等）匹配的围栏 Markdown template
- **AND** 每个 template 附带一个简要示例，展示正确的标题使用和场景要点

### 需求：预验证清单
`openspec/AGENTS.md` 应提供一个简洁的预验证清单，在运行 `openspec validate` 之前突出显示常见的格式错误。

#### 场景：突出显示常见的验证失败
- **WHEN** 读者到达验证指南时
- **THEN** 提供一个清单，提醒他们验证需求标题、场景格式和差异部分
- **AND** 至少包含关于 `#### Scenario:` 用法和在场景前添加描述性需求文本的提醒

### 需求：渐进式披露 workflow 指南
文档应将初学者必备内容与高级主题分开，使新手能够专注于核心步骤，同时不失去对高级 workflow 的访问权限。

#### 场景：组织初级和高级部分
- **WHEN** 重新组织 `openspec/AGENTS.md` 时
- **THEN** 将介绍部分限制为最少的步骤（脚手架、起草、验证、请求审查）
- **AND** 将高级主题（多能力变更、archive 细节、工具深入探讨）移至清晰标记的后续部分
- **AND** 提供从快速参考到这些高级部分的锚点链接
