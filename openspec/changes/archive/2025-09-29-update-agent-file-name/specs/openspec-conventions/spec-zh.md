## 修改后的需求

### 需求：项目结构
OpenSpec 项目应为 spec 和变更维护一致的目录结构。

#### 场景：初始化项目结构
- **WHEN** OpenSpec 项目被初始化时
- **THEN** 其应具有以下结构：
```
openspec/
├── project.md # 项目特定上下文
├── AGENTS.md # AI 助手指令
├── specs/ # 当前已部署的能力
│ └── [capability]/ # 单一、聚焦的能力
│ ├── spec.md # 做什么和为什么
│ └── design.md # 如何做（可选，适用于已建立的 schema）
└── changes/ # 提议的变更
 ├── [change-name]/ # 描述性变更标识符
 │ ├── proposal.md # 原因、内容和影响
 │ ├── tasks.md # 实施检查清单
 │ ├── design.md # 技术决策（可选）
 │ └── specs/ # 完整的未来状态
 │ └── [capability]/
 │ └── spec.md # 干净的 Markdown（无差异语法）
 └── archive/ # 已完成的变更
 └── YYYY-MM-DD-[name]/
```
