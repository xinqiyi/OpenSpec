## 新增需求

### 需求：workspace planning 词汇
OpenSpec 约定应使用面向用户的产品语言来区分 workspace planning 概念。

#### 场景：命名影响区域
- **WHEN** 文档或生成的指引提及 workspace 变更涉及的 repository、文件夹、包、服务、应用或文档站点时
- **THEN** 应将其称为影响区域
- **AND** 应避免使用"目标 repository"或"repository 切片"作为主要面向用户的术语

#### 场景：命名交付切片
- **WHEN** 文档或生成的指引提及较大变更内部的交付 delta 时
- **THEN** 仅在交付排序是主题时才应将其称为切片或阶段
- **AND** 不应将切片用作 repository、文件夹或影响区域的同义词

### 需求：workspace planning 与实施的边界
OpenSpec 约定应区分 workspace 级别的 planning 与 repository 本地的实施所有权。

#### 场景：workspace 作为共享 planning 中心
- **WHEN** 变更跨越已链接的 repository 或文件夹时
- **THEN** 约定应将 workspace 描述为共享 planning 中心
- **AND** repository 本地的实施中心应保留对其代码和 spec 行为的所有权

#### 场景：避免以物化优先的语言表达
- **WHEN** 文档解释 workspace 变更创建时
- **THEN** 应从共享 planning 和影响区域的角度描述用户成果
- **AND** 应避免让用户在能够 planning 之前就需要理解诸如物化等实施术语

#### 场景：保留熟悉的 workflow 动词
- **WHEN** workspace 指引描述 OpenSpec workflow 时
- **THEN** 应保留熟悉的动词：探索、提议、应用、验证和 archive
- **AND** 应解释 workspace 上下文改变了路径、范围和允许的编辑根目录，而不是创建了一个独立的 workflow 体系
