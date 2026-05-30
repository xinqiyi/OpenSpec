## 阶段 1：workspace 设置 skill

用户可测试的成果：用户可以运行 workspace 设置，选择哪些 agent 获得活动配置文件的 OpenSpec skill，并验证所选 skill 仅在 workspace 根目录生成。

- [x] 1.1 添加一个名为"安装 agent skill"的交互式 workspace 设置步骤，询问哪些 agent 应在此 workspace 中获得 OpenSpec skill。
- [x] 1.2 当首选打开程序支持 skill 时，预选该打开程序，同时允许用户选择不同或额外的 agent。
- [x] 1.3 使用现有的 `--tools all|none|<ids>` 风格支持非交互式 agent 选择。
- [x] 1.4 使用与 repository 初始化相同的受支持 skill 生成工具集来验证 workspace 设置工具 ID。
- [x] 1.5 解析活动的全局配置文件，并使用它来选择 workspace 设置安装哪些 workflow skill。
- [x] 1.6 确保 `openspec workspace setup` 为所选 agent 在 workspace 根目录生成或刷新 OpenSpec agent skill。
- [x] 1.7 将设置时的 skill 生成限定在 workspace planning 主目录内；在 workspace 设置期间不将 skill 或 OpenSpec artifact 写入链接的 repository 或文件夹。
- [x] 1.8 在此切片中将 workspace 设置 skill 生成保持为仅限 skill；即使全局交付包含命令，也不生成斜杠命令或全局命令文件。
- [x] 1.9 定义设置在人类和 JSON 输出中如何报告已生成、已刷新、已跳过、已失败和仅 skill 交付。
- [x] 1.10 将所选的 workspace skill agent 和最后应用的 workflow ID 存储在仅限 workspace 本地的机器状态中。
- [x] 1.11 当 `--tools` 省略时，通过跳过 skill 安装并给出清晰指导，保持非交互式设置兼容性。
- [x] 1.12 在交互式和非交互式 schema 下手动运行 workspace 设置，并验证所选的配置文件 workflow 仅落地在 workspace 根目录。
- [x] 1.13 审查设置 UX：提示措辞、默认值、跳过路径、配置文件/交付消息、成功输出和 JSON 输出在继续前是否清晰。

## 阶段 2：workspace skill 更新

用户可测试的成果：用户可以在现有 workspace 中更改全局配置文件、运行 workspace 更新，并看到 workspace 本地 skill 刷新为所选 workflow，并带有清晰的人类和 JSON 输出。

- [x] 2.1 添加一个 workspace 更新流程，用于刷新、添加或删除现有 workspace 中的 OpenSpec agent skill。
- [x] 2.2 让 `openspec workspace update` 在从 workspace 内部运行时解析当前 workspace。
- [x] 2.3 支持命名和选定 workspace 更新形式，例如 `openspec workspace update platform` 和 `openspec workspace update --workspace platform`。
- [x] 2.4 支持非交互式更新形式，例如 `openspec workspace update platform --tools codex,claude`。
- [x] 2.5 仅移除不再选中的 agent 的已知 OpenSpec 管理 workflow skill 目录。
- [x] 2.6 将 workspace 本地 workflow skill 目录与当前全局配置文件选择同步。
- [x] 2.7 在此切片中将 workspace 更新保持为仅限 skill；即使全局交付包含命令，也不生成斜杠命令或全局命令文件。
- [x] 2.8 定义更新在人类和 JSON 输出中如何报告已刷新、已添加、已移除、已跳过、已失败和仅 skill 交付。
- [x] 2.9 当 workspace 更新在没有 `--tools` 的情况下运行时使用存储的所选 agent，并在传递 `--tools` 时更新该存储的选择。
- [x] 2.10 检测 workspace 本地 skill 与活动全局配置文件的差异，并报告 `openspec workspace update` 指导。
- [x] 2.11 手动运行 workspace 更新，涵盖刷新、添加、移除、无操作、省略 `--tools` 和配置文件变更情况，并验证链接的 repository 保持不变。
- [x] 2.12 审查更新 UX：命令形式、当前 workspace 检测、配置文件/交付消息、差异消息、移除消息和 JSON 输出是否可理解。

## 阶段 3：配置配置文件 workspace 应用

用户可测试的成果：用户可以在 workspace 内运行 `openspec config profile`，并选择是否将变更后的全局配置文件应用到该 workspace。

