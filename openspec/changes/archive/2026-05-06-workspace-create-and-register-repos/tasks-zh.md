## 1. POC 发现与范围

- [x] 1.1 确认 `setup`、`list` 和 `doctor` 属于此切片
- [x] 1.2 明确 setup 不应拥有首选 agent 或 workspace 打开行为
- [x] 1.3 明确允许链接的 repository 或文件夹以及单体 repository 路径，无需 repository 本地的 OpenSpec 状态
- [x] 1.4 明确关于 JSON 输出、`ls`、`.gitignore`、非交互式 setup、必需首个链接和 relink 行为的决策
- [x] 1.5 明确公共 `workspace create` 不在首个版本范围内
- [x] 1.6 明确 `link`/`relink` 是面向用户的命令

## 2. Workspace 设置

- [x] 2.1 实现 `openspec workspace setup` 作为唯一的公共创建路径
- [x] 2.2 在交互式 setup 中先提示输入 workspace 名称
- [x] 2.3 验证 workspace 名称为 kebab-case，并允许交互式用户重试无效名称
- [x] 2.4 在 setup 期间要求至少一个现有的 repository 或文件夹路径
- [x] 2.5 在 setup 期间从文件夹基本名称推断链接名称
- [x] 2.6 允许用户通过简单的重复提示添加更多 repository 或文件夹
- [x] 2.7 在 setup 后运行 `workspace doctor` 并显示可读摘要
- [x] 2.8 打印 workspace 位置、planning 路径、链接的 repository 或文件夹以及下一步有用命令
- [x] 2.9 将首选 agent 提示和 workspace 打开排除在此切片之外
- [x] 2.10 为机器本地的 workspace 状态添加 `.gitignore` 处理
- [x] 2.11 在本地 workspace 注册表中记录已创建的 workspace
- [x] 2.12 在实际可行的情况下为本机 Windows/PowerShell 和 WSL2 兼容的路径构造添加测试

## 3. 非交互式设置

- [x] 3.1 添加 `workspace setup --no-interactive --name <name> --link <path>` 支持
- [x] 3.2 支持重复的 `--link` 值
- [x] 3.3 支持带推断名称的 `--link <path>`
- [x] 3.4 支持带显式名称的 `--link <name>=<path>`
- [x] 3.5 当非交互式 setup 缺少名称或至少一个链接时优雅失败
- [x] 3.6 在存储本地状态之前，将相对链接路径解析为已验证的绝对运行时本地路径
- [x] 3.7 使用 `workspace setup --json` 时需要 `--no-interactive`
- [x] 3.8 为非交互式 setup 添加 `--json` 输出
- [x] 3.9 当未传递 `--no-interactive` 时保留交互式 setup UX

## 4. Workspace 列表

- [x] 4.1 实现 `openspec workspace list`
- [x] 4.2 添加 `workspace ls` 作为 `workspace list` 的别名
- [x] 4.3 从本地 workspace 注册表列出已知的 OpenSpec 管理的 workspace
- [x] 4.4 处理无 workspace 的情况，提供清晰的下一步操作
- [x] 4.5 显示每个 workspace 位置和链接的 repository 或文件夹
- [x] 4.6 报告过期的注册表条目，附带状态条目，但不删除、重写或修复注册表状态
- [x] 4.7 添加带有类型化 workspace 对象和结构化状态数组的 JSON 输出

## 5. Workspace 选择

- [x] 5.1 使 workspace 命令能够从 workspace 目录外部工作
- [x] 5.2 为需要一个 workspace 的命令添加 `--workspace <name>`
- [x] 5.3 从 workspace 内部运行时使用当前 workspace
- [x] 5.4 使用未注册的当前 workspace，并显示非致命警告状态
- [x] 5.5 在成功的 `workspace link` 或 `workspace relink` 后，在本地注册表中记录未注册的当前 workspace
- [x] 5.6 当当前 workspace 未注册时，保持 `workspace doctor` 仅为诊断
- [x] 5.7 当存在多个已知 workspace 且未指定 workspace 时，显示交互式选择器
- [x] 5.8 当只有一个已知 workspace 时自动选择它
- [x] 5.9 在非交互 schema 下 workspace 选择歧义时清晰失败
- [x] 5.10 当 `--json` workspace 选择歧义时，以结构化状态输出代替提示
- [x] 5.11 使用本地 workspace 注册表进行 workspace 查找

## 6. Workspace 链接

