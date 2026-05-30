## 新增需求

### 需求：堆叠 planning 命令
变更 CLI 应提供用于活动变更依赖感知排序的命令。

#### 场景：显示依赖图
- **WHEN** 用户运行 `openspec change graph`
- **THEN** CLI 应显示活动变更的依赖关系
- **AND** 应包含确定性的推荐执行顺序

#### 场景：显示下一个无阻塞变更
- **WHEN** 用户运行 `openspec change next`
- **THEN** CLI 应列出未被未解决依赖阻塞的变更
- **AND** 当存在多个选项时，应使用确定性决胜规则

### 需求：拆分大型变更脚手架
变更 CLI 应支持从现有大型变更搭建子片段脚手架。

#### 场景：Split 命令搭建子变更脚手架
- **WHEN** 用户运行 `openspec change split <change-id>`
- **THEN** CLI 应创建包含 proposal/任务存根的子变更目录
- **AND** 生成的元数据应包含指向源变更的 `parent` 和依赖链接

#### 场景：对已拆分的变更重新运行 split
- **WHEN** 用户对已存在生成子目录的父级运行 `openspec change split <change-id>`
- **THEN** CLI 应以确定性的可操作错误失败
- **AND** 除非请求显式覆盖 schema，否则不应修改现有子变更内容
