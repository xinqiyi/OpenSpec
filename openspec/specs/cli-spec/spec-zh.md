# cli-spec spec

## 目的

定义 `openspec spec` 命令用于列出、显示和验证真实来源 spec 的行为。

## 需求

### 需求：交互式 spec 显示

spec show 命令应在未提供 spec-id 时支持交互式选择。

#### 场景：用于 show 的交互式 spec 选择

- **WHEN** 执行 `openspec spec show` 不带参数
- **THEN** 显示可用 spec 的交互式列表
- **AND** 允许用户选择要显示的 spec
- **AND** 显示所选 spec 的内容
- **AND** 保留所有现有的 show 选项（--json、--requirements、--no-scenarios、-r）

#### 场景：非交互式回退保持当前行为

- **GIVEN** 标准输入不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **WHEN** 执行 `openspec spec show` 不带 spec-id
- **THEN** 不进行交互式提示
- **AND** 打印现有缺失 spec-id 的错误信息
- **AND** 设置非零退出码

### 需求：Spec 命令

系统应提供 `spec` 命令，包含用于显示、列出和验证 spec 的子命令。

#### 场景：以 JSON 格式显示 spec

- **WHEN** 执行 `openspec spec show init --json`
- **THEN** 解析 Markdown spec 文件
- **AND** 按层次提取标题和内容
- **AND** 向 stdout 输出有效的 JSON

#### 场景：列出所有 spec

- **WHEN** 执行 `openspec spec list`
- **THEN** 扫描 openspec/specs 目录
- **AND** 返回所有可用能力的列表
- **AND** 支持使用 `--json` 标志输出 JSON

#### 场景：过滤 spec 内容

- **WHEN** 执行 `openspec spec show init --requirements`
- **THEN** 仅显示需求名称和 SHALL 语句
- **AND** 排除场景内容

#### 场景：验证 spec 结构

- **WHEN** 执行 `openspec spec validate init`
- **THEN** 解析 spec 文件
- **AND** 根据 Zod schema 进行验证
- **AND** 报告任何结构性问题

### 需求：JSON schema 定义

系统应定义准确表示 spec 结构的 Zod schema，用于运行时验证。

#### 场景：schema 验证

- **WHEN** 将 spec 解析为 JSON 时
- **THEN** 使用 Zod schema 验证结构
- **AND** 确保所有必填字段存在
- **AND** 为验证失败提供清晰的错误信息

### 需求：交互式 spec 验证

spec validate 命令应在未提供 spec-id 时支持交互式选择。

#### 场景：用于验证的交互式 spec 选择

- **WHEN** 执行 `openspec spec validate` 不带参数
- **THEN** 显示可用 spec 的交互式列表
- **AND** 允许用户选择要验证的 spec
- **AND** 验证所选 spec
- **AND** 保留所有现有的验证选项（--strict、--json）

#### 场景：非交互式回退保持当前行为

- **GIVEN** 标准输入不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **WHEN** 执行 `openspec spec validate` 不带 spec-id
- **THEN** 不进行交互式提示
- **AND** 打印现有缺失 spec-id 的错误信息
- **AND** 设置非零退出码
