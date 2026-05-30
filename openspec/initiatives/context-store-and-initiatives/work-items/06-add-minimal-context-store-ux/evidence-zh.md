# 添加最小上下文存储 UX 证据

## 对话决策

- 下一个路线图步骤不应直接跳到 repository 本地变更关联或 workspace 倡议打开。
- 团队首先需要一个简单的方法来创建或注册持有倡议的共享上下文存储。
- workflow 是 agent 优先的：用户向 agent 发出提示，agent 使用 CLI 原语来发现存储和倡议。
- `context-store` 目前应是顶级命令命名空间。对于 agent 来说，它比 `store` 更明确，而 `store` 可以作为作用域标志中的简写，例如 `initiative list --store <id>`。
- 存储可以作为一个本地 Git 支持的文件夹开始。OpenSpec 可以帮助创建文件夹、写入元数据、在本地注册，并可选择初始化 Git。
- 当设置未收到 `--path` 时，应创建或使用 `./<id>`。这使真正的共享存储保持可见，避免了将其隐藏在全局数据下。
- 使用当前目录需要显式的 `--path .`。
- 如果用户注册现有文件夹或克隆，默认存储 ID 可以是 repository 或文件夹名称。
- 可移植的 `.openspec-store/store.yaml` 元数据应被检入，且不应包含本地路径。
- `.openspec-store/store.yaml` 本身就是标识文件，而不是另一个已检入元数据文件旁边的捆绑包。目前它应仅包含 `version` 和 `id`。
- 未来的后端、同步、集合、权限或策略配置默认不应添加到 `store.yaml` 中。
- 本地注册表将存储 ID 映射到一台机器上的本地路径。
- 远程 URL 克隆/设置糖语法虽有用但可以等待。
- `initiative list` 默认应列出所有已注册的存储；`--store` 应进行过滤。
- 交互式设置应提示 Git 初始化，并在未提供显式 Git 标志时默认选择是。
- 非交互式、JSON、`--init-git` 和 `--no-init-git` 设置不应提示。
- `context-store register` 对于相同的 ID/路径应是幂等的，对于相同 ID 但不同路径应失败，直到未来有显式的替换选项。
- `context-store list` 应保持简单的注册表索引，不应显示健康警告。
- `context-store doctor` 拥有健康诊断。第一个切片应检查注册表/路径/元数据和简单的 Git repository 存在性，不检查脏状态、分支、远程、同步、拉取/推送或冲突。
- `initiative list` 应在全存储 schema 下允许部分成功：显示可读存储中的倡议，并在其他已注册存储无法读取时打印一条指向 `context-store doctor` 的小警告。
- 过滤后的 `initiative list --store` 和显式的 `--store-path` 在所选存储无法读取时应直接失败。
- 部分成功应以退出码 0 退出，并在 JSON 中包含警告诊断。完全失败应以非零退出码退出。
- 注册 ID 推断应直接使用 repository/文件夹名称，并进行正常的上下文存储 ID 验证。在此切片中不添加 spec 化。
- 设置目前应拒绝没有上下文存储元数据的非空文件夹。
- 注册表冲突应在相同 ID 指向不同路径或相同路径已以不同 ID 注册时失败。
- 空状态应保持简单：`context-store list` 和 `doctor` 显示未注册存储；`initiative list` 显示未找到倡议，因为没有存储已注册。
- 静态 shell 补全元数据现在是已发布的命令表面的一部分；动态存储 ID 和倡议 ID 补全仍被推迟。

## 实施前需要检查的风险

- 现有的命令命名约定可能偏好动词优先的流程，而 context-store 命令自然是以名词命名空间的。
- Shell 补全是手动注册的；将未来的命令添加保持在 `src/core/completions/command-registry.ts` 中，并配合有针对性的注册测试。
- 人类输出应与现有的紧凑 CLI 输出 schema 匹配。
- JSON 输出应足够稳定以供 agent 使用，同时不过度建模未来的同步或远程行为。

## 实施证据

- `src/commands/context-store.ts` 添加了 `context-store` 命令命名空间，包含 setup、register、list 和 doctor 子命令。
- `src/cli/index.ts` 注册了 context-store 命令。
- `src/commands/context-store.ts` 在命令层保持严格的 CLI 设置/注册策略，同时重用 context-store 基础助手。
- `src/commands/initiative.ts` 现在让 `initiative list` 默认搜索所有已注册的存储，保留 `--store` 作为过滤器，保持 `--store-path`，并通过警告诊断报告全存储部分成功。
- `src/core/completions/command-registry.ts` 为 context-store 命令表面注册静态补全元数据。
- `test/commands/context-store.test.ts` 涵盖 setup、register、list、doctor、冲突处理、非空设置拒绝和交互式 Git 初始化。
- `test/commands/initiative.test.ts` 涵盖全存储倡议列表、紧凑人类输出、空已注册存储状态、部分成功和所有存储不可读。

## 验证

- `pnpm run build`
- `pnpm exec vitest run test/commands/context-store.test.ts test/commands/initiative.test.ts`
- `pnpm exec vitest run test/core/context-store/foundation.test.ts
 test/core/context-store/registry.test.ts
 test/core/collections/initiatives/operations.test.ts`
- `pnpm run lint`
