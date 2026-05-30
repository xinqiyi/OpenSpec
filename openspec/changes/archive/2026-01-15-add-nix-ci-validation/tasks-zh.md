# 实施任务

## 1. 在 CI 中添加 Nix 安装

- [x] 1.1 调研 GitHub Actions 的 Nix 安装选项（nix-installer-action 与手动安装）
- [x] 1.2 在 .github/workflows/ci.yml 中添加 Nix 安装步骤
- [x] 1.3 配置 Nix 启用实验性功能（flakes、nix-command）
- [x] 1.4 添加 Nix 存储缓存以提升 CI 性能

## 2. 创建 Nix 构建验证任务

- [x] 2.1 在 .github/workflows/ci.yml 中添加新的 `nix-flake-validate` 任务
- [x] 2.2 实现带有适当错误处理的 `nix build` 步骤
- [x] 2.3 添加验证步骤，确认构建输出中存在二进制文件
- [x] 2.4 添加测试二进制执行的步骤（`nix run . -- --version`）

## 3. 添加更新脚本验证

- [x] 3.1 添加任务步骤，以 dry-run 或测试模式运行 scripts/update-flake.sh
- [x] 3.2 验证脚本无错误执行
- [x] 3.3 添加验证，确保从 package.json 正确提取版本号
- [x] 3.4 验证 flake.nix 以正确格式（版本和哈希）更新

## 4. 配置任务依赖和需求

- [x] 4.1 配置 Nix 验证任务在 pull_request 和 push 事件上运行
- [x] 4.2 将 Nix 验证添加到必需的检查列表
- [x] 4.3 配置任务与现有测试/代码检查任务并行运行
- [x] 4.4 设置适当的超时时间（5-10 分钟）

## 5. 使用 act 进行本地测试

- [x] 5.1 如果尚未安装，在本地安装 act
- [x] 5.2 使用 `act pull_request` 测试 Nix 验证任务
- [x] 5.3 验证 act 能够运行安装了 Nix 的工作流
- [x] 5.4 在 .actrc 或 README 中记录所需的 act 特定配置

## 6. 文档和收尾

- [x] 6.1 在 README 或 CONTRIBUTING.md 中添加关于 Nix CI 验证的文档
- [x] 6.2 记录如何使用 act 在本地测试 CI
- [ ] 6.3 如有需要，更新 CI 徽章或状态指示器
- [ ] 6.4 通过创建测试 PR 进行端到端测试

## 7. 归档变更

- [x] 7.1 合并并验证后，在 openspec/specs/ci-nix-validation/spec.md 创建新的规范文件
- [x] 7.2 将变更目录移动到 openspec/changes/archive/[date]-add-nix-ci-validation/
- [x] 7.3 运行 `openspec validate --strict` 确认归档的变更通过验证
