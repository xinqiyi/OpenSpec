## 修改后的需求

### 需求：Schema 加载
系统应从 schema 目录中的 YAML schema 文件加载制品图定义。

#### 场景：有效 schema 加载
- **WHEN** schema 目录包含有效的 `schema.yaml` 文件
- **THEN** 系统返回包含所有制品和依赖关系的 ArtifactGraph

#### 场景：无效 schema 被拒绝
- **WHEN** schema YAML 文件缺少必填字段
- **THEN** 系统抛出带有描述性消息的错误

#### 场景：检测到循环依赖
- **WHEN** schema 包含循环的制品依赖
- **THEN** 系统抛出错误，列出循环中的制品 ID

#### 场景：无效的依赖引用
- **WHEN** 制品的 `requires` 数组引用了不存在的制品 ID
- **THEN** 系统抛出错误，标识无效引用

#### 场景：重复的制品 ID 被拒绝
- **WHEN** schema 包含多个具有相同 ID 的制品
- **THEN** 系统抛出错误，标识重复项

#### 场景：Schema 目录未找到
- **WHEN** 解析没有对应目录的 schema 名称时
- **THEN** 系统抛出错误，列出可用的 schema

## 新增需求

### 需求：Schema 目录结构
系统应支持包含协同定位 template 的自包含 schema 目录。

#### 场景：带 template 的 Schema
- **WHEN** schema 目录包含 `schema.yaml` 和 `templates/` 子目录
- **THEN** 制品可以引用相对于 schema template 目录的 template

#### 场景：用户 schema 覆盖
- **WHEN** schema 目录存在于 `${XDG_DATA_HOME}/openspec/schemas/<name>/`
- **THEN** 系统使用该目录而不是内置目录

#### 场景：内置 schema 回退
- **WHEN** schema 没有用户覆盖
- **THEN** 系统使用包内置的 schema 目录

#### 场景：列出可用 schemas
- **WHEN** 列出 schemas 时
- **THEN** 系统返回来自用户目录和包目录的 schema 名称
