# 实现任务 — 添加交互式 Show 命令

## 目标
- 添加一个顶层 `show` 命令，具有智能选择和类型检测功能。
- 当未提供 ID 时，为 `change show` 和 `spec show` 添加交互式选择。
- 保留原始优先的输出行为和现有的 JSON 格式/过滤器。
- 一致地遵循 `--no-interactive` 和 `OPEN_SPEC_INTERACTIVE=0`。

---

## 1) CLI 接线
- [x] 在 `src/cli/index.ts` 中添加顶层命令：`program.command('show [item-name]')`
 - 选项：
 - `--json`
 - `--type <type>` 其中 `<type>` 为 `change|spec`
 - `--no-interactive`
 - 使用 `.allowUnknownOption(true)` 允许透传类型特定的标志，使顶层可以将标志转发到底层类型处理器。
 - 动作：实例化 `new ShowCommand().execute(itemName, options)`。
- [x] 更新 `change show` 子命令以接受 `--no-interactive` 并将其传递给 `ChangeCommand.show(...)`。
- [x] 更改 `spec show` 子命令以接受可选的 ID（`show [spec-id]`），添加 `--no-interactive`，并传递给 spec show 实现。

验收：
- `openspec show` 存在，并在非交互式上下文中无参数时打印有用的提示。
- 其他类型的未知标志不会导致解析崩溃；它们会被适当地警告/忽略。

---

## 2) 新模块：`src/commands/show.ts`
- [x] 创建 `ShowCommand`，包含：
 - `execute(itemName?: string, options?: { json?: boolean; type?: string; noInteractive?: boolean; [k: string]: any })`
 - 当 `!itemName` 且启用交互 schema 时的交互路径：
 - 提示："你想显示什么？" → `change` 或 `spec`。
 - 加载所选类型的可用 ID 并提示选择。
 - 委托给类型特定的 show 实现。
 - 当 `!itemName` 时的非交互路径：
 - 打印带有示例的提示：
 - `openspec show <item>`
 - `openspec change show`
 - `openspec spec show`
 - 以退出码 1 退出。
 - 当提供 `itemName` 时的直接条目路径：
 - 通过 `--type` 的类型覆盖优先。
 - 否则使用 `getActiveChangeIds()` 和 `getSpecIds()` 进行检测。
 - 如果存在歧义且无覆盖：打印错误 + 建议传递 `--type` 或使用子命令；退出码 1。
 - 如果未知：打印未找到及最接近匹配的建议；退出码 1。
 - 成功后：委托给类型特定的 show。
- [x] 标志作用域和透传：
 - 通用：`--json` → 转发给两种类型。
 - Change 专用：`--deltas-only`、`--requirements-only`（已弃用别名）。
 - Spec 专用：`--requirements`、`--no-scenarios`、`-r/--requirement`。
 - 警告并忽略与解析类型无关的标志。

验收：
- `openspec show <change-id> --json --deltas-only` 匹配 `openspec change show <id> --json --deltas-only` 的输出。
- `openspec show <spec-id> --json --requirements` 匹配 `openspec spec show <id> --json --requirements` 的输出。
- 歧义和未找到的行为符合 `cli-show` spec。

---

## 3) 重构 spec show 为可复用 API
- [x] 在 `src/commands/spec.ts` 中，将 show 逻辑提取到导出的 `SpecCommand`，包含 `show(specId?: string, options?: { json?: boolean; requirements?: boolean; scenarios?: boolean; requirement?: string; noInteractive?: boolean })`。
 - 复用当前的辅助函数（`parseSpecFromFile`、`filterSpec`、原始优先打印）。
 - 保留 `registerSpecCommand`，但委托给 `new SpecCommand().show(...)`。
- [x] 更新 CLI spec show 子命令为可选参数和交互行为（参见第 4 节）。

验收：
- 现有的 `spec show` 测试继续通过。
- 新的 `SpecCommand.show` 可以从 `ShowCommand` 调用。

---

## 4) 子命令中的向后兼容交互
- [x] `src/commands/change.ts` → 扩展 `show(changeName?: string, options?: { json?: boolean; requirementsOnly?: boolean; deltasOnly?: boolean; noInteractive?: boolean })`：
 - 当 `!changeName` 且启用交互 schema 时：从 `getActiveChangeIds()` 提示并显示选中的变更。
 - 非交互回退：保持当前行为（打印可用 ID + `openspec change list` 提示，设置 `process.exitCode = 1`）。
- [x] `src/commands/spec.ts` → `SpecCommand.show` 如上：
 - 当 `!specId` 且启用交互 schema 时：从 `getSpecIds()` 提示并显示选中的 spec。
 - 非交互回退：打印与缺失 `<spec-id>` 相同的行为错误并设置非零退出码。

验收：
- `openspec change show` 在非交互 schema 下打印列表提示并以非零退出。
- `openspec spec show` 在非交互 schema 下打印缺少参数错误并以非零退出。

---

## 5) 共享工具函数
- [x] 将 `nearestMatches` 和 `levenshtein` 从 `src/commands/validate.ts` 提取到 `src/utils/match.ts`（导出的辅助函数）。
- [x] 更新 `ValidateCommand` 和新的 `ShowCommand` 以从 `utils/match` 导入。

验收：
- 构建成功，辅助函数共享且无重复。

---

## 6) 提示、警告和消息
- [x] 顶层 `show` 提示（非交互式无参数）：
 - 行内容包括：`openspec show <item>`、`openspec change show`、`openspec spec show`，以及"或在交互式终端中运行。"。
- [x] 歧义消息建议使用 `--type change|spec` 和子命令。
- [x] 未找到建议最接近的匹配（最多 5 个）。
- [x] 不相关标志警告针对解析的类型（打印到 stderr，不崩溃）。

验收：
- 消息符合 `cli-show` spec 措辞意图和别处使用的风格。

---

## 7) 测试
添加测试，镜像现有 schema（通过 `OPEN_SPEC_INTERACTIVE=0` 进行非 TTY 模拟）。

- [x] `test/commands/show.test.ts`
 - 非交互式，无参数 → 打印提示并以非零退出。
 - 直接条目检测 change 和 spec。
 - 两者都存在时的歧义情况 → 错误和建议 `--type`。
 - 未找到情况 → 最接近匹配建议。
 - 透传标志：change `--json --deltas-only`，spec `--json --requirements`。
- [x] `test/commands/change.interactive-show.test.ts`（非交互回退）
 - 确保 `openspec change show` 无参数时打印可用 ID + 列表提示并以非零退出。
- [x] `test/commands/spec.interactive-show.test.ts`（非交互回退）
 - 确保 `openspec spec show` 无参数时打印缺少参数错误并以非零退出。

验收：
- 构建后所有新测试通过；现有测试无回归。

---

## 8) 文档（可选但推荐）
- [x] 更新 `openspec/README.md` 的使用示例，包含新的 `show` 命令，包括类型检测和标志。

---

## 9) 非功能性检查
- [x] 运行 `pnpm build` 和所有测试（`pnpm test`）。
- [x] 确保没有 linter/类型错误，消息与现有风格一致。

---

## 一致性说明
- 遵循文本输出的原始优先行为：透传文件内容，无格式，镜像当前 `change show` 和 `spec show` 的行为。
- 复用 `isInteractive` 和 `item-discovery` 辅助函数以保持一致的提示行为。
- 保持 JSON 输出形状与当前的 `ChangeCommand.show` 和 `spec show` 输出一致。
