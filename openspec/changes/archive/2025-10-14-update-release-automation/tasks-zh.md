## 1. 发布 workflow 自动化
- [x] 1.1 添加 `.github/workflows/release.yml`，在推送到 `main` 时运行，设置 pnpm + Node 20，安装依赖，并使用 `publish: pnpm run release` 调用 `changesets/action@v1`。
- [x] 1.2 使用 `createGithubReleases: true` 配置操作，记录必需的密钥（`NPM_TOKEN`、默认 `GITHUB_TOKEN`）以及建议的并发安全措施。
- [x] 1.3 使用 `act` 或干运行推送验证 workflow，确认当 changesets 存在时操作会打开发布 PR，当发布 PR 合并时发布。

## 2. 包发布脚本
- [x] 2.1 在 `package.json` 中添加 `release` 脚本，构建项目并使用 pnpm 运行 `changeset publish`。
- [x] 2.2 确保脚本尊重现有的 `prepare`/`prepublishOnly` 钩子，避免重复构建，如果需要调整则更新文档或脚本。

## 3. 文档和恢复步骤
- [x] 3.1 更新维护者文档（例如 README 或 `/docs`），包含端到端的自动化发布流程，明确移除不再需要的手动标签/发布步骤，并解释 changesets 如何驱动发布 PR。
- [x] 3.2 记录发布失败的回退步骤（重新运行 workflow、手动发布）以及在无待处理 changesets 时需要发布的热修复路径。
