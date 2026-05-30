## 0. 堆栈协调

- [ ] 0.1 在实现之前，将此变更变基到最新的 `main` 分支
- [ ] 0.2 如果 `simplify-skill-installation` 先合并，保留其 profile/delivery 模型，并将此变更作为能力感知的精炼应用
- [ ] 0.3 如果此变更先合并，确保后续变基不会重新引入一刀切的"commands = 移除所有技能"规则
- [ ] 0.4 如果 `add-global-install-scope` 已合并，验证 scope x delivery x command-surface 的组合行为保持确定性

## 1. 工具命令表面能力模型

- [ ] 1.1 在 `src/core/config.ts` 中扩展工具元数据，添加可选的命令表面能力字段
- [ ] 1.2 定义支持的能力值：`adapter`、`skills-invocable`、`none`
- [ ] 1.3 将 Trae 标记为 `skills-invocable`
- [ ] 1.4 添加共享能力解析器（优先显式元数据覆盖，其次根据适配器存在推断回退）
- [ ] 1.5 为能力解析添加针对性的单元测试（显式覆盖、推断适配器、推断无）

## 2. Init：能力感知的交付规划

- [ ] 2.1 重构 init 生成逻辑，计算每个工具的有效操作（生成/移除技能和命令），而非仅使用全局布尔值
- [ ] 2.2 在 `delivery=commands` 模式下，为 `skills-invocable` 工具保留/生成技能，不移除那些受管理的技能目录
- [ ] 2.3 在 `delivery=commands` 模式下，当任何选中的工具解析为 `none` 时，在写入前快速失败
- [ ] 2.4 更新 init 输出，清晰报告 `skills-invocable` 工具的有效行为（技能用作命令表面）
- [ ] 2.5 确保 init 不再对有意使用 `skills-invocable` 的工具报告"无适配器"
- [ ] 2.6 添加/调整 init 测试，覆盖 `delivery=commands` + `trae`（技能保留/生成，无适配器错误）、混合工具（`claude,trae`），以及不支持的命令表面（`none`）的确定性失败路径

## 3. Update：能力感知的同步和漂移检测

- [ ] 3.1 重构 update 同步逻辑，按工具能力应用交付行为（而非每次运行全局应用）
- [ ] 3.2 在 `delivery=commands` 模式下，为 `skills-invocable` 工具保留/生成受管理的技能
- [ ] 3.3 在 `delivery=commands` 模式下，当已配置的工具包含 `none` 命令表面时，在部分更新前失败
- [ ] 3.4 更新 profile/delivery 漂移检测，避免在 commands 交付下对 `skills-invocable` 工具产生永久漂移
- [ ] 3.5 确保已配置工具检测在 commands 交付下，当存在受管理技能时仍包含 `skills-invocable` 工具
- [ ] 3.6 更新摘要输出，使 skills-invocable 行为报告为预期行为（而非隐式跳过/错误）
- [ ] 3.7 添加/调整 update 测试，覆盖 `delivery=commands` + 已配置的 Trae（技能保留/生成）、幂等的第二次 update（无错误漂移循环）、混合已配置工具（`claude` + `trae`），以及不支持的命令表面（`none`）的确定性预检失败

## 4. 用户体验和错误消息

- [ ] 4.1 为 `delivery=commands` 且所选工具包含 `skills-invocable` 时添加交互式 init 兼容性说明
- [ ] 4.2 添加确定性的非交互式错误文本，包含不兼容的工具 ID 和建议的替代方案（`both` 或 `skills`）
- [ ] 4.3 统一 init 和 update 的措辞，使能力相关的行为/消息保持一致

## 5. 文档更新

- [ ] 5.1 更新 `docs/supported-tools.md`，记录 Trae 的命令表面语义并澄清交付交互
- [ ] 5.2 更新 `docs/cli.md` 交付指导，解释 `delivery=commands` 的能力感知行为
- [ ] 5.3 为"仅命令 + 不支持的工具"失败添加简短的故障排除说明

## 6. 验证

- [ ] 6.1 运行针对性测试：`test/core/init.test.ts` 和 `test/core/update.test.ts`
- [ ] 6.2 运行此变更中添加的任何新的能力/单元测试文件
- [ ] 6.3 运行完整测试套件（`pnpm test`）并解决回归问题
- [ ] 6.4 手动冒烟检查：`openspec init --tools trae` 配合 `delivery=commands`
- [ ] 6.5 手动冒烟检查：混合工具（`claude,trae`）配合 `delivery=commands`
