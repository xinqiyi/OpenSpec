## 原因

最近的跨 shell 回归问题揭示了 `openspec` 命令的现有单元/集成测试未对打包后的 CLI 或特定 shell 行为进行测试。先前尝试 Vitest spawn 测试因将 e2e 覆盖与 `pnpm pack` 安装耦合而受阻，这在网络受限环境中会失败。结合这些发现，我们现在需要一个已批准的计划来重新调整工作。

## 变更内容

- 采用分阶段策略，首先通过轻量级固定装置和共享的 `runCLI` 辅助程序，使构建后的 CLI（`node dist/cli/index.js`）的直接 spawn 测试稳定。
- 一旦 spawn 测试框架稳定，扩展覆盖范围，保持初始矩阵专注于 Linux/macOS 上的 bash 作业和 Windows 上的 `pwsh`，同时同时测试直接 `node dist/cli/index.js` 调用和 bin shim，使用非 TTY 默认值和捕获的诊断信息。
- 将打包/安装验证视为可选的 CI 安全措施：当运行器具有注册表访问权限时，运行简单的基于 pnpm 的 pack->install->smoke-test 流程；否则，将其记录为范围外，同时完成剩余的加固项。
- 完成剩余的跨 shell 加固项：确保 `.gitattributes` 覆盖打包资源，在 CI 期间强制执行 CLI shim 的可执行位，并完成待处理的 SIGINT 处理改进。

## 影响范围

- 测试：添加 `test/cli-e2e` spawn 套件，创建共享的 `runCLI` 辅助程序，并根据需要调整 `vitest.setup.ts`。
- 工具：使用上述轻量级矩阵更新 GitHub Actions 工作流，并在网络可用时（可选）添加打包安装检查。
- 文档：在此提案（或相关规范）中内联记录阶段进展和任何限制，以便未来阶段有清晰的上下文。

### 阶段 1 状态

- 共享的 `test/helpers/run-cli.ts` 保证 CLI 包在 spawn 之前存在，并对每次调用强制执行非 TTY 默认值。
- 新的 `test/cli-e2e/basic.test.ts` 覆盖了 `--help`、`--version`、成功的 `validate --all --json` 以及针对 `tmp-init` 固定装置副本的未知项错误路径。
- 旧版顶级 `validate` exec 测试现在依赖 `runCLI`，避免手动使用 `execSync`，同时保持其固定装置编写不变。
- CI 矩阵基础工作已就绪（Linux/macOS 上的 bash，Windows 上的 pwsh），因此 spawn 套件在支持的 shell 中以与辅助程序相同的方式运行。
