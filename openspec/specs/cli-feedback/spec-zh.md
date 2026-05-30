# cli-feedback 规范

## 目的
定义 `openspec feedback` 的行为，通过 `gh` CLI 安全地创建 GitHub Issue，并在自动化不可用时提供手动回退。

## 需求
### 需求：反馈命令

系统应提供一个 `openspec feedback` 命令，使用 `gh` CLI 在 openspec 仓库中创建 GitHub Issue。系统应使用带参数数组的 `execFileSync` 以防止 shell 注入漏洞。

#### 场景：简单反馈提交

- **WHEN** 用户执行 `openspec feedback "Great tool!"`
- **THEN** 系统执行 `gh issue create`，标题为 "Feedback: Great tool!"
- **AND** 在 openspec 仓库中创建 issue
- **AND** issue 具有 `feedback` 标签
- **AND** 系统显示创建的 issue URL

#### 场景：安全命令执行

- **WHEN** 通过 `gh` CLI 提交反馈
- **THEN** 系统使用带独立参数数组的 `execFileSync`
- **AND** 用户输入不通过 shell 传递
- **AND** shell 元字符（引号、反引号、$() 等）被视为文字文本

#### 场景：带正文的反馈

- **WHEN** 用户执行 `openspec feedback "Title here" --body "Detailed description..."`
- **THEN** 系统创建一个具有指定标题的 GitHub Issue
- **AND** issue 正文包含详细描述
- **AND** issue 正文包含元数据（OpenSpec 版本、平台、时间戳）

### 需求：GitHub CLI 依赖

系统应在 `gh` CLI 可用时使用其进行自动反馈提交，并在 `gh` 未安装或未认证时提供手动提交回退。系统应使用适合平台的命令检测 `gh` CLI 的可用性。

#### 场景：缺失 gh CLI 并回退

- **WHEN** 用户运行 `openspec feedback "message"`
- **AND** `gh` CLI 未安装（在 PATH 中未找到）
- **THEN** 系统显示警告："GitHub CLI not found. Manual submission required."
- **AND** 输出带有分隔符的结构化反馈内容：
  - "--- FORMATTED FEEDBACK ---"
  - 标题行
  - 标签行
  - 带元数据的正文内容
  - "--- END FEEDBACK ---"
- **AND** 显示预填充的 GitHub issue URL 用于手动提交
- **AND** 以零退出码退出（成功回退）

#### 场景：Unix 上的跨平台 gh CLI 检测

- **WHEN** 系统运行在 macOS 或 Linux 上（平台为 'darwin' 或 'linux'）
- **AND** 检查 `gh` CLI 是否已安装
- **THEN** 系统执行 `which gh` 命令

#### 场景：Windows 上的跨平台 gh CLI 检测

- **WHEN** 系统运行在 Windows 上（平台为 'win32'）
- **AND** 检查 `gh` CLI 是否已安装
- **THEN** 系统执行 `where gh` 命令

#### 场景：未认证的 gh CLI 并回退

- **WHEN** 用户运行 `openspec feedback "message"`
- **AND** `gh` CLI 已安装但未认证
- **THEN** 系统显示警告："GitHub authentication required. Manual submission required."
- **AND** 输出结构化反馈内容（与缺失 gh CLI 场景相同格式）
- **AND** 显示预填充的 GitHub issue URL 用于手动提交
- **AND** 显示认证说明："To auto-submit in the future: gh auth login"
- **AND** 以零退出码退出（成功回退）

#### 场景：已认证的 gh CLI

- **WHEN** 用户运行 `openspec feedback "message"`
- **AND** `gh auth status` 返回成功（已认证）
- **THEN** 系统继续执行反馈提交

### 需求：Issue 元数据

系统应在 GitHub Issue 正文中包含相关元数据。

#### 场景：标准元数据

- **WHEN** 为反馈创建 GitHub Issue
- **THEN** issue 正文包含：
  - OpenSpec CLI 版本
  - 平台（darwin、linux、win32）
  - 提交时间戳
  - 分隔线："---\nSubmitted via OpenSpec CLI"

#### 场景：Windows 平台元数据

- **WHEN** 在 Windows 上为反馈创建 GitHub Issue
- **THEN** issue 正文包含 "Platform: win32"
- **AND** 所有平台检测使用 Node.js `os.platform()` API

#### 场景：无敏感元数据

- **WHEN** 为反馈创建 GitHub Issue
- **THEN** issue 正文不包含：
  - 用户系统中的文件路径
  - 项目名称或目录名称
  - 环境变量
  - IP 地址

### 需求：反馈始终有效

系统应允许反馈提交，无论遥测设置如何。

#### 场景：遥测禁用时的反馈

- **WHEN** 用户通过 `OPENSPEC_TELEMETRY=0` 禁用了遥测
- **AND** 用户运行 `openspec feedback "message"`
- **THEN** 仍然通过 `gh` CLI 提交反馈
- **AND** 不发送遥测事件

#### 场景：CI 环境中的反馈

- **WHEN** 环境中设置了 `CI=true`
- **AND** 用户运行 `openspec feedback "message"`
- **THEN** 反馈提交正常进行（如果 `gh` 可用且已认证）

### 需求：错误处理

系统应优雅地处理反馈提交错误。

#### 场景：gh CLI 执行失败

- **WHEN** `gh issue create` 命令失败
- **THEN** 系统显示 `gh` CLI 的错误输出
- **AND** 以与 `gh` 相同的退出码退出

#### 场景：网络故障

- **WHEN** `gh` CLI 报告网络连接问题
- **THEN** 系统显示 `gh` 的错误消息
- **AND** 建议检查网络连接
- **AND** 以非零退出码退出

### 需求：面向代理的反馈技能

系统应提供一个 `/feedback` 技能，指导代理收集和提交用户反馈。

#### 场景：代理发起的反馈

- **WHEN** 用户在代理对话中调用 `/feedback`
- **THEN** 代理从对话中收集上下文
- **AND** 起草包含丰富内容的反馈 issue
- **AND** 匿名化敏感信息
- **AND** 向用户展示草稿以供批准
- **AND** 在用户确认后通过 `openspec feedback` 命令提交

#### 场景：上下文丰富

- **WHEN** 代理起草反馈
- **THEN** 代理包含相关上下文，例如：
  - 正在执行的任务
  - 哪些方面效果好或差
  - 具体的痛点或赞扬

#### 场景：匿名化

- **WHEN** 代理起草反馈
- **THEN** 代理移除或替换：
  - 文件路径替换为 `<path>` 或通用描述
  - API 密钥、令牌、机密替换为 `<redacted>`
  - 公司/组织名称替换为 `<company>`
  - 个人名称替换为 `<user>`
  - 特定 URL 替换为 `<url>`，除非是公开/相关的

#### 场景：需要用户确认

- **WHEN** 代理已起草反馈
- **THEN** 代理必须向用户展示完整草稿
- **AND** 在提交前请求明确批准
- **AND** 允许用户请求修改
- **AND** 仅在用户确认后提交

### 需求：Shell 补全

系统应为 feedback 命令提供 shell 补全。

#### 场景：命令补全

- **WHEN** 用户输入 `openspec fee<TAB>`
- **THEN** shell 补全为 `openspec feedback`

#### 场景：标志补全

- **WHEN** 用户输入 `openspec feedback "msg" --<TAB>`
- **THEN** shell 建议可用的标志（`--body`）
