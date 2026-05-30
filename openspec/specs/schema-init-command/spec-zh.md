# schema-init-command spec

## 目的
定义 `openspec schema init` 在交互式和非交互式 schema 下创建项目本地 schema 骨架的行为。

## 需求
### 需求：Schema init 命令创建项目本地 schema
CLI 应提供 `openspec schema init <name>` 命令，在 `openspec/schemas/<name>/` 下创建新的 schema 目录，包含有效的 `schema.yaml` 文件和默认 template 文件。

#### 场景：使用有效名称创建 schema
- **WHEN** 用户运行 `openspec schema init my-workflow`
- **THEN** 系统创建 `openspec/schemas/my-workflow/` 目录
- **AND** 创建包含名称、版本、描述和 artifact 数组的 `schema.yaml`
- **AND** 创建 artifact 引用的 template 文件
- **AND** 显示包含创建路径的成功消息

#### 场景：拒绝无效的 schema 名称
- **WHEN** 用户运行 `openspec schema init "My Workflow"`（包含空格）
- **THEN** 系统显示有关无效 schema 名称的错误
- **AND** 建议使用 kebab-case 格式
- **AND** 以非零退出码退出

#### 场景：schema 名称已存在
- **WHEN** 用户运行 `openspec schema init existing-schema` 且 `openspec/schemas/existing-schema/` 已存在
- **THEN** 系统显示 schema 已存在的错误
- **AND** 建议使用 `--force` 覆盖或使用 `schema fork` 复制
- **AND** 以非零退出码退出

### 需求：Schema init 支持交互式 schema
CLI 应在交互式终端中运行且未使用显式标志时，提示用户进行 schema 配置。

#### 场景：交互式提示输入描述
- **WHEN** 用户在交互式终端中运行 `openspec schema init my-workflow`
- **THEN** 系统提示输入 schema 描述
- **AND** 在生成的 `schema.yaml` 中使用提供的描述

#### 场景：交互式提示选择 artifact
- **WHEN** 用户在交互式终端中运行 `openspec schema init my-workflow`
- **THEN** 系统显示包含常见 artifact（proposal、specs、design、tasks）的多选提示
- **AND** 每个选项包含简短描述
- **AND** 在生成的 `schema.yaml` 中使用选中的 artifact

#### 场景：带标志的非交互式 schema
- **WHEN** 用户运行 `openspec schema init my-workflow --description "My workflow" --artifacts proposal,tasks`
- **THEN** 系统创建 schema 而不提示
- **AND** 使用标志值进行配置

### 需求：Schema init 支持设置项目默认值
CLI 应提供将新创建的 schema 设置为项目默认值的选项。

#### 场景：交互式设置为默认值
- **WHEN** 用户在交互式 schema 下运行 `openspec schema init my-workflow`
- **AND** 用户确认设置为默认值
- **THEN** 系统更新 `openspec/config.yaml` 中的 `defaultSchema: my-workflow`

#### 场景：通过标志设置为默认值
- **WHEN** 用户运行 `openspec schema init my-workflow --default`
- **THEN** 系统创建 schema 并更新 `openspec/config.yaml` 中的 `defaultSchema: my-workflow`

#### 场景：跳过设置默认值
- **WHEN** 用户运行 `openspec schema init my-workflow --no-default`
- **THEN** 系统创建 schema 而不修改 `openspec/config.yaml`

### 需求：Schema init 输出 JSON 格式
CLI 应支持 `--json` 标志用于机器可读输出。

#### 场景：成功时的 JSON 输出
- **WHEN** 用户运行 `openspec schema init my-workflow --json --description "Test" --artifacts proposal`
- **THEN** 系统输出包含 `created: true`、`path` 和 `schema` 字段的 JSON
- **AND** 不显示交互式提示或旋转动画

#### 场景：错误时的 JSON 输出
- **WHEN** 用户运行 `openspec schema init "invalid name" --json`
- **THEN** 系统输出包含描述问题的 `error` 字段的 JSON
- **AND** 以非零退出码退出
