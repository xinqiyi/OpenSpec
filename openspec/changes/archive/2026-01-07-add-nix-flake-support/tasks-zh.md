## 1. 创建 Flake 结构

- [x] 1.1 在 repository 根目录创建 flake.nix
- [x] 1.2 定义 inputs（仅 nixpkgs，无 flake-utils）
- [x] 1.3 设置 supportedSystems 列表（4 个平台）
- [x] 1.4 创建 forAllSystems 辅助函数

## 2. 配置包构建

- [x] 2.1 使用 finalAttrs schema 设置 stdenv.mkDerivation
- [x] 2.2 使用 fetchPnpmDeps 配置 pnpmDeps
- [x] 2.3 设置 pnpm = pnpm_9 和 fetcherVersion = 3
- [x] 2.4 添加占位哈希（全零）
- [x] 2.5 配置 nativeBuildInputs（nodejs_20、hooks、pnpm_9）
- [x] 2.6 设置 dontNpmPrune = true

## 3. 定义构建阶段

- [x] 3.1 添加带 runHook preBuild 的 buildPhase
- [x] 3.2 添加 pnpm run build 命令
- [x] 3.3 添加 runHook postBuild

## 4. 配置安装

- [x] 4.1 让 npmInstallHook 自动处理安装
- [x] 4.2 验证二进制文件在 $out/bin/openspec 中

## 5. 添加元数据

- [x] 5.1 设置 meta.description
- [x] 5.2 设置 meta.homepage
- [x] 5.3 设置 meta.license（MIT）
- [x] 5.4 设置 meta.mainProgram = "openspec"

## 6. 配置应用入口点

- [x] 6.1 添加带 forAllSystems 的 apps 输出
- [x] 6.2 将默认应用设置为 openspec 二进制文件
- [x] 6.3 测试 nix run 是否有效

## 7. 添加开发 Shell

- [x] 7.1 添加带 forAllSystems 的 devShells 输出
- [x] 7.2 在 buildInputs 中包含 nodejs_20 和 pnpm_9
- [x] 7.3 添加带欢迎消息和说明的 shellHook

## 8. 获取正确的依赖哈希

- [x] 8.1 运行 nix build 触发哈希不匹配
- [x] 8.2 从错误消息中复制正确的哈希
- [x] 8.3 更新 flake.nix 中的 pnpmDeps.hash
- [x] 8.4 验证构建成功

## 9. 测试

- [x] 9.1 在 x86_64-linux 上测试 `nix build`
- [x] 9.2 测试 `nix run . -- --version` 有效
- [x] 9.3 测试 `nix develop` 提供正确的环境
- [ ] 9.4 在 macOS 上测试（如果有条件）
- [ ] 9.5 合并到主分支后测试 `nix run github:Fission-AI/OpenSpec -- init`

## 10. 文档

- [x] 10.1 在 README 中添加 Nix 安装部分
- [x] 10.2 在 README 中包括常见 Nix workflow 的示例命令
