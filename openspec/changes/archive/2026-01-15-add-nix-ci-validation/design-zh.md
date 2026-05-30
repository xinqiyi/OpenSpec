# 设计：Nix CI 验证

## 上下文

OpenSpec 最近添加了 Nix flake 支持，使 Nix 用户能够安装该工具。这包括：
- `flake.nix`：包含 pnpm 依赖获取的 Nix 包定义
- `scripts/update-flake.sh`：用于在发布时更新版本和哈希的自动化脚本

目前，没有 CI 验证来确保这些 Nix 工件保持可用。现有的 CI 工作流（.github/workflows/ci.yml）验证多个平台（Linux、macOS、Windows）上的 Node.js 构建、测试和代码检查，但不验证 Nix 构建。

**利益相关者**：Nix 用户、维护者、需要确信 Nix 支持有效的贡献者。

**约束条件**：
- 必须在 GitHub Actions Linux 运行器中工作
- 应最小化 CI 运行时间影响（增加少于 5 分钟）
- 应支持使用 `act` 进行本地测试以实现快速迭代
- 必须与现有的必需检查集成

## 目标 / 非目标

**目标**：
- 验证每个 PR/推送上的 `nix build` 是否成功
- 验证 `scripts/update-flake.sh` 无错误执行
- 确保 Nix 支持不会无意中退化
- 支持使用 `act` 进行本地测试
- 使用缓存优化以最小化 CI 时间

**非目标**：
- 在 macOS 上测试（GitHub 托管的 macOS 运行器更慢且更昂贵；Nix flake 已声明支持 macOS）
- 为所有声明的系统（x86_64-linux、aarch64-linux、x86_64-darwin、aarch64-darwin）构建——专注于最常见的平台
- 验证 Nix flake 质量/风格（nixpkgs-fmt 等）——如有需要可后续添加
- 通过 Nix 构建运行 OpenSpec 的完整测试套件——现有 CI 已经完成此工作

## 决策

### 决策 1：使用 DeterminateSystems nix-installer-action

**内容**：使用 `determinatesystems/nix-installer-action` 在 CI 中安装 Nix。

**原因**：
- 由 Determinate Systems（Nix 专家）维护的官方 GitHub Action
- 自动处理 GitHub Actions 环境问题
- 包含自动缓存配置
- 比 curl | sh 安装脚本更可靠
- 更好的错误消息和诊断

**考虑的替代方案**：
- 官方 Nix 安装程序（`curl -L https://nixos.org/nix/install | sh`）：可用，但需要手动设置 flakes、缓存和 CI 特定配置
- `cachix/install-nix-action`：流行的替代方案，但 determinatesystems 维护更积极，GHA 集成更好

### 决策 2：使用 Magic Nix Cache 提升性能

**内容**：使用 `determinatesystems/magic-nix-cache-action` 实现自动二进制缓存。

**原因**：
- Nix 存储的零配置缓存
- 显著减少后续运行的 CI 时间（从约 5 分钟减少到约 1-2 分钟）
- 对公共仓库免费
- 自动处理缓存键

**考虑的替代方案**：
- 使用 GitHub Actions 缓存进行手动 Nix 存储缓存：更复杂，需要手动缓存键管理
- Cachix：优秀的工具，但需要账户设置和令牌管理
- 无缓存：初始实施可以接受，但开发者体验较差

### 决策 3：Nix 验证独立任务

**内容**：在 .github/workflows/ci.yml 中创建一个专用的 `nix-validate` 任务，与其它任务并行运行。

**原因**：
- 将 Nix 验证与 Node.js 验证隔离
- 允许并行执行以加快 CI
- 在出现 Nix 特定问题时更容易调试
- 可以独立标记为必需检查

**考虑的替代方案**：
- 向现有任务添加 Nix 步骤：导致 Node.js 和 Nix 验证之间的耦合，更难维护
- 单独的工作流文件：对于单个任务来说过于复杂，更难管理必需检查

### 决策 4：通过执行脚本来验证更新脚本

**内容**：将 `scripts/update-flake.sh` 作为 CI 验证的一部分运行。

**原因**：
- 确保脚本不会因 package.json 格式、nix 构建输出或依赖项的更改而损坏
- 测试用户在发布时将遵循的完整工作流
- 及早发现错误

**实施方法**：
- 以不修改 git 状态的方式执行脚本（或之后丢弃更改）
- 验证脚本以代码 0 退出
- 可选地，验证执行后 flake.nix 包含预期的模式

