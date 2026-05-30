## 新增需求

### 需求：Spec 命令

系统应提供一个 `spec` 命令，包含用于显示、列出和验证 spec 的子命令。

#### 场景：以 JSON 格式显示 spec

- **WHEN** 执行 `openspec spec show init --json`
- **THEN** 解析 markdown spec 文件
- **AND** 按层次提取标题和内容
- **AND** 输出有效的 JSON 到标准输出

#### 场景：列出所有 spec

- **WHEN** 执行 `openspec spec list`
- **THEN** 扫描 openspec/specs 目录
- **AND** 返回所有可用能力的列表
- **AND** 支持使用 `--json` 标志输出 JSON

#### 场景：筛选 spec 内容

- **WHEN** 执行 `openspec spec show init --requirements`
- **THEN** 仅显示需求名称和 SHALL 语句
- **AND** 排除场景内容

#### 场景：验证 spec 结构

- **WHEN** 执行 `openspec spec validate init`
- **THEN** 解析 spec 文件
- **AND** 根据 Zod schema 进行验证
- **AND** 报告任何结构问题

### 需求：JSON Schema 定义

系统应定义准确表示 spec 结构的 Zod schemas，用于运行时验证。

#### 场景：Schema 验证

- **WHEN** 将 spec 解析为 JSON 时
- **THEN** 使用 Zod schemas 验证结构
- **AND** 确保所有必填字段存在
- **AND** 为验证失败提供清晰的错误消息
