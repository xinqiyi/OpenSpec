## 为什么

NixOS 或使用 Nix 包管理器的 OpenSpec 用户如果不通过 npm，无法轻松安装或运行 OpenSpec。添加 Nix flake 使 OpenSpec 成为 Nix 生态系统中的一等公民，使用户可以运行 `nix run github:Fission-AI/OpenSpec -- init` 或在开发环境中声明式地包含 OpenSpec。

## 变更内容

- 在 repository 根目录添加 `flake.nix`，支持多平台（x86_64-linux、aarch64-linux、x86_64-darwin、aarch64-darwin）
- 包使用 pnpm 进行依赖管理（匹配现有的开发 workflow）
- 支持通过 `nix run` 直接执行和通过 `nix profile install` 安装
- 为使用 Nix 的贡献者提供 dev shell

## 能力

### 新增能力
- `nix-flake-support`：用于构建和运行 OpenSpec 的 Nix flake 配置

### 修改的能力
- 无

## 影响

- **新文件**：repository 根目录中的 `flake.nix`
- **文档**：应为 Nix 用户添加安装说明
- **CI/CD**：可以向 CI 管道添加 flake 检查（可选）
- **维护**：依赖变更时需要更新 pnpmDeps 哈希
