## 新增需求

### 需求：命令表面能力解析
init 命令应首先使用显式元数据解析每个选定工具的命令表面，然后进行确定性推断。

#### 场景：显式命令表面覆盖
- **WHEN** 工具声明了显式的命令表面能力
- **THEN** init 应使用该显式能力
- **AND** 不应基于适配器存在与否覆盖它

#### 场景：从适配器存在推断命令表面
- **WHEN** 工具未声明显式的命令表面能力
- **AND** 为该工具注册了命令适配器
- **THEN** init 应推断 `adapter` 作为命令表面

#### 场景：纯 skill 工具的命令表面推断
- **WHEN** 工具未声明显式的命令表面能力
- **AND** 没有为该工具注册命令适配器
- **AND** 该工具配置了 `skillsDir`
- **THEN** init 应推断 `skills-invocable` 作为命令表面

#### 场景：无适配器或 skill 时的命令表面推断
- **WHEN** 工具未声明显式的命令表面能力
- **AND** 没有为该工具注册命令适配器
- **AND** 该工具没有 `skillsDir`
- **THEN** init 应推断 `none` 作为命令表面

### 需求：按工具命令表面的交付兼容性
init 命令应使用每个工具的命令表面能力应用交付设置，而非仅凭适配器存在与否。

#### 场景：适配器支持的工具的双重交付
- **WHEN** 用户使用选定的具有命令适配器的工具运行 `openspec init`
- **AND** 交付设置为 `both`
- **THEN** 系统应为活跃 workflow 使用该适配器生成命令文件
- **AND** 当工具具有 `skillsDir` 时应生成或刷新托管 skill

#### 场景：skill 可调用工具的双重交付
- **WHEN** 用户使用命令表面为 `skills-invocable` 的选定工具运行 `openspec init`
- **AND** 交付设置为 `both`
- **THEN** 系统应在工具具有 `skillsDir` 时生成或刷新托管 skill 目录
- **AND** 不应要求为该工具生成适配器命令文件

#### 场景：无命令表面工具的双重交付
- **WHEN** 用户使用命令表面为 `none` 的选定工具运行 `openspec init`
- **AND** 交付设置为 `both`
- **THEN** 系统不应为该工具执行任何命令表面 artifact 操作
- **AND** 可以发出兼容性说明，指示没有可用的命令表面

#### 场景：适配器支持工具的 skill 交付
- **WHEN** 用户使用选定的具有命令适配器的工具运行 `openspec init`
- **AND** 交付设置为 `skills`
- **THEN** 系统应在工具具有 `skillsDir` 时生成或刷新托管 skill 目录
- **AND** 应移除该工具的托管适配器生成的命令文件

#### 场景：skill 可调用工具的 skill 交付
- **WHEN** 用户使用命令表面为 `skills-invocable` 的选定工具运行 `openspec init`
- **AND** 交付设置为 `skills`
- **THEN** 系统应在工具具有 `skillsDir` 时生成或刷新托管 skill 目录
- **AND** 不应要求为该工具生成适配器命令文件

#### 场景：无命令表面工具的 skill 交付
- **WHEN** 用户使用命令表面为 `none` 的选定工具运行 `openspec init`
- **AND** 交付设置为 `skills`
- **THEN** 系统不应为该工具执行任何命令表面 artifact 操作
- **AND** 可以发出兼容性说明，指示没有可用的命令表面

#### 场景：适配器支持工具的命令交付
- **WHEN** 用户使用选定的具有命令适配器的工具运行 `openspec init`
- **AND** 交付设置为 `commands`
- **THEN** 系统应为活跃 workflow 使用该适配器生成命令文件
- **AND** 系统应移除该工具的托管 skill 目录

#### 场景：skill 可调用工具的命令交付
- **WHEN** 用户使用命令表面为 `skills-invocable` 的选定工具运行 `openspec init`
- **AND** 交付设置为 `commands`
- **THEN** 系统应为活跃 workflow 生成或刷新托管 skill 目录
- **AND** 系统不应作为仅命令清理的一部分移除这些托管 skill 目录
- **AND** 系统不应要求为该工具配备命令适配器

#### 场景：混合工具选择的命令交付
- **WHEN** 用户使用多个工具运行 `openspec init`
- **AND** 选定的工具包括适配器支持和 skill 可调用的命令表面
- **AND** 交付设置为 `commands`
- **THEN** 系统应按工具能力应用仅命令行为
- **AND** 生成的安装应包括适配器支持工具的命令文件和 skill 可调用工具的 skill 文件

#### 场景：不支持的命令表面的命令交付
- **WHEN** 用户使用没有命令表面能力的选定工具运行 `openspec init`
- **AND** 交付设置为 `commands`
- **THEN** 系统应在生成或删除 artifact 之前失败
- **AND** 错误应列出不兼容的工具 ID 并说明支持的替代方案（`both` 或 `skills`）

#### 场景：不支持的命令表面的交互式处理
- **WHEN** 用户以交互方式运行 `openspec init`
- **AND** 交付设置为 `commands`
- **AND** 选定的工具包括一个或多个命令表面为 `none` 的工具
- **THEN** CLI 应显示兼容性错误并返回到交互式选择流程以进行更正
- **AND** 在确认有效选择之前不应执行 artifact 写入

### 需求：Init 兼容性指示
init 命令应在交互式和非交互式流程中清晰指示命令表面兼容性结果。

#### 场景：交互式兼容性说明
- **WHEN** init 以交互方式运行
- **AND** 交付为 `commands`
- **AND** 选定的工具包括 skill 可调用的命令表面
- **THEN** 系统应在确认提示之前显示兼容性说明，指示这些工具将使用 skill 作为其命令表面

#### 场景：skill 可调用工具的非交互式兼容性摘要
- **WHEN** init 以非交互方式运行（包括使用 `--tools`）
- **AND** 交付为 `commands`
- **AND** 选定的工具包括一个或多个 `skills-invocable` 命令表面
- **THEN** 命令应以退出码 0 继续
- **AND** 命令应将确定性兼容性摘要行写入 stdout，指示这些工具将使用托管 skill 作为其命令表面

#### 场景：非交互式兼容性失败
- **WHEN** init 以非交互方式运行（包括使用 `--tools`）
- **AND** 交付为 `commands`
- **AND** 选定的工具包括任何没有命令表面能力的工具
- **THEN** 命令应以退出码 1 退出
- **AND** 命令应将确定性、可操作的解决选择指南写入 stderr
