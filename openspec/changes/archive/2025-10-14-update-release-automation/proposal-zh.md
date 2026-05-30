## 为什么
当前流程要求维护者合并 Changesets PR、手动创建标签并起草 GitHub 发布。在现有工作流中，npm 发布在 GitHub 发布后运行。人工参与的步骤（版本控制、打标签、发布说明）拖慢了我们的速度，并导致 npm、标签和变更日志之间出现偏差风险。

## 变更内容
- 在推送到 `main` 时使用单一的 `changesets/action`，要么打开/更新版本 PR，要么在发布 PR 合并时使用仓库密钥自动运行发布命令。
- 添加构建并运行 `changeset publish` 的 `release` 脚本，使操作端到端地处理版本升级、变更日志提交、npm 发布和 GitHub 发布。
- 启用 `createGithubReleases: true`，以便在发布后立即根据 changeset 数据创建 GitHub 发布。
- 记录自动化流程、必需的密钥、安全措施和恢复步骤（回滚、热修复）。

## 两阶段推出（两个 PR）
1) 阶段 1 — 干运行（不发布）
   - 更新现有的 `release-prepare.yml`，连接 `changesets/action`，使用 `createGithubReleases: true` 和空操作 `publish` 命令（例如 `echo 'dry run'`）。
   - 保持 `.github/workflows/release-publish.yml` 不变。这避免了在验证版本 PR 行为和权限正确性时更改发布路径。
   - 添加仓库保护（`if: github.repository == 'Fission-AI/OpenSpec'`）和并发组以确保安全。

2) 阶段 2 — 启用发布并整合
   - 在 `package.json` 中添加 `"release": "pnpm run build && pnpm exec changeset publish"`。
   - 修改 `release-prepare.yml`，使用 `with: publish: pnpm run release` 和 `env: NPM_TOKEN: \${{ secrets.NPM_TOKEN }}` 以及默认的 `GITHUB_TOKEN`。
   - 移除 `.github/workflows/release-publish.yml` 以避免重复发布。现在当版本 PR 合并时进行发布。

## 安全措施
- 并发：工作流上使用 `concurrency: { group: release-\${{ github.ref }}, cancel-in-progress: false }` 来序列化发布。
- 仓库/分支保护：仅在上游 `main` 上运行发布逻辑（`if: github.repository == 'Fission-AI/OpenSpec' && github.ref == 'refs/heads/main'`）。
- 权限：确保 `contents: write` 和 `pull-requests: write` 用于打开/更新版本 PR；`packages: read` 可选。

## 回滚和热修复
- 回滚：撤销发布 PR 的合并（撤销版本升级/变更日志）；如果已创建标签或 GitHub 发布，删除标签和发布；如有必要，弃用 npm 版本（`npm deprecate @fission-ai/openspec@x.y.z 'reason'`）。
- 热修复（紧急情况，无待处理的 changesets）：为修复创建 changeset 并合并发布 PR；在紧急情况下，运行手动版本升级/发布，但通过添加后续 changeset 对齐版本以与 Changesets 保持一致。

## 必需的密钥
- 具有 `@fission-ai` 范围发布权限的 `NPM_TOKEN`。
- 用于打开/更新版本 PR 和创建 GitHub 发布的默认 `GITHUB_TOKEN`（由 GitHub 提供）。

## 维护者流程的变化
| 步骤 | 当前流程 | 未来流程 |
| --- | --- | --- |
| 准备发布 | 合并 changeset PR，然后手动起草发布说明和标签 | 合并发布 PR；操作自动更新版本和处理变更日志 |
| 发布 npm 包 | 在 GitHub 发布后自动进行 | 通过操作调用的 `changeset publish` 自动进行 |
| GitHub 发布 | 手动起草并与变更日志同步 | 操作根据 changeset 数据创建 GitHub 发布 |
| 文档/流程 | 遵循手动打标签/发布步骤 | 文档描述自动化流程 + 恢复和热修复路径 |

## 影响
- 自动化：重用 `.github/workflows/release-prepare.yml`（阶段 1：干运行，阶段 2：发布）并在阶段 2 中移除 `.github/workflows/release-publish.yml`。
- 包元数据：在 `package.json` 中添加 `release` 脚本。
- 文档：更新 README 或 `/docs` 以显示自动化流程、密钥、安全措施和恢复步骤。

## 验收标准
- 阶段 1：合并到 `main` 会打开/更新版本 PR；合并时，操作的 `publish` 步骤是空操作；不进行 npm 发布；日志确认预期行为；GitHub 发布创建已连接但由于没有发布而处于非活动状态。
- 阶段 2：合并到 `main` 会从操作运行 `pnpm run release`；npm 包成功发布；自动创建 GitHub 发布；`.github/workflows/release-publish.yml` 被移除；不会发生重复发布。
