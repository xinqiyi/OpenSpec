## 为什么

维护 Nix flake 需要在发布新版本或更新依赖时手动更新版本和依赖哈希。这容易出错，并且要求维护者理解 Nix 内部细节。自动化此过程可确保一致性，并减少发布的阻力。

## 变更内容

- 添加 `scripts/update-flake.sh` 以自动更新 flake.nix 版本和依赖哈希
- 添加 `scripts/README.md` 记录所有维护脚本
- 脚本自动从 package.json 提取版本并确定正确的 pnpm 依赖哈希

## 能力

### 新增能力
- `flake-update-script`：维护 flake.nix 的自动化脚本

### 修改的能力
- 无

## 影响

- **新文件**：`scripts/update-flake.sh`、`scripts/README.md`
- **维护者工作流**：版本升级现在包括运行 `./scripts/update-flake.sh`
- **依赖**：脚本需要 Node.js（已是依赖）和 Nix（适用于使用 Nix 的维护者）
