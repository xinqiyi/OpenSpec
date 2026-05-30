## 1. 全局配置扩展

- [x] 1.1 在 `src/core/global-config.ts` 模式中扩展 `profile`、`delivery` 和 `workflows` 字段
- [x] 1.2 添加 profile（`core` | `custom`）、delivery（`both` | `skills` | `commands`）和 workflows（字符串数组）的 TypeScript 类型
- [x] 1.3 更新 `GlobalConfig` 接口和默认值（profile=`core`、delivery=`both`）
- [x] 1.4 更新现有的 `readGlobalConfig()` 以使用默认值处理缺少的新字段
- [x] 1.5 为模式演进添加测试（不含新字段的现有配置）

## 2. 配置文件系统

- [x] 2.1 创建包含配置文件定义（core、custom）的 `src/core/profiles.ts`
- [x] 2.2 定义 `CORE_WORKFLOWS` 常量：`['propose', 'explore', 'apply', 'archive']`
- [x] 2.3 定义包含全部 11 个工作流的 `ALL_WORKFLOWS` 常量
- [x] 2.4 在 `src/core/shared/tool-detection.ts` 中添加 `COMMAND_IDS` 常量（与现有的 `SKILL_NAMES` 并行）
- [x] 2.5 实现 `getProfileWorkflows(profile, customWorkflows?)` 解析函数
- [x] 2.6 为配置文件解析添加测试

## 3. 配置 Profile 命令（交互式选择器）

- [x] 3.1 在 `src/commands/config.ts` 中添加 `config profile` 子命令
- [x] 3.2 实现带有 delivery 选择（skills/commands/both）的交互式选择器 UI
- [x] 3.3 实现带有 workflow 切换开关的交互式选择器 UI
- [x] 3.4 在选择器中预选当前配置值
- [x] 3.5 确认后更新全局配置（仅配置，不重新生成文件）
- [x] 3.6 显示更新后消息："配置已更新。在你的项目中运行 `openspec update` 以应用。"
- [x] 3.7 检测是否在 OpenSpec 项目内运行，并提供自动运行 update 的选项
- [x] 3.8 实现 `config profile core` 预设快捷方式（保留 delivery 设置）
- [x] 3.9 处理非交互模式：报错并显示有帮助的消息
- [x] 3.10 更新 `openspec config list` 以显示 profile、delivery 和 workflows 设置（标明默认值与显式值）
- [x] 3.11 为 config profile 命令和 config list 输出添加测试

## 4. 可用工具检测

- [x] 4.1 创建 `src/core/available-tools.ts`（与现有的 `tool-detection.ts` 分离）
- [x] 4.2 实现 `getAvailableTools(projectPath)`，扫描 AI 工具目录（`.claude/`、`.cursor/` 等）
- [x] 4.3 使用 `AI_TOOLS` 配置将目录名称映射到工具 ID
- [x] 4.4 为可用工具检测添加测试，包括跨平台路径

## 5. Propose 工作流模板

- [x] 5.1 创建 `src/core/templates/workflows/propose.ts`
- [x] 5.2 实现结合 new + ff 行为的技能模板
- [x] 5.3 确保 propose 在生成工件之前通过 `openspec new change` 创建 `.openspec.yaml`
- [x] 5.4 为模板添加入门式解释性输出
- [x] 5.5 实现 propose 的命令模板
- [x] 5.6 从 `src/core/templates/skill-templates.ts` 导出模板
- [x] 5.7 在 `src/core/shared/tool-detection.ts` 的 `SKILL_NAMES` 中添加 `openspec-propose`
- [x] 5.8 在 `src/core/shared/skill-generation.ts` 的命令模板中添加 `propose`
- [x] 5.9 在 `src/core/shared/tool-detection.ts` 的 `COMMAND_IDS` 中添加 `propose`
- [x] 5.10 为 propose 模板添加测试（创建变更、生成工件、等同于 new + ff）

## 6. 条件性技能/命令生成

- [x] 6.1 更新 `getSkillTemplates()` 以接受配置文件过滤参数
- [x] 6.2 更新 `getCommandTemplates()` 以接受配置文件过滤参数
- [x] 6.3 更新 init.ts 中的 `generateSkillsAndCommands()` 以尊重 delivery 设置
- [x] 6.4 添加当 delivery 为 'commands' 时跳过技能生成的逻辑
- [x] 6.5 添加当 delivery 为 'skills' 时跳过命令生成的逻辑
- [x] 6.6 为条件性生成添加测试

## 7. Init 流程更新

- [x] 7.1 更新 init 以首先调用 `getAvailableTools()`
- [x] 7.2 更新 init 以读取全局配置获取 profile/delivery 默认值
- [x] 7.3 向 init 添加迁移检查：在配置文件解析前调用共享的 `migrateIfNeeded()`
- [x] 7.4 将工具选择改为显示预选的已检测工具
- [x] 7.5 在 init 中直接应用已配置的配置文件（无配置文件确认提示）
- [x] 7.6 更新成功消息以显示 `/opsx:propose` 提示（仅当 propose 在活跃配置文件中时）
- [x] 7.7 添加 `--profile` 标志以覆盖全局配置
- [x] 7.8 更新非交互模式以使用默认值，不进行提示
- [x] 7.9 为各种场景下的 init 流程添加测试（包括重新初始化时的迁移和自定义配置文件行为）

