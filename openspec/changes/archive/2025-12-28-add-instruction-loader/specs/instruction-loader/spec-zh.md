# instruction-loader spec

## 目的
从 schema 目录加载 template，并用变更特定上下文丰富 template 以指导 artifact 创建。

## 新增需求

### 需求：template 加载
系统应从 schema 目录加载 template。

#### 场景：从 schema 目录加载 template
- **WHEN** 调用 `loadTemplate(schemaName, templatePath)`
- **THEN** 系统从 `schemas/<schemaName>/templates/<templatePath>` 加载 template

#### 场景：template 文件未找到
- **WHEN** template 文件在 schema 的 template 目录中不存在
- **THEN** 系统抛出包含 template 路径的错误

### 需求：变更上下文加载
系统应加载结合图谱和完成状态的变更上下文。

#### 场景：为现有变更加载上下文
- **WHEN** 为现有变更调用 `loadChangeContext(projectRoot, changeName)`
- **THEN** 系统返回包含图谱、完成集合、schema 名称和变更信息的上下文

#### 场景：使用自定义 schema 加载上下文
- **WHEN** 调用 `loadChangeContext(projectRoot, changeName, schemaName)`
- **THEN** 系统使用指定的 schema 而非默认 schema

#### 场景：为不存在的变更目录加载上下文
- **WHEN** 为不存在的变更目录调用 `loadChangeContext`
- **THEN** 系统返回包含空完成集合的上下文

### 需求：template 丰富
系统应使用变更特定上下文丰富 template。

#### 场景：包含 artifact 元数据
- **WHEN** 为 artifact 生成指令时
- **THEN** 输出包含变更名称、artifact ID、schema 名称和输出路径

#### 场景：包含依赖状态
- **WHEN** artifact 有依赖项时
- **THEN** 输出显示每个依赖项的完成状态（完成/缺失）

#### 场景：包含解锁的 artifact
- **WHEN** 生成指令时
- **THEN** 输出包含在此 artifact 之后哪些 artifact 变为可用

#### 场景：根 artifact 指示器
- **WHEN** artifact 没有依赖项
- **THEN** 依赖项部分指示这是一个根 artifact

### 需求：状态格式化
系统应将变更状态格式化为可读输出。

#### 场景：所有 artifact 已完成
- **WHEN** 所有 artifact 完成时
- **THEN** 状态显示所有 artifact 为"完成"

#### 场景：混合完成状态
- **WHEN** 部分 artifact 完成时
- **THEN** 状态显示已完成为"done"，就绪为"ready"，阻塞为"blocked"

#### 场景：阻塞 artifact 详情
- **WHEN** artifact 被阻塞时
- **THEN** 状态显示哪些依赖项缺失

#### 场景：包含输出路径
- **WHEN** 格式化状态时
- **THEN** 每个 artifact 显示其输出路径 schema