- [x] 6.1 实现带有推断链接名称的 `openspec workspace link <path>`
- [x] 6.2 实现带有显式链接名称的 `openspec workspace link <name> <path>`
- [x] 6.3 接受完整的 repository 根目录和单体 repository 的包/服务/应用文件夹路径
- [x] 6.4 要求链接的路径存在
- [x] 6.5 允许链接没有 repository 本地 `openspec/` 的路径
- [x] 6.6 将稳定的链接名称存储在共享状态中，本地路径存储在机器本地状态中
- [x] 6.7 保持链接名称为文件夹样式，检测重复链接名称并给出特定错误，显示现有链接路径并建议不同名称或 `workspace relink`
- [x] 6.8 在存储本地状态之前，将相对链接路径解析为已验证的绝对运行时本地路径
- [x] 6.9 保留本机 Windows 和 WSL2 样式的路径作为本地路径值，不进行跨运行时转换
- [x] 6.10 确保 link 仅记录状态，不编辑链接的 repository/文件夹
- [x] 6.11 为 `workspace link` 添加 `--json` 输出

## 7. Workspace 重新链接

- [x] 7.1 实现 `openspec workspace relink <name> <path>`
- [x] 7.2 允许用户修复或更改现有链接的本地路径
- [x] 7.3 要求 relink 路径存在
- [x] 7.4 在存储本地状态之前，将相对 relink 路径解析为已验证的绝对运行时本地路径
- [x] 7.5 将所有者或交接元数据排除在此切片之外
- [x] 7.6 为 `workspace relink` 添加 `--json` 输出
- [x] 7.7 对未知链接名称返回清晰错误

## 8. Workspace 诊断

- [x] 8.1 实现 `openspec workspace doctor`，仅针对一个选定的 workspace
- [x] 8.2 显示 workspace 位置和 workspace planning 路径
- [x] 8.3 以可读的人工输出显示链接的 repository 或文件夹，并带有清晰的问题部分
- [x] 8.4 报告缺失的本地路径、缺失的文件系统路径、仅本地名称和选定 workspace 位置问题
- [x] 8.5 当 repository 本地的 `openspec/specs` 存在时报告 `repo_specs_path`，否则报告 `null`
- [x] 8.6 为每个问题包含建议的修复方法
- [x] 8.7 避免自动修复行为
- [x] 8.8 添加带有类型化 workspace/链接对象和结构化状态数组的 JSON 输出
- [x] 8.9 将过期的注册表清理命令（如 `workspace forget`）排除在此切片之外

## 9. 文档与指导

- [x] 9.1 以面向用户的产品语言记录 setup/list/link/relink/doctor
- [x] 9.2 记录链接的 repository 或文件夹以及大型单体 repository 文件夹链接
- [x] 9.3 记录 workspace 可见性不等同于变更承诺
- [x] 9.4 在面向用户的文档中避免使用"工作集"、"代码区域"、"条目"、"别名"和"本地覆盖"
- [x] 9.5 记录 JSON 输出支持以及用于非交互/直接命令的对象/状态响应 schema
- [x] 9.6 记录全局命令行为、workspace 选择器行为和 `--workspace <name>`
- [x] 9.7 记录 setup 控制 workspace 存储并始终显示 workspace 位置

## 10. 验证

- [x] 10.1 运行 `openspec validate workspace-create-and-register-repos --strict`
- [x] 10.2 运行针对 workspace setup/list/link/relink/doctor 的定向命令测试，包括 doctor 推断当前 workspace
- [x] 10.3 运行针对没有 repository 本地 OpenSpec 的链接和单体 repository 文件夹链接的定向测试
- [x] 10.4 运行针对 JSON 输出、`ls`、`.gitignore`、非交互式 setup、必需首个链接、已验证的绝对路径存储和 JSON/非交互式提示抑制的定向测试
- [x] 10.5 运行针对全局命令选择、未注册的当前 workspace 处理和本地 workspace 注册表行为的定向测试

## 11. 审查修复

- [x] 11.1 在推断的 setup 链接路径中保留 `=` 字符，同时保持显式的 `--link <name>=<path>` 支持
- [x] 11.2 添加可重用的核心辅助函数，用于可选的本地状态读取和 setup 链接输入解析
- [x] 11.3 当本地状态无效时，在变更之前使 `workspace link` 和 `workspace relink` 失败
- [x] 11.4 在 `workspace list` 和 `workspace doctor` 中清晰报告无效的本地状态
- [x] 11.5 为等号 setup 路径和格式错误的本地状态行为添加回归测试