## 8. Update 命令（配置文件支持 + 迁移）

- [x] 8.1 修改现有的 `src/commands/update.ts` 以读取全局配置中的 profile/delivery/workflows
- [x] 8.2 实现共享的 `scanInstalledWorkflows(projectPath, tools)` — 扫描工具目录，仅匹配 `ALL_WORKFLOWS` 常量，返回各工具的并集
- [x] 8.3 实现共享的 `migrateIfNeeded(projectPath, tools)` — 由 `init` 和 `update` 使用的一次性迁移逻辑
- [x] 8.4 显示迁移消息："已迁移：包含 N 个工作流的自定义配置文件" + "此版本新增：/opsx:propose。尝试运行 'openspec config profile core' 以获得精简体验。"
- [x] 8.5 添加项目检查：如果不存在 `openspec/` 目录则退出并报错
- [x] 8.6 添加检测逻辑，找出配置中存在但未安装的工作流（以便添加）
- [x] 8.7 添加检测逻辑，找出已安装且需要刷新的工作流（以便更新）
- [x] 8.8 尊重 delivery 设置：如果为 `skills` 则仅生成技能，如果为 `commands` 则仅生成命令
- [x] 8.9 当 delivery 更改时删除文件：如果为 `skills` 则移除命令，如果为 `commands` 则移除技能
- [x] 8.10 为配置文件中缺失的工作流生成新的工作流文件
- [x] 8.11 显示摘要："已添加：X、Y" / "已更新：Z" / "已移除：N 个文件" / "已是最新。"
- [x] 8.12 在输出中列出受影响的工具："工具：Claude Code、Cursor"
- [x] 8.13 检测当前未配置的新工具目录，并显示重新初始化提示
- [x] 8.14 为迁移场景添加测试（现有用户、部分工作流、多工具、幂等性、忽略自定义技能）
- [x] 8.15 为带配置文件的 update 命令场景添加测试（包括 delivery 更改、项目外错误、新工具检测）

## 9. 工具选择 UX 修复

- [x] 9.1 更新 `src/prompts/searchable-multi-select.ts` 的快捷键
- [x] 9.2 将空格键改为切换选择
- [x] 9.3 将回车键改为确认选择
- [x] 9.4 移除 Tab 键确认行为
- [x] 9.5 添加提示文字"空格键切换，回车键确认"
- [x] 9.6 为快捷键行为添加测试

## 10. 脚手架验证

- [x] 10.1 验证 `openspec new change` 创建包含 schema 和 created 字段的 `.openspec.yaml`

<!-- 注意：下面的 10.2 和 10.3 是潜在的后续工作，不是此变更的核心 -->
<!-- - [ ] 10.2 更新 ff 技能以验证 `openspec new change` 后 `.openspec.yaml` 是否存在 -->
<!-- - [ ] 10.3 为技能添加防护："切勿手动在 openspec/changes/ 中创建文件——请使用 openspec new change" -->

## 11. 模板下一步指导

- [x] 11.1 审计所有模板，检查硬编码的跨工作流命令引用（例如 `/opsx:propose`）
- [x] 11.2 将所有特定命令引用替换为基于概念的通用指导（例如"创建变更提案"）
- [x] 11.3 审查 explore 到 propose 的过渡 UX（参见 `openspec/explorations/explore-workflow-ux.md` 中未解决的问题）

## 12. 集成与手动测试

- [x] 12.1 运行完整测试套件并修复所有失败
- [x] 12.2 在 Windows 上测试（或确认 CI 在 Windows 上通过）
- [x] 12.3 测试端到端流程：init → propose → apply → archive
- [x] 12.4 更新新命令的 CLI 帮助文本
- [x] 12.5 手动：交互式 init — 验证检测到的工具已预选、确认提示有效、成功消息正确
- [x] 12.6 手动：`openspec config profile` 选择器 — 验证 delivery 切换、workflow 切换、当前值预选、core 预设快捷方式
- [x] 12.7 手动：使用自定义配置文件的 init — 验证 init 无需配置文件确认提示即可进行
- [x] 12.8 手动：通过 update 进行 delivery 更改 — 验证在 skills/commands/both 之间切换时正确删除/创建文件
- [x] 12.9 手动：迁移流程 — 在已有的无配置文件中配置字段的项目上运行 update，验证迁移消息和生成的配置

## 13. 实现后加固（审查后续）

- [x] 13.1 确保即使模板是最新的，`update` 也将 profile/delivery 漂移视为需要更新
- [x] 13.2 确保 `update` 将仅命令安装视为已配置的工具
- [x] 13.3 确保 `init` 验证 `--profile` 值并在无效覆盖时报错
- [x] 13.4 确保重新运行 `init` 时应用 delivery 清理（移除与当前 delivery 模式不匹配的文件）
- [x] 13.5 添加/调整配置漂移同步、仅命令检测、无效配置覆盖和重新初始化 delivery 清理的回归测试
