# 实现任务

## 阶段 1：基础和 Bash 支持

- [x] 更新 `src/utils/shell-detection.ts` 中的 `SupportedShell` 类型，包含 `'bash' | 'fish' | 'powershell'`
- [x] 扩展 shell 检测逻辑以从环境变量识别 bash、fish 和 PowerShell
- [x] 创建 `src/core/completions/generators/bash-generator.ts`，实现 `CompletionGenerator` 接口
- [x] 创建 `src/core/completions/installers/bash-installer.ts`，实现 `CompletionInstaller` 接口
- [x] 更新 `CompletionFactory.createGenerator()` 以支持 bash
- [x] 更新 `CompletionFactory.createInstaller()` 以支持 bash
- [x] 创建测试文件 `test/core/completions/generators/bash-generator.test.ts`，镜像 zsh 测试结构
- [x] 创建测试文件 `test/core/completions/installers/bash-installer.test.ts`，镜像 zsh 测试结构
- [x] 手动验证 bash 补全能正常工作：`openspec completion install bash && exec bash`

## 阶段 2：Fish 支持

- [x] 创建 `src/core/completions/generators/fish-generator.ts`，实现 `CompletionGenerator` 接口
- [x] 创建 `src/core/completions/installers/fish-installer.ts`，实现 `CompletionInstaller` 接口
- [x] 更新 `CompletionFactory.createGenerator()` 以支持 fish
- [x] 更新 `CompletionFactory.createInstaller()` 以支持 fish
- [x] 创建测试文件 `test/core/completions/generators/fish-generator.test.ts`
- [x] 创建测试文件 `test/core/completions/installers/fish-installer.test.ts`
- [x] 手动验证 fish 补全能正常工作：`openspec completion install fish`

## 阶段 3：PowerShell 支持

- [x] 创建 `src/core/completions/generators/powershell-generator.ts`，实现 `CompletionGenerator` 接口
- [x] 创建 `src/core/completions/installers/powershell-installer.ts`，实现 `CompletionInstaller` 接口
- [x] 更新 `CompletionFactory.createGenerator()` 以支持 powershell
- [x] 更新 `CompletionFactory.createInstaller()` 以支持 powershell
- [x] 创建测试文件 `test/core/completions/generators/powershell-generator.test.ts`
- [x] 创建测试文件 `test/core/completions/installers/powershell-installer.test.ts`
- [x] 在 Windows 或 macOS PowerShell 上手动验证 PowerShell 补全能正常工作

## 阶段 4：文档和测试

- [x] 更新 `CLAUDE.md` 或相关文档以提及所有四个受支持的 shell
- [x] 添加跨 shell 一致性测试，验证所有 shell 支持相同的命令
- [x] 运行 `pnpm test` 确保所有测试通过
- [x] 运行 `pnpm run build` 验证 TypeScript 编译
- [x] 在不同平台上测试所有 shell（Linux 用于 bash/fish/zsh，Windows/macOS 用于 PowerShell）

## 阶段 5：验证和清理

- [x] 运行 `openspec validate extend-shell-completions --strict` 并解决所有问题
- [x] 更新错误消息以列出所有四个受支持的 shell
- [x] 验证 `openspec completion --help` 文档是最新的
- [x] 测试自动检测对所有 shell 有效
- [x] 确保卸载对所有 shell 都能干净地工作
