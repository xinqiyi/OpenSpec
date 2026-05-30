# schema-which-command 规范

## 目的
定义 `openspec schema which` 的行为，用于报告已解析的模式源、位置和回退详情。

## 需求
### 需求：Schema which 显示解析结果
CLI 应提供 `openspec schema which <name>` 命令，显示模式从何处解析。

#### 场景：模式从项目解析
- **当** 用户运行 `openspec schema which my-workflow` 且模式存在于 `openspec/schemas/my-workflow/`
- **那么** 系统显示源为"project"
- **并且** 显示模式目录的完整路径

#### 场景：模式从用户目录解析
- **当** 用户运行 `openspec schema which my-workflow` 且模式仅存在于用户数据目录中
- **那么** 系统显示源为"user"
- **并且** 显示包括 XDG 数据目录的完整路径

#### 场景：模式从包解析
- **当** 用户运行 `openspec schema which spec-driven` 且不存在覆盖
- **那么** 系统显示源为"package"
- **并且** 显示包的 schemas 目录的完整路径

#### 场景：模式未找到
- **当** 用户运行 `openspec schema which nonexistent`
- **那么** 系统显示未找到模式的错误
- **并且** 列出可用的模式
- **并且** 以非零退出码退出

### 需求：Schema which 显示阴影信息
CLI 应指示一个模式何时遮蔽了较低优先级级别的另一个模式。

#### 场景：项目模式遮蔽包
- **当** 用户运行 `openspec schema which spec-driven` 且项目和包都有 `spec-driven`
- **那么** 系统显示项目模式处于活跃状态
- **并且** 指示它遮蔽了包版本
- **并且** 显示被遮蔽的包模式的路径

#### 场景：无遮蔽
- **当** 模式仅存在于一个位置
- **那么** 系统不显示遮蔽信息

#### 场景：多重遮蔽
- **当** 项目模式同时遮蔽用户和包模式
- **那么** 系统按优先级顺序列出所有被遮蔽的位置

### 需求：Schema which 输出 JSON 格式
CLI 应支持 `--json` 标志用于机器可读输出。

#### 场景：基础 JSON 输出
- **当** 用户运行 `openspec schema which spec-driven --json`
- **那么** 系统输出包含 `name`、`source` 和 `path` 字段的 JSON

#### 场景：带遮蔽的 JSON 输出
- **当** 用户运行 `openspec schema which spec-driven --json` 且模式有遮蔽
- **那么** JSON 包含 `shadows` 数组，每个被遮蔽的模式包含 `source` 和 `path`

### 需求：Schema which 支持列表模式
CLI 应支持列出所有模式及其解析源。

#### 场景：列出所有模式
- **当** 用户运行 `openspec schema which --all`
- **那么** 系统显示按源分组的所有可用模式
- **并且** 指示哪些模式遮蔽了其他模式

#### 场景：以 JSON 格式列出
- **当** 用户运行 `openspec schema which --all --json`
- **那么** 系统输出包含每个模式解析信息的 JSON 数组
