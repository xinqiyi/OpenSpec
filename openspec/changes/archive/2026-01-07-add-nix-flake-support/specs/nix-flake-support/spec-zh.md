## 新增的需求

### 需求：多平台 Nix flake

系统应提供一个 Nix flake，为多个平台构建 OpenSpec。

#### 场景：在 Linux x86_64 上构建
- **WHEN** 用户在 x86_64-linux 系统上运行 `nix build`
- **THEN** 系统成功构建 OpenSpec 包
- **AND** 包包含 `openspec` 二进制文件

#### 场景：在 macOS ARM 上构建
- **WHEN** 用户在 aarch64-darwin 系统上运行 `nix build`
- **THEN** 系统成功构建 OpenSpec 包
- **AND** 包包含 `openspec` 二进制文件

#### 场景：在 Linux ARM 上构建
- **WHEN** 用户在 aarch64-linux 系统上运行 `nix build`
- **THEN** 系统成功构建 OpenSpec 包

#### 场景：在 macOS x86_64 上构建
- **WHEN** 用户在 x86_64-darwin 系统上运行 `nix build`
- **THEN** 系统成功构建 OpenSpec 包

### 需求：通过 nix run 直接执行

系统应允许用户无需安装即可直接从 GitHub 运行 OpenSpec。

#### 场景：从 GitHub 运行 init 命令
- **WHEN** 用户运行 `nix run github:Fission-AI/OpenSpec -- init`
- **THEN** 系统下载并构建 OpenSpec
- **AND** 执行 `openspec init` 命令

#### 场景：运行任何 OpenSpec 命令
- **WHEN** 用户运行 `nix run github:Fission-AI/OpenSpec -- <command> <args>`
- **THEN** 系统执行 `openspec <command> <args>`

### 需求：pnpm 依赖管理

系统应在 Nix flake 中使用 pnpm 构建 OpenSpec。

#### 场景：使用 pnpm 获取依赖
- **WHEN** Nix 构建包时
- **THEN** 系统使用 `fetchPnpmDeps` 下载依赖
- **AND** 使用 pnpm-lock.yaml 实现可重复构建
- **AND** 对版本 9.0 的 lockfile 使用 fetcherVersion 3

#### 场景：使用 pnpm 构建
- **WHEN** Nix 运行构建阶段时
- **THEN** 系统执行 `pnpm run build`
- **AND** 生成包含编译后 TypeScript 的 dist 目录

### 需求：Node.js 版本兼容性

系统应使用 package.json engines 字段中指定的 Node.js 20。

#### 场景：使用正确的 Node 版本构建
- **WHEN** Nix 构建 OpenSpec
- **THEN** 系统使用来自 nixpkgs 的 nodejs_20
- **AND** 构建成功，无版本兼容性错误

### 需求：开发 shell

系统应为贡献者提供一个 Nix 开发 shell。

#### 场景：进入开发 shell
- **WHEN** 用户在 OpenSpec repository 中运行 `nix develop`
- **THEN** 系统提供包含 nodejs_20 和 pnpm_9 的 shell
- **AND** 显示带有版本信息的欢迎消息
- **AND** 提供运行 `pnpm install` 的说明

### 需求：正确的二进制安装

系统应正确安装 openspec 二进制文件。

#### 场景：二进制在 PATH 中
- **WHEN** 包已构建或安装
- **THEN** `openspec` 二进制文件在 `$out/bin/openspec` 中可用
- **AND** 二进制文件可执行
- **AND** 安装后无需完整路径即可调用二进制文件

#### 场景：二进制正确执行
- **WHEN** 用户运行已安装的 `openspec` 命令
- **THEN** 系统执行 CLI 入口点
- **AND** 所有子命令正常工作
