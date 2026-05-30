## 上下文

OpenSpec 是一个使用 pnpm 进行依赖管理的 TypeScript CLI 工具。该项目需要 Node.js >=20.19.0。Nix 使用自己的构建系统，需要了解如何获取依赖并可重现地构建项目。

Nix 生态系统有特定的 schema 来打包 Node.js/pnpm 项目，这与传统的 npm 生态系统不同。

## 目标

- 使 OpenSpec 能通过 `nix run github:Fission-AI/OpenSpec` 直接运行
- 支持所有主要平台（Linux x86/ARM、macOS x86/ARM）
- 使用现有的 pnpm-lock.yaml 进行可重现构建
- 为 Nix 用户提供开发环境

## 非目标

- 替换现有的 npm/pnpm 发布 workflow
- 发布到 nixpkgs（可以在以后作为单独的工作进行）
- 支持 Windows（Nix 不在 Windows 上原生运行）

## 决策

### 使用 stdenv.mkDerivation 而非 buildNpmPackage

**决策**：使用带 pnpm hooks 的 `stdenv.mkDerivation` 打包 OpenSpec。

**理由**：nixpkgs 中的 zigbee2mqtt 包展示了当前 pnpm 项目的最佳实践。使用带 pnpm 的 `buildNpmPackage` 需要复杂的配置，而使用正确 hooks 的 `mkDerivation` 更直接且支持更好。

**考虑的替代方案**：使用带 `npmConfigHook = pkgs.pnpmConfigHook` 的 `buildNpmPackage` - 这是较旧的 schema，会导致依赖获取问题。

### 使用 fetchPnpmDeps 和显式 pnpm 版本

**决策**：使用 `pkgs.fetchPnpmDeps` 并设置 `pnpm = pkgs.pnpm_9` 和 `fetcherVersion = 3`。

**理由**：
- pnpm lockfile 版本 9.0 需要 fetcherVersion 3
- 显式的 pnpm_9 确保获取和构建之间的一致性
- 这是在 nixpkgs 中处理 pnpm 项目的文档化方式

### 无需 flake-utils 的多平台支持

**决策**：使用纯 Nix 配合 `nixpkgs.lib.genAttrs` 实现多平台支持。

**理由**：根据用户要求，避免额外依赖。`genAttrs` schema 在 Nix 社区中简单且广为人知。

### 使用 Node.js 20 而非最新版本

**决策**：锁定 nodejs_20 以匹配 package.json 的 engines 要求。

**理由**：确保与开发环境和 npm 包要求的一致性。避免与较新 Node 版本的潜在兼容性问题。

## 关键实现细节

### 依赖哈希管理

`pnpmDeps.hash` 字段必须在依赖变更时更新。workflow：
1. 将哈希设置为假值（全零）
2. 运行 `nix build`
3. Nix 失败并显示实际哈希
4. 使用正确的哈希更新 flake.nix

这是固定输出派生值的标准 Nix workflow。

### 构建输入

必需的 nativeBuildInputs：
- `nodejs_20` - 运行时
- `npmHooks.npmInstallHook` - 处理安装阶段
- `pnpmConfigHook` - 配置 pnpm 环境
- `pnpm_9` - pnpm 可执行文件

`dontNpmPrune = true` 对于在构建后保留所有依赖很重要。

## 风险/权衡

**[风险]** 依赖变更时需要更新哈希 → **缓解措施**：清晰记录；Nix 的错误消息提供正确的哈希

**[风险]** Nix 构建可能落后于 npm 发布 → **缓解措施**：这没问题；如果需要最新版本，Nix 用户仍可以使用 npm

**[权衡]** 哈希更新的额外维护负担 → **好处**：为 Nix 生态系统用户提供更好的体验

## 迁移计划

1. 向 repository 添加 flake.nix
2. 在多个平台上测试构建（可以使用带 Nix 的 GitHub Actions）
3. 使用 Nix 安装说明更新 README
4. 可选地添加到 CI 管道以尽早捕获哈希不匹配

无破坏性变更 - 这纯粹是附加性的。

## 开放问题

- 是否应该在 CI 中添加自动哈希更新？（可以使用 nix-update-script）
- 是否应该在验证后提交到 nixpkgs？（单独决策）
- 是否要在 flake 中支持较旧的 Node 版本？（可能不需要 - 遵循 package.json 要求）
