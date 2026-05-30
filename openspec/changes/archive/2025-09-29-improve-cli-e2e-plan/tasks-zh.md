## 1. 阶段 1 — 稳定本地 Spawn 覆盖
- [x] 1.1 添加 `test/helpers/run-cli.ts`，确保构建运行一次并使用非 TTY 默认值执行 `node dist/cli/index.js`；更新 `vitest.setup.ts` 以重用共享构建步骤。
- [x] 1.2 使用最小固定装置集（`tmp-init` 或副本）初始化 `test/cli-e2e`，以通过新辅助程序覆盖 help/version、正常的 `validate` 路径以及代表性错误流程。
- [x] 1.3 将最高价值的现有 CLI exec 测试（例如 validate）迁移到 `runCLI`，并在本提案中总结阶段 1 覆盖范围以供下一阶段使用。

## 2. 阶段 2 — 扩展跨 Shell 验证
- [x] 2.1 在 spawn 套件中测试两个入口点（`node dist/cli/index.js`、`bin/openspec.js`），并为 shell/OS 上下文添加诊断信息。
- [x] 2.2 扩展 GitHub Actions 以在 Linux/macOS 的 bash 作业和 Windows 的 `pwsh` 作业上运行 spawn 套件；捕获 shell/OS 诊断信息，并记录其他 shell 的后续工作。
