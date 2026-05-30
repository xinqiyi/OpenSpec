## 1. 首选打开程序状态

- [x] 1.1 为工作区本地状态解析和序列化添加结构化的 `preferred_opener` 支持
- [x] 1.2 在添加 `preferred_opener` 的同时，支持对现有本地工作区文件的向后兼容解析
- [x] 1.3 验证支持的打开程序值：`codex`、`claude`、`github-copilot` 和 `editor`
- [x] 1.4 将 `editor` 映射到 `kind: editor, id: vscode`
- [x] 1.5 将代理打开程序值映射到 `kind: agent` 及匹配的 `id`
- [x] 1.6 为 `code`、`codex` 和 `claude` 添加简单的可执行文件检测
- [x] 1.7 为首选打开程序解析、序列化和无效打开程序值添加单元测试

## 2. 设置打开程序选择

- [x] 2.1 为首选打开程序添加交互式设置提示
- [x] 2.2 显示所有受支持的打开程序选择，已检测到的打开程序排在前面
- [x] 2.3 用清晰的可获得性说明标记不可用的打开程序选择
- [x] 2.4 在需要回退时，优先选择纯编辑器选项作为设置回退
- [x] 2.5 为非交互式设置添加 `workspace setup --opener <id>`
- [x] 2.6 在提供 `--opener` 时，在非交互式设置期间存储首选打开程序
- [x] 2.7 为交互式打开程序选择和非交互式 `--opener` 添加测试
- [x] 2.8 添加测试，验证省略 `--opener` 的非交互式设置保持打开程序未设置

## 3. 打开表面同步

- [x] 3.1 添加由 setup、link 和 relink 使用的共享打开表面同步助手
- [x] 3.2 创建或刷新根目录的 `AGENTS.md`，包含 OpenSpec 管理工作区指导块
- [x] 3.3 保留用户编写的 `AGENTS.md` 中受管理块之外的内容
- [x] 3.4 将受管理块附加到未标记的现有 `AGENTS.md` 文件
- [x] 3.5 在工作区根目录创建或刷新 `<workspace-name>.code-workspace`
- [x] 3.6 在 `.code-workspace` 中包含工作区根目录和每个具有有效本地路径的链接仓库或文件夹
- [x] 3.7 从 `.code-workspace` 中省略本地路径缺失或无效的链接仓库或文件夹
- [x] 3.8 使用特定维护的 `<workspace-name>.code-workspace` 条目刷新 `.gitignore`
- [x] 3.9 将忽略更新限定在维护的 `<workspace-name>.code-workspace` 文件
- [x] 3.10 为 `.code-workspace` 路径构造添加跨平台测试，并在可行时添加 Windows 风格路径测试

## 4. 工作区打开选择

- [x] 4.1 添加 `openspec workspace open [name]`
- [x] 4.2 支持 `openspec workspace open --workspace <name>` 作为位置参数的别名
- [x] 4.3 当位置参数和 `--workspace` 都提供但值不同时，清晰失败
- [x] 4.4 从工作区文件夹或子目录运行时，打开当前工作区
- [x] 4.5 在工作区外部运行时，自动选择唯一已知的工作区
- [x] 4.6 当有多个已知工作区时，显示交互式选择器
- [x] 4.7 在非交互式模式下报告模糊的工作区选择，并列出已知工作区名称
- [x] 4.8 清晰报告未解析的工作区选择，并建议 `openspec workspace setup`
- [x] 4.9 处理不支持的 `--prepare-only`、`--json` 和 `--change` 标志并给出清晰错误
- [x] 4.10 为选择、冲突、不支持标志和无工作区情况添加命令集成测试

## 5. 打开程序解析

- [x] 5.1 在工作区本地偏好之前解析命令行打开程序覆盖
- [x] 5.2 实现 `workspace open --agent codex`
- [x] 5.3 实现 `workspace open --agent claude`
- [x] 5.4 实现 `workspace open --agent github-copilot`
- [x] 5.5 实现 `workspace open --editor`
- [x] 5.6 对于 `--agent` 和 `--editor` 覆盖，保持存储的首选打开程序不变
- [x] 5.7 当打开程序偏好未设置时，交互式提示选择打开程序
- [x] 5.8 在非交互式模式下报告未设置的打开程序偏好，并给出覆盖指导
- [x] 5.9 为打开程序优先级、提示、非交互式失败和未更改的偏好行为添加测试

## 6. 打开程序启动器

- [x] 6.1 通过使用 `code` 打开维护的 `.code-workspace` 文件来启动 VS Code 编辑器
- [x] 6.2 通过使用 VS Code 打开维护的 `.code-workspace` 文件来启动 GitHub Copilot
- [x] 6.3 从工作区根目录启动 Codex，并附加有效的链接路径
- [x] 6.4 从工作区根目录启动 Claude，并附加有效的链接路径
- [x] 6.5 当代理 CLI 需要初始提示参数时，使用最简启动提示
- [x] 6.6 跳过的损坏链接以 `openspec workspace doctor` 作为修复路径报告
- [x] 6.7 当所选打开程序可执行文件不可用时，清晰失败
- [x] 6.8 在 VS Code 打开程序可用性错误中包含 `.code-workspace` 路径
- [x] 6.9 启动时保持所选打开程序为必需
- [x] 6.10 为启动器命令构造添加单元测试，使用外部工具的测试替身

## 7. 文档和命令元数据

- [x] 7.1 更新工作区命令帮助，涵盖 setup `--opener`、open 位置参数、`--workspace`、`--agent` 和 `--editor`
- [x] 7.2 为新的工作区打开表面更新命令注册表和 shell 补全元数据
- [x] 7.3 更新工作区文档，描述首选打开程序、编辑器打开、代理打开和 `.code-workspace` 行为
- [x] 7.4 记录 `.code-workspace` 是机器本地的，默认被忽略
- [x] 7.5 记录根工作区打开支持探索和规划，实现从显式用户请求开始

## 8. 验证

- [x] 8.1 运行 `node bin/openspec.js validate workspace-open-agent-context --strict`
- [x] 8.2 运行针对性工作区命令测试
- [x] 8.3 运行针对性工作区基础测试
- [x] 8.4 运行涵盖 Codex、Claude、GitHub Copilot 和 VS Code 编辑器路径的命令生成或启动器测试
- [x] 8.5 为工作区打开表面运行跨平台路径测试
- [x] 8.6 运行相关的 TypeScript 测试套件
- [x] 8.7 运行 `pnpm run build`
