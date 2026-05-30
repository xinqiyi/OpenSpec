# OpenSpec 脚本

用于 OpenSpec 维护和开发的实用脚本。

## update-flake.sh

自动更新 `flake.nix` pnpm 依赖哈希。

**使用时机**：更新依赖后（`pnpm install`, `pnpm update`）。

**用法**：
```bash
./scripts/update-flake.sh
```

**功能说明**：
1. 从 `package.json` 读取版本（由 `flake.nix` 动态使用）
2. 自动确定正确的 pnpm 依赖哈希
3. 更新 `flake.nix` 中的哈希
4. 验证构建是否成功

**示例工作流**：
```bash
# 依赖更新后
pnpm install
./scripts/update-flake.sh
git add flake.nix
git commit -m "chore: update flake.nix dependency hash"
```

## postinstall.js

包安装后执行的安装后脚本。

## pack-version-check.mjs

在发布前验证包版本一致性。
