## 修改的需求

### 需求：AIToolOption 的 skillsDir 字段
`AIToolOption` 接口除路径元数据外还应包含作用域支持元数据。

#### 场景：存在作用域支持元数据
- **WHEN** `AI_TOOLS` 中定义了工具条目时
- **THEN** 它可以声明支持的 skills 和 commands 安装作用域
- **AND** 此元数据应用于有效作用域解析

#### 场景：缺少作用域支持元数据
- **WHEN** `AI_TOOLS` 中的工具条目对某个表面省略了作用域支持元数据时
- **THEN** 解析器行为应默认该表面仅支持项目作用域
- **AND** 有效作用域解析应针对该默认值应用正常的首选/回退规则

### 需求：支持的工具的路径配置
路径元数据应通过解析器逻辑同时支持项目和全局安装目标。

#### 场景：项目作用域路径
- **WHEN** skills 的有效作用域为 `project` 时
- **THEN** `skillsDir` 应被视为项目根目录下特定于工具的容器路径
- **AND** 托管的 skill 制品应写入 `<projectRoot>/<skillsDir>/skills/`
- **AND** 工具定义应相应设置 `skillsDir`（例如 `.openspec` -> `.openspec/skills/`）

#### 场景：全局作用域路径
- **WHEN** 支持的工具/表面的有效作用域为 `global` 时
- **THEN** 路径应解析为特定于工具的全局目录
- **AND** 在适用时应尊重环境变量覆盖（例如 `CODEX_HOME`）

#### 场景：Codex 命令的 Windows 全局路径解析
- **WHEN** 有效作用域为 `global`
- **AND** 工具为 Codex
- **AND** 平台为 Windows
- **THEN** 当设置了 `CODEX_HOME` 时，命令目标应解析为 `%CODEX_HOME%\prompts`
- **AND** 否则应解析为 `%USERPROFILE%\.codex\prompts`