- [x] 3.1 检测 `openspec config profile` 何时从 OpenSpec workspace 内部运行。
- [x] 3.2 在 workspace 内发生实际的配置文件或交付变更后，提示立即将变更应用于当前 workspace。
- [x] 3.3 确认后，为当前 workspace 运行 `openspec workspace update`，而不是 repository 本地的 `openspec update`。
- [x] 3.4 拒绝时，报告全局配置已更改，以及 `openspec workspace update` 可以稍后应用它。
- [x] 3.5 在 workspace 外部保留现有的 repository 本地 `openspec config profile` 应用行为。
- [x] 3.6 保持 `openspec config profile core` 为非交互式，但在 workspace 内部运行时打印特定于 workspace 的 `openspec workspace update` 指导。
- [x] 3.7 当 workspace 本地 skill 与活动全局配置文件有差异时，在 workspace 内无操作配置配置文件上给出警告。
- [x] 3.8 手动在 workspace 内部运行 `openspec config profile`，涵盖确认、拒绝、无操作、差异警告和 `core` 预设路径。
- [x] 3.9 审查配置配置文件 UX：提示措辞、项目/workspace 区分、无操作行为、预设指导和后续指导是否清晰。

## 阶段 4：workspace 变更创建

用户可测试的成果：用户可以从协调根目录创建 workspace 级别的变更，检查其 workspace planning artifact，并确认链接的 repository 未被编辑。

- [x] 4.1 添加内置的 `workspace-planning` schema 和 template，保持正常的 proposal/spec/设计/任务 artifact 结构。
- [x] 4.2 定义 workspace-planning spec artifact，支持嵌套的 `specs/**/*.md` 输出和 `specs/<区域或 repository>/<能力>/spec.md` 的说明。
- [x] 4.3 添加从 workspace 协调根目录创建 workspace 感知的变更。
- [x] 4.4 默认将 workspace 范围的变更创建设置为 `workspace-planning` schema。
- [x] 4.5 将 workspace 级别的变更存储在 workspace planning 路径下，而不是在链接的 repository 或文件夹下。
- [x] 4.6 在 workspace 变更级别一次性捕获产品目标。
- [x] 4.7 通过 workspace 范围的 spec 或任务章节，在适用时使用已注册的 workspace 链接名称记录或验证受影响的区域名称。
- [x] 4.8 确保创建 workspace 变更不会创建 repository 本地 OpenSpec artifact 或编辑链接的 repository。
- [x] 4.9 在 workspace 外部保留 repository 本地变更创建行为。
- [x] 4.10 从协调根目录手动创建 workspace 变更，并验证生成的 artifact、workspace 范围的 spec/任务、受影响的区域和未触及的链接 repository。
- [x] 4.11 审查变更创建 UX：目标捕获、受影响区域识别、artifact 路径和下一步指导感觉清晰。

## 阶段 5：planning 主目录和 agent 上下文

用户可测试的成果：用户可以运行 repository 本地和 workspace 变更的状态和说明，并看到解析后的 planning 主目录、artifact 路径、受影响的区域、约束和下一步。

- [x] 5.1 引入一个共享的 planning 主目录解析器，用于识别 repository 本地与 workspace planning 主目录。
- [x] 5.2 使用 planning 主目录、变更根目录、相关 artifact 路径、受影响的区域、下一步和操作上下文来丰富 `openspec status --change <id> --json`。
- [x] 5.3 使用解析后的 artifact 路径（用于 repository 本地和 workspace 范围的变更）来丰富 `openspec instructions <artifact> --change <id> --json`。
- [x] 5.4 在显式的实施 workflow 选择受影响的区域之前，保持 workspace 级别的 planning 作为真实源。
- [x] 5.5 在状态和说明输出中保留嵌套的 workspace spec 路径，而不将它们扁平化为 repository 本地能力路径。
- [x] 5.6 为 repository 本地和 workspace 范围的变更手动运行状态和说明，并验证路径和操作上下文正确。
- [x] 5.7 审查 planning 上下文 UX：人类输出、JSON 字段名称和下一步指导对用户和 agent 易于理解。

## 阶段 6：workflow skill 说明

用户可测试的成果：用户可以检查重新生成的 workflow skill，并验证它们是路径无关的，并告诉 agent 使用 CLI 报告的 artifact 路径。

