# template-artifact-pipeline spec

## 目的

定义一个统一的 workflow template 生成架构，集中管理 workflow 定义、工具能力连接、转换执行和 artifact 同步，同时保持输出保真度。

## 新增的需求

### 需求：spec workflow 清单

系统应将 spec workflow 清单定义为生成的 skill 和命令 artifact 的唯一真实来源。

#### 场景：一次性注册 workflow

- **WHEN** 添加或修改 workflow（例如 `explore`、`ff` 或 `onboard`）时
- **THEN** 其 spec 定义应在 workflow 清单中一次性注册
- **AND** skill/命令投影应从该清单派生
- **AND** 不应需要重复维护的列表

#### 场景：必需的 skill 元数据

- **WHEN** 在清单中定义 workflow skill 条目时
- **THEN** 应包含必需的元数据字段（`license`、`compatibility` 和 `metadata`）
- **AND** 生成应使用这些值或对所有 workflow 以一致的方式使用显式默认值

### 需求：工具配置文件注册表

系统应定义一个工具配置文件注册表，捕获每个工具的生成能力。

#### 场景：解析工具能力

- **WHEN** 为所选工具生成 artifact 时
- **THEN** 系统应解析声明 skill 路径能力、命令适配器连接和转换集的工具配置文件
- **AND** 支持 skill 但没有命令适配器的工具应被显式处理，无隐式回退行为

#### 场景：能力一致性验证

- **WHEN** 运行验证检查时
- **THEN** 系统应检测已配置工具、配置文件定义和已注册适配器之间的不匹配
- **AND** 在开发/CI 中以可操作的错误失败

### 需求：有序转换流水线

系统应支持具有显式范围和阶段语义的有序 artifact 转换。

#### 场景：执行适配器前和适配器后转换

- **WHEN** 生成 artifact 时
- **THEN** 匹配的转换应基于阶段和优先级按确定性顺序执行
- **AND** `preAdapter` 转换应在命令适配器格式化之前运行
- **AND** `postAdapter` 转换应在适配器格式化之后运行

#### 场景：以声明方式应用工具特定重写

- **WHEN** 工具需要指令重写（例如命令引用语法变更）时
- **THEN** 这些重写应作为具有显式适用性谓词的已注册转换来实现
- **AND** 生成入口点不应实现临时重写逻辑

### 需求：共享 artifact 同步引擎

系统应提供一个由所有生成入口点使用的共享 artifact 同步引擎。

#### 场景：init 和 update 使用相同引擎

- **WHEN** `openspec init` 或 `openspec update` 写入 skill/命令时
- **THEN** 两个流程应使用相同的编排引擎进行 planning、渲染、验证和写入 artifact
- **AND** 行为差异应由配置驱动，而非单独的重复循环

#### 场景：遗留升级路径复用引擎

- **WHEN** 遗留清理触发 artifact 重新生成时
- **THEN** 重新生成路径应使用相同的共享引擎
- **AND** 生成的输出应遵循相同的转换和验证规则

### 需求：保真度护栏

系统应实施防止重构期间输出漂移的护栏。

#### 场景：投影一致性检查

- **WHEN** CI 运行 template 生成测试时
- **THEN** 应验证清单派生的投影保持一致（workflow、命令 ID、skill 目录）
- **AND** 检测缺失的导出或缺失的 workflow 注册

#### 场景：输出一致性检查

- **WHEN** 对具有代表性的 workflow/工具组合运行一致性测试时
- **THEN** 生成的 artifact 应在行为上等同于已批准的基线，除非有意更改
- **AND** 有意更改应在明确的 spec/proposal 更新中捕获