**考虑的替代方案**：
- 模拟/dry-run 模式：需要大幅修改脚本
- 跳过验证：有风险——脚本可能损坏且仅在发布时被发现
- 仅在发布分支上运行：错过开发早期的问题

### 决策 5：在 pull_request 和推送到 main 时运行

**内容**：配置 Nix 验证任务在以下事件上运行：
- `pull_request` 事件（任何针对 main 的 PR）
- `push` 事件（直接推送到 main）
- `workflow_dispatch`（用于测试的手动触发）

**原因**：
- 在合并前发现问题（pull_request）
- 验证 main 分支保持健康（push）
- 允许手动测试而无需创建 PR（workflow_dispatch）

### 决策 6：支持 act 进行本地测试

**内容**：确保工作流与 `act` 工具兼容，用于本地 CI 测试。

**原因**：
- 在开发 CI 变更时更快迭代
- 允许在不推送到 GitHub 的情况下进行测试
- 减少来自 CI 调试的提交噪音

**要求**：
- 使用标准的 GitHub Actions 语法
- 记录所需的任何 act 特定配置
- 测试 Nix 能否在 act 的 Docker 容器中安装

**限制**：
- act 可能无法完美复制 GitHub 的运行器，但足够接近验证目的

## 风险 / 权衡

### 风险：CI 运行时间增加

**影响**：添加 Nix 验证将使每次运行的总 CI 时间增加 2-5 分钟。

**缓解措施**：
- 使 Nix 任务与现有任务并行运行（无阻塞延迟）
- 对后续运行使用 magic-nix-cache（带缓存约 1-2 分钟）
- 配置适当的超时时间（最长 10 分钟）

**接受程度**：防止 Nix 退化带来的好处超过了成本。

### 风险：CI 中 Nix 安装失败

**影响**：Nix 安装的瞬时故障可能阻止 PR。

**缓解措施**：
- 使用具有重试逻辑的 determinatesystems action
- 监控不稳定故障并根据需要调整
- 记录故障排除步骤

**接受程度**：Nix 安装通常在 GHA 中稳定；风险较低。

### 风险：更新脚本修改 git 状态

**影响**：运行 update-flake.sh 会修改 flake.nix，如果检查 git 状态，可能导致 CI 失败。

**缓解措施**：
- 在隔离环境中运行脚本，不提交更改
- 验证后添加 `git checkout -- flake.nix`
- 或接受 CI 中的脏 git 状态（不影响构建验证）

**接受程度**：脚本验证足够重要，值得谨慎处理。

### 风险：act 兼容性问题

**影响**：由于 Docker 环境差异，工作流可能无法与 act 完美配合。

**缓解措施**：
- 记录已知限制
- 将 GitHub Actions 作为主要验证目标
- 将 act 用作尽力而为的本地测试

**接受程度**：act 支持是可选的，非必需。

## 迁移计划

### 阶段 1：添加 Nix 任务（新的，非必需）
1. 在 .github/workflows/ci.yml 中添加 `nix-validate` 任务
2. 配置为与现有任务并行运行
3. 初始不标记为必需检查
4. 监控约 1 周以确保稳定性

### 阶段 2：设为必需
1. 验证稳定后，添加到必需检查
2. 在 GitHub 设置中更新分支保护规则
3. 在 CONTRIBUTING.md 或 README 中记录

### 回滚计划
如果 Nix 验证导致问题：
1. 从 GitHub 设置的必需检查中移除任务（立即）
2. 注释掉或从工作流中移除任务（永久修复）
3. 调查并修复问题
4. 按照相同的分阶段方法重新启用

## 未决问题

- **问**：是否应在每次 CI 运行时测试 update-flake.sh，还是仅在 package.json 或 pnpm-lock.yaml 更改时测试？
  - **答**：为简单起见，在每次运行时测试。脚本执行速度快（少于 30 秒），且捕获回归问题很有价值。

- **问**：是否也应在 macOS 上进行验证？
  - **答**：初始实施不需要。Linux 验证已足够，macOS 运行器更慢且更昂贵。如果用户报告 macOS 特定问题，可以后续添加。

- **问**：是否应通过 Nix 构建运行完整的 OpenSpec 测试？
  - **答**：不需要。Nix 构建已在其构建阶段运行 `pnpm test`。现有 CI 任务已充分覆盖测试。Nix 验证专注于构建成功。

- **问**：Nix 验证任务应使用什么超时时间？
  - **答**：从 10 分钟开始。使用缓存时，任务应在 1-3 分钟内完成。无缓存（首次运行）时，预计 5-7 分钟。