- [x] 6.1 更新生成的 workflow skill template，在 artifact 工作前运行 `openspec status --change <id> --json`，并信任返回的 planning 上下文。
- [x] 6.2 更新生成的 workflow skill template，在编写 artifact 前运行 `openspec instructions <artifact> --change <id> --json`，并使用解析后的输出路径。
- [x] 6.3 审计源 workflow template 中硬编码的 `openspec/changes/<name>` 假设，并用 CLI 报告的路径指导替换它们。
- [x] 6.4 在此切片中保持 artifact 上下文命令独立，除非丰富的状态/说明在实施过程中被证明不足。
- [x] 6.5 手动重新生成或检查已安装的 workflow skill，并验证它们在 workspace 变更中遵循 CLI 报告的 artifact 路径。
- [x] 6.6 保护配置文件选中的 workflow skill，其 workspace 行为尚未实现，以免它们回退到 repository 本地路径或编辑链接的 repository。
- [x] 6.7 审查 agent 指令 UX：说明简洁、路径无关、对不受支持的 workspace workflow 安全，且对 repository 本地和 workspace planning 都实用。

## 阶段 7：验证

用户可测试的成果：用户或审查者可以从一个干净的 workspace 运行完整的检查清单，并比较每个早期阶段的预期与实际证据。

- [x] 7.1 添加测试，验证 workspace 设置在 workspace 根目录安装 skill，并保持链接的 repository 不变。
- [x] 7.2 添加测试，验证 workspace 更新刷新、添加和仅移除管理 workspace skill 目录。
- [x] 7.3 添加测试，验证 workspace 设置/更新使用当前全局配置文件进行 workflow skill 选择，同时保持 workspace 交付仅限 skill。
- [x] 7.4 添加测试，验证 `openspec config profile` 在 workspace 内部可以通过 `openspec workspace update` 应用变更。
- [x] 7.5 添加测试，用于存储的 workspace skill agent 选择、省略 `--tools` 行为和配置文件差异报告。
- [x] 7.6 添加测试，验证 `openspec update` 从 workspace planning 主目录重定向到 `openspec workspace update`。
- [x] 7.7 添加测试，验证不受支持的 workspace workflow skill 被保护，不会指示 repository 本地回退编辑。
- [x] 7.8 添加测试，验证已注册的 repository 在变更创建前可见。
- [x] 7.9 添加测试，验证 workspace 变更创建不意味着创建 repository 本地 artifact。
- [x] 7.10 添加测试，验证 workspace-planning schema 将嵌套的 `specs/<区域或 repository>/<能力>/spec.md` 文件解析为 workspace 范围的 spec。
- [x] 7.11 为 workspace 根 skill 路径和 workspace 变更路径添加跨平台路径测试。
- [x] 7.12 更新 CLI 文档、命令帮助和 shell 补全覆盖，涵盖 `workspace update`、`--tools`、配置文件行为和 workspace 仅 skill 交付。
- [x] 7.13 运行 `openspec validate workspace-change-planning --strict`。
- [x] 7.14 在标记变更为完成之前，运行完整的验收检查清单，涵盖设置、更新、配置配置文件、变更创建、planning 上下文和 workflow skill。
- [x] 7.15 完成对整个 workflow 的最终 UX 审查，并记录任何后续修复或有意的推迟。
- [x] 7.16 在实施签署前，记录每个阶段的手动命令或交互路径、预期观察和实际观察。
- [x] 7.17 如果有单独的审查者或新的 agent 上下文，重新运行验收和 UX 检查清单；如果没有，从干净的临时 workspace 重新运行并报告证据。

## 验证证据

完成证据于 2026-05-14 记录。

自动化检查：

```bash
pnpm run build
pnpm vitest run test/commands/workspace.test.ts test/commands/artifact-workflow.test.ts test/core/workspace/skills.test.ts test/core/planning-home.test.ts test/core/templates/skill-templates-parity.test.ts
node dist/cli/index.js validate workspace-change-planning --strict
git diff --check
```

干净 workspace 重新运行涵盖非交互式 workspace 设置、workspace 诊断、配置配置文件更新指导、workspace 更新重定向、使用 `--areas api,web` 的 workspace 变更创建、嵌套 workspace spec 的状态/说明 JSON、链接 repository 清洁度和受保护的不受支持 workflow skill。

观察到的结果：

- 构建、针对性测试、严格验证和空白字符检查通过。
- workspace 设置/更新仅在 workspace 根目录生成 skill，并保持链接的 repository 未触及。
- workspace 变更创建使用了 schema `workspace-planning`，报告了受影响的区域 `api` 和 `web`，保留了嵌套的 `specs/api/login/spec.md`，并在 planning 期间保持 `actionContext.allowedEditRoots` 为空。
- 生成的 workflow skill 使用了 CLI 报告的路径和 workspace 保护，而不是硬编码的 `openspec/changes/<name>` 路径。
- 没有新的 agent 重新运行；干净的临时 workspace 重新运行作为后备的独立验收通行证。
