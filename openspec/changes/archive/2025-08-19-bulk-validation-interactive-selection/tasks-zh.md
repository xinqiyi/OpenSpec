# 实施任务

## 1. 变更命令：交互式验证选择
- [x] 1.1 在 `src/cli/index.ts` 中为 `change validate` 添加 `--no-interactive` 标志
- [x] 1.2 在 `src/commands/change.ts` 中实现交互性开关，遵循 TTY 和 `OPEN_SPEC_INTERACTIVE=0`
- [x] 1.3 当未提供 `[change-name]` 且允许交互时，显示活跃变更列表（排除 `archive/`）并验证所选变更
- [x] 1.4 保留当前非交互式回退：打印可用变更 ID 和提示，设置 `process.exitCode = 1`
- [x] 1.5 测试：为交互式和非交互式流程添加覆盖
 - 已添加 `test/commands/change.interactive-validate.test.ts`

## 2. spec 命令：交互式验证选择
- [x] 2.1 使 `spec validate` 在 `src/commands/spec.ts` 注册中接受可选的 `[spec-id]`
- [x] 2.2 为 `spec validate` 添加 `--no-interactive` 标志
- [x] 2.3 实现交互性开关，遵循 TTY 和 `OPEN_SPEC_INTERACTIVE=0`
- [x] 2.4 当未提供 `[spec-id]` 且允许交互时，提示从 `openspec/specs/*/spec.md` 中选择并验证所选 spec
- [x] 2.5 当无 spec-id 且无交互时保留当前非交互式回退：打印现有错误并以非零退出码退出
- [x] 2.6 测试：为交互式和非交互式流程添加覆盖
 - 已添加 `test/commands/spec.interactive-validate.test.ts`

## 3. 新的顶级 `validate` 命令
- [x] 3.1 在 `src/cli/index.ts` 中添加 `validate` 命令
 - 选项：`--all`、`--changes`、`--specs`、`--type <change|spec>`、`--strict`、`--json`、`--no-interactive`
 - 用法：`openspec validate [item-name]`
- [x] 3.2 创建 `src/commands/validate.ts` 实现：
 - [x] 3.2.1 无参数时的交互式选择器（选项：全部、变更、spec、特定项目）
 - [x] 3.2.2 带帮助提示和退出码 1 的非交互式回退
 - [x] 3.2.3 带自动类型检测的直接项目验证
 - [x] 3.2.4 当名称同时作为变更和 spec 存在时的歧义错误；建议使用 `--type` 或子命令
 - [x] 3.2.5 未知项目处理，提供最接近匹配的建议
 - [x] 3.2.6 `--all`、`--changes`、`--specs` 的批量验证（排除 `openspec/changes/archive/`）
 - [x] 3.2.7 遵循 `--strict` 和 `--json` 选项；JSON 格式符合 spec
 - [x] 3.2.8 如果任何验证失败，以退出码 1 退出
 - [x] 3.2.9 批量验证的有界并发（默认 4-8）
 - [x] 3.2.10 批量运行期间的进度指示（当前项目、运行计数）

## 4. 工具和共享辅助函数
- [x] 4.1 添加 `src/utils/interactive.ts`，包含 `isInteractive(stdin: NodeJS.ReadStream, noInteractiveFlag?: boolean): boolean`
 - 考虑：`process.stdin.isTTY`、`--no-interactive`、`OPEN_SPEC_INTERACTIVE=0`
- [x] 4.2 添加 `src/utils/item-discovery.ts`，包含：
 - `getActiveChangeIds(root = process.cwd()): Promise<string[]>`（排除 `archive/`）
 - `getSpecIds(root = process.cwd()): Promise<string[]>`（包含 `spec.md` 的文件夹）
- [ ] 4.3 可选：`src/utils/concurrency.ts` 有界并行辅助函数
- [x] 4.4 复用 `src/core/validation/validator.ts` 进行项目验证

## 5. JSON 输出（批量验证）
- [x] 5.1 实现 JSON schema：
 - `items: Array<{ id: string, type: "change"|"spec", valid: boolean, issues: Issue[], durationMs: number }>`
 - `summary: { totals: { items: number, passed: number, failed: number }, byType: { change?: { items: number, passed: number, failed: number }, spec?: { items: number, passed: number, failed: number } } }`
 - `version: "1.0"`
- [x] 5.2 确保如果任何 `items[].valid === false`，进程退出码为 1
- [x] 5.3 JSON 形状（键、类型、计数）和退出码行为的测试
 - 已添加 `test/commands/validate.test.ts`

## 6. 进度和用户体验
- [x] 6.1 使用 `ora` 或最小控制台进度显示当前项目和运行计数
- [x] 6.2 在 `--json` schema 下保持输出稳定（无额外日志到 stdout；如有需要将进度输出到 stderr）
- [x] 6.3 通过并发限制确保响应性

## 7. 测试
- [x] 7.1 添加顶级验证测试：`test/commands/validate.test.ts`
 - 包括非交互式提示、--all JSON、带并发的 --specs、歧义错误
- [ ] 7.2 为 `isInteractive` 和项目发现辅助函数添加单元测试
- [x] 7.3 扩展现有变更/spec 命令测试以覆盖交互式 `validate`
 - 已添加 `test/commands/change.interactive-validate.test.ts`、`test/commands/spec.interactive-validate.test.ts`

## 8. CLI 帮助和文档
- [x] 8.1 更新 `src/cli/index.ts` 中的命令描述/选项
- [x] 8.2 验证帮助输出包含 `validate` 命令和标志
- [x] 8.3 确保 `openspec/changes/bulk-validation-interactive-selection/specs/*` 下现有 spec 仍然满足

## 9. 非功能性需求
- [x] 9.1 代码风格和类型：导出的 API 使用显式类型；避免 `any`
- [x] 9.2 无 linter 错误；格式稳定；避免无关重构
- [x] 9.3 保持未受影响命令的现有行为

## 10. 验收标准映射
- [x] AC-1：`openspec change validate` 无参数时交互式选择（仅 TTY；遵循 `--no-interactive`/环境变量）—— 符合 cli-change spec
- [x] AC-2：`openspec spec validate` 无参数时交互式选择（仅 TTY；遵循 `--no-interactive`/环境变量）—— 符合 cli-spec spec
- [x] AC-3：新的 `openspec validate` 支持交互式选择、批量/过滤验证、JSON schema、进度、并发、退出码 —— 符合 cli-validate spec
