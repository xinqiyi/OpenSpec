## 修改后的需求

### 需求：目录创建
命令应创建完整的 OpenSpec 目录结构，包含所有必需的目录和文件。

#### 场景：创建 OpenSpec 结构
- **WHEN** 执行 `openspec init`
- **THEN** 创建以下目录结构：
```
openspec/
├── project.md
├── AGENTS.md
├── specs/
└── changes/
 └── archive/
```

### 需求：文件生成
命令应生成带有适当内容的所需 template 文件，以便立即使用。

#### 场景：生成 template 文件
- **WHEN** 初始化 OpenSpec
- **THEN** 生成包含供 AI 助手使用的完整 OpenSpec 指令的 `AGENTS.md`
- **AND** 生成带有项目上下文 template 的 `project.md`

### 需求：AI 工具配置详情

命令应使用标记系统为选定的 AI 工具正确配置 OpenSpec 特定指令。

#### 场景：创建新的 CLAUDE.md
- **WHEN** CLAUDE.md 不存在
- **THEN** 创建包含包裹在标记中的 OpenSpec 内容的新文件，并引用 `@openspec/AGENTS.md`

### 需求：成功输出

命令应在成功初始化时提供清晰、可操作的下一步指导。

#### 场景：显示成功消息
- **WHEN** 初始化成功完成
- **THEN** 包含提示："请解释来自 openspec/AGENTS.md 的 OpenSpec workflow 以及我应如何在此项目中与您协作"
