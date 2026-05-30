## 1. POC 发现和模型决策

- [x] 1.1 在 proposal/设计 artifact 中捕获基础 POC 发现
- [x] 1.2 确定 `.openspec-workspace/` 作为 workspace 元数据目录
- [x] 1.3 定义最小 workspace 根形状和根标记
- [x] 1.4 定义提交的 workspace 状态与机器本地 workspace 状态
- [x] 1.5 捕获 workspace 设置仅在至少一个 repository 或文件夹链接后才有用
- [x] 1.6 捕获 repository 拥有的 spec 和实施仍由 repository 拥有
- [x] 1.7 捕获 planning 可以包含没有 repository 本地 OpenSpec 状态的 repository 或单体 repository 文件夹
- [x] 1.8 捕获 workspace 持有许多变更，不是功能容器
- [x] 1.9 捕获 `link`/`relink` 作为面向用户的模型，替代 `add-repo`/`update-repo`

## 2. 基础助手

- [x] 2.1 为 `.openspec-workspace/`、`workspace.yaml`、`local.yaml` 和根目录 `changes/` 添加 workspace 路径常量和助手
- [x] 2.2 从任意起始目录添加 workspace 根检测
- [x] 2.3 为最小共享 workspace 状态添加带类型的解析和验证
- [x] 2.4 为最小机器本地 workspace 状态添加带类型的解析和验证
- [x] 2.5 确保 repository 本地 `openspec/` 项目不被误认为是协调 workspace
- [x] 2.6 使用 `getGlobalDataDir()/workspaces` 添加标准 workspace 位置解析器
- [x] 2.7 确保 workspace 路径助手使用平台路径 API，避免硬编码的 POSIX 分隔符
- [x] 2.8 添加本地 workspace 注册表路径常量和助手

## 3. 元数据和本地状态

- [x] 3.1 使用 workspace 名称和稳定链接映射定义带版本的共享状态形状
- [x] 3.2 使用稳定链接名称映射到本地路径定义带版本的本地状态形状
- [x] 3.3 确保本地状态文件被视为机器本地，OpenSpec 创建的 workspace 从可移植协作状态中排除 `.openspec-workspace/local.yaml`
- [x] 3.4 为无效版本、无效链接名称、格式错误的链接映射和格式错误的本地路径映射添加验证
- [x] 3.5 在读取和写入本地路径状态时，保留本机 Windows 和 WSL2 路径字符串
- [x] 3.6 使用 workspace 名称映射到 workspace 根目录定义带版本的本地注册表形状
- [x] 3.7 确保本地注册表被视为便利索引，而非 workspace 真实源

## 4. 文档和指导

- [x] 4.1 记录协调 workspace 心智模型
- [x] 4.2 记录 `.openspec-workspace/` 与 repository 本地 `openspec/` 的区别
- [x] 4.3 记录稳定链接名称作为引用链接 repository 和文件夹的方式
- [x] 4.4 记录哪些行为有意推迟到以后的 workspace 切片
- [x] 4.5 记录本机 Windows/PowerShell 和 WSL2 路径行为，用于管理 workspace 存储
- [x] 4.6 记录没有 repository 本地 OpenSpec 的链接 repository/文件夹和大型单体 repository planning 行为
- [x] 4.7 记录本地 workspace 注册表和全局命令模型

## 5. 验证

- [x] 5.1 为根检测和非检测情况添加单元测试
- [x] 5.2 为共享状态和本地状态解析添加单元测试
- [x] 5.3 为标准 workspace 位置解析添加单元测试，包括 XDG/Linux 回退和本机 Windows 回退
- [x] 5.4 添加单元测试，验证本地状态解析保留本机 Windows 和 WSL2 风格路径
- [x] 5.5 为 repository 本地兼容性边界添加单元测试
- [x] 5.6 添加测试或文档覆盖，验证链接的 repository/文件夹不需要 repository 本地 `openspec/`
- [x] 5.7 为相同 workspace 模型下的单体 repository 文件夹链接添加测试或文档覆盖
- [x] 5.8 添加本地注册表解析和过期注册表条目的测试
- [x] 5.9 添加测试或文档覆盖，验证 OpenSpec 创建 workspace 中 `.openspec-workspace/local.yaml` 的排除
- [x] 5.10 运行 `openspec validate workspace-foundation --strict`
- [x] 5.11 运行新的 workspace 基础助手的针对性测试覆盖
