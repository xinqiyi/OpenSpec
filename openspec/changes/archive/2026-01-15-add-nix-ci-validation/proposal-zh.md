# 添加 Nix CI 验证

## 原因

项目最近添加了 Nix flake 支持（flake.nix）和一个自动化更新脚本（scripts/update-flake.sh），使 Nix 用户能够安装 OpenSpec。然而，没有 CI 验证来确保这些 Nix 工件在项目演进过程中持续工作。这带来了破坏性变更可能在未被检测到的情况下合并的风险。

## 变更内容

- 添加一个新的 GitHub Actions 工作流任务，验证 Nix flake 构建成功
- 添加对 update-flake.sh 脚本无错误执行的验证
- 在 Linux 上测试（Nix 支持最常见的平台）
- 确保如果 Nix 构建或更新脚本损坏，CI 会失败
- 支持开发者使用 `act` 进行本地测试

## 影响

- 受影响的规范：新能力 `ci-nix-validation`
- 受影响的代码：`.github/workflows/ci.yml`（添加新任务）
- 受影响的基础设施：安装了 Nix 的 GitHub Actions 运行器
- 好处：防止 Nix 支持退化，给 Nix 用户带来信心
- 权衡：CI 运行时间增加约 2-3 分钟
