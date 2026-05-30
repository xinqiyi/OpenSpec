## 新增需求

### 需求：Schema init 命令创建项目本地模式
CLI 应提供 `openspec schema init <name>` 命令，在 `openspec/schemas/<name>/` 下创建新的模式目录，包含有效的 `schema.yaml` 文件和默认模板文件。

#### 场景：使用有效名称创建模式
- **当** 用户运行 `openspec schema init my-workflow`
- **那么** 系统创建 `openspec/schemas/my-workflow/` 目录
- **并且** 创建包含名称、版本、描述和工件数组的 `schema.yaml`
- **并且** 创建工件引用的模板文件
- **并且** 显示包含创建路径的成功消息

#### 场景：拒绝无效的模式名称
- **当** 用户运行 `openspec schema init "My Workflow"`（包含空格）
- **那么** 系统显示有关无效模式名称的错误
- **并且** 建议使用 kebab-case 格式
- **并且** 以非零退出码退出

#### 场景：模式名称已存在
- **当** 用户运行 `openspec schema init existing-schema` 且 `openspec/schemas/existing-schema/` 已存在
- **那么** 系统显示模式已存在的错误
- **并且** 建议使用 `--force` 覆盖或使用 `schema fork` 复制
- **并且** 以非零退出码退出

### 需求：Schema init 支持交互式模式
CLI 应在交互式终端中运行且未使用显式标志时，提示用户进行模式配置。

#### 场景：交互式提示输入描述
- **当** 用户在交互式终端中运行 `openspec schema init my-workflow`
- **那么** 系统提示输入模式描述
- **并且** 在生成的 `schema.yaml` 中使用提供的描述

#### 场景：交互式提示选择工件
- **当** 用户在交互式终端中运行 `openspec schema init my-workflow`
- **那么** 系统显示包含常见工件（proposal、specs、design、tasks）的多选提示
- **并且** 每个选项包含简短描述
- **并且** 在生成的 `schema.yaml` 中使用选中的工件

#### 场景：带标志的非交互式模式
- **当** 用户运行 `openspec schema init my-workflow --description "My workflow" --artifacts proposal,tasks`
- **那么** 系统创建模式而不提示
- **并且** 使用标志值进行配置

### 需求：Schema init 支持设置项目默认值
CLI 应提供将新创建的模式设置为项目默认值的选项。

#### 场景：交互式设置为默认值
- **当** 用户在交互式模式下运行 `openspec schema init my-workflow`
- **并且** 用户确认设置为默认值
- **那么** 系统更新 `openspec/config.yaml` 中的 `defaultSchema: my-workflow`

#### 场景：通过标志设置为默认值
- **当** 用户运行 `openspec schema init my-workflow --default`
- **那么** 系统创建模式并更新 `openspec/config.yaml` 中的 `defaultSchema: my-workflow`

#### 场景：跳过设置默认值
- **当** 用户运行 `openspec schema init my-workflow --no-default`
- **那么** 系统创建模式而不修改 `openspec/config.yaml`

### 需求：Schema init 输出 JSON 格式
CLI 应支持 `--json` 标志用于机器可读输出。

#### 场景：成功时的 JSON 输出
- **当** 用户运行 `openspec schema init my-workflow --json --description "Test" --artifacts proposal`
- **那么** 系统输出包含 `created: true`、`path` 和 `schema` 字段的 JSON
- **并且** 不显示交互式提示或旋转动画

#### 场景：错误时的 JSON 输出
- **当** 用户运行 `openspec schema init "invalid name" --json`
- **那么** 系统输出包含描述问题的 `error` 字段的 JSON
- **并且** 以非零退出码退出
