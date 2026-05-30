## 新增需求

### 需求：全局配置中的安装作用域字段
全局配置 schema 应包含安装作用域偏好。

#### 场景：配置结构支持安装作用域
- **WHEN** 读取或写入全局配置时
- **THEN** 配置应支持允许值为 `global` 和 `project` 的 `installScope`

#### 场景：schema 演化默认值
- **WHEN** 加载不含 `installScope` 的旧版配置时
- **THEN** 系统应保持 schema 兼容性而不修改文件
- **AND** 在用户显式设置 `installScope` 之前，有效安装作用域应解析为 `project`
- **AND** 保留所有其他现有字段

#### 场景：新配置默认值
- **WHEN** 创建新的全局配置时
- **THEN** 系统应默认持久化 `installScope: global`
- **AND** 用户可以显式切换到 `project`

#### 场景：无效的安装作用域值
- **WHEN** 配置验证接收到无效的安装作用域值时
- **THEN** 应拒绝该值
- **AND** 系统应保留现有的有效配置
