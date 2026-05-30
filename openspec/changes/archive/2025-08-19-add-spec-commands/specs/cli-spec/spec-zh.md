## 新增需求

### 需求：Spec 命令

系统应提供一个 `spec` 命令，包含用于显示、列出和验证规范的子命令。

#### 场景：以 JSON 格式显示规范

- **当** 执行 `openspec spec show init --json`
- **则** 解析 markdown 规范文件
- **并且** 按层次提取标题和内容
- **并且** 输出有效的 JSON 到标准输出

#### 场景：列出所有规范

- **当** 执行 `openspec spec list`
- **则** 扫描 openspec/specs 目录
- **并且** 返回所有可用能力的列表
- **并且** 支持使用 `--json` 标志输出 JSON

#### 场景：筛选规范内容

- **当** 执行 `openspec spec show init --requirements`
- **则** 仅显示需求名称和 SHALL 语句
- **并且** 排除场景内容

#### 场景：验证规范结构

- **当** 执行 `openspec spec validate init`
- **则** 解析规范文件
- **并且** 根据 Zod schema 进行验证
- **并且** 报告任何结构问题

### 需求：JSON Schema 定义

系统应定义准确表示规范结构的 Zod schemas，用于运行时验证。

#### 场景：Schema 验证

- **当** 将规范解析为 JSON 时
- **则** 使用 Zod schemas 验证结构
- **并且** 确保所有必填字段存在
- **并且** 为验证失败提供清晰的错误消息
