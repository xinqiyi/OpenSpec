## 新增需求

### 需求：Schema which 显示解析结果
CLI 应提供 `openspec schema which <name>` 命令，显示 schema 从何处解析。

#### 场景：schema 从项目解析
- **WHEN** 用户运行 `openspec schema which my-workflow` 且 schema 存在于 `openspec/schemas/my-workflow/`
- **THEN** 系统显示源为"project"
- **AND** 显示 schema 目录的完整路径

#### 场景：schema 从用户目录解析
- **WHEN** 用户运行 `openspec schema which my-workflow` 且 schema 仅存在于用户数据目录中
- **THEN** 系统显示源为"user"
- **AND** 显示包括 XDG 数据目录的完整路径

#### 场景：schema 从包解析
- **WHEN** 用户运行 `openspec schema which spec-driven` 且不存在覆盖
- **THEN** 系统显示源为"package"
- **AND** 显示包的 schemas 目录的完整路径

#### 场景：schema 未找到
- **WHEN** 用户运行 `openspec schema which nonexistent`
- **THEN** 系统显示未找到 schema 的错误
- **AND** 列出可用的 schema
- **AND** 以非零退出码退出

### 需求：Schema which 显示阴影信息
CLI 应指示一个 schema 何时遮蔽了较低优先级级别的另一个 schema。

#### 场景：项目 schema 遮蔽包
- **WHEN** 用户运行 `openspec schema which spec-driven` 且项目和包都有 `spec-driven`
- **THEN** 系统显示项目 schema 处于活跃状态
- **AND** 指示它遮蔽了包版本
- **AND** 显示被遮蔽的包 schema 的路径

#### 场景：无遮蔽
- **WHEN** schema 仅存在于一个位置
- **THEN** 系统不显示遮蔽信息

#### 场景：多重遮蔽
- **WHEN** 项目 schema 同时遮蔽用户和包 schema
- **THEN** 系统按优先级顺序列出所有被遮蔽的位置

### 需求：Schema which 输出 JSON 格式
CLI 应支持 `--json` 标志用于机器可读输出。

#### 场景：基础 JSON 输出
- **WHEN** 用户运行 `openspec schema which spec-driven --json`
- **THEN** 系统输出包含 `name`、`source` 和 `path` 字段的 JSON

#### 场景：带遮蔽的 JSON 输出
- **WHEN** 用户运行 `openspec schema which spec-driven --json` 且 schema 有遮蔽
- **THEN** JSON 包含 `shadows` 数组，每个被遮蔽的 schema 包含 `source` 和 `path`

### 需求：Schema which 支持列表 schema
CLI 应支持列出所有 schema 及其解析源。

#### 场景：列出所有 schema
- **WHEN** 用户运行 `openspec schema which --all`
- **THEN** 系统显示按源分组的所有可用 schema
- **AND** 指示哪些 schema 遮蔽了其他 schema

#### 场景：以 JSON 格式列出
- **WHEN** 用户运行 `openspec schema which --all --json`
- **THEN** 系统输出包含每个 schema 解析信息的 JSON 数组
