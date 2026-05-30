# ci-nix-validation spec

## 目的

在 CI 中验证 Nix flake 构建和维护脚本，以确保 Nix 用户可以可靠地安装和使用 OpenSpec。通过在每次拉取请求和推送到 main 时测试构建和 update-flake.sh 脚本，防止 Nix 支持出现回归。
## 需求
### 需求：Nix Flake 构建验证

CI 系统应在每次拉取请求和推送到 main 时验证 Nix flake 构建成功。

#### 场景：成功的 flake 构建

- **WHEN** 提交拉取请求或推送到 main 时
- **THEN** CI 应执行 `nix build` 并验证它以退出码 0 完成
- **AND** 构建输出应包含 openspec 二进制文件

#### 场景：Flake 构建失败

- **WHEN** Nix flake 配置损坏时
- **THEN** CI 作业应以非零退出码失败
- **AND** CI 应阻止合并该拉取请求

#### 场景：多平台支持检查

- **WHEN** flake 声明支持多个系统时
- **THEN** CI 应验证 flake 至少在 Linux（x86_64-linux）上构建

### 需求：更新脚本验证

CI 系统应验证 update-flake.sh 脚本成功执行并产生有效输出。

#### 场景：更新脚本执行

- **WHEN** CI 运行更新脚本验证时
- **THEN** 脚本应无错误执行
- **AND** 脚本应正确读取 package.json 中的版本
- **AND** 脚本应验证 flake.nix 使用来自 package.json 的动态版本

#### 场景：带模拟哈希的更新脚本

- **WHEN** 在 CI 中验证更新脚本时
- **THEN** 脚本应能够检测并提取正确的 pnpm 依赖哈希
- **AND** flake.nix 应使用有效的 sha256 哈希更新

### 需求：CI 作业集成

Nix 验证作业应集成到现有的 GitHub Actions workflow 中，并作为合并的必要条件。

#### 场景：PR 合并要求

- **WHEN** 创建拉取请求时
- **THEN** Nix 验证作业应包含在必要检查中
- **AND** 在 Nix 验证通过之前，PR 不应可合并

#### 场景：作业执行触发

- **WHEN** 代码推送到拉取请求或推送到 main 或手动触发时
- **THEN** Nix 验证作业应自动执行

### 需求：本地测试支持

CI workflow 应可使用 `act` 工具在本地进行测试，以实现快速迭代。

#### 场景：使用 act 本地执行 CI

- **WHEN** 开发者使用 Nix 验证 workflow 运行 `act`
- **THEN** workflow 应在本地 Docker 环境中执行
- **AND** 开发者应无需推送到 GitHub 即可收到关于 Nix 构建状态的反馈

#### 场景：Act 配置兼容性

- **WHEN** 设计 workflow 时
- **THEN** 应使用与 `act` 兼容的标准 GitHub Actions 语法
- **AND** 任何 Nix 特定的设置应在 act Docker 环境中正常工作

### 需求：CI 中的 Nix 安装

CI 环境在运行验证之前应正确安装和配置 Nix。

#### 场景：Nix 安装步骤

- **WHEN** Nix 验证作业启动时
- **THEN** 应使用官方 Nix 安装程序或 determinatesystems/nix-installer-action 安装 Nix
- **AND** 应缓存 Nix 安装以提高后续运行的性能

#### 场景：CI 的 Nix 配置

- **WHEN** Nix 在 CI 中安装时
- **THEN** 应配置为在 GitHub Actions 环境中工作
- **AND** 应启用实验性功能（flakes、nix-command）

### 需求：CI 性能优化

Nix 验证应进行优化，以最小化对 CI 运行时间的影响。

#### 场景：可接受的运行时间

- **WHEN** Nix 验证作业运行时
- **THEN** 全新运行应在 5 分钟内完成
- **AND** 使用缓存后，后续运行应在 3 分钟内完成

#### 场景：并行执行

- **WHEN** 多个 CI 作业同时运行时
- **THEN** Nix 验证作业应与其他验证作业（测试、lint）并行运行
- **AND** 不应阻塞其他独立检查
