## 1. 遗留检测与清理模块

- [x] 1.1 创建 `src/core/legacy-cleanup.ts`，包含所有遗留制品类型的检测函数
- [x] 1.2 实现 `detectLegacyConfigFiles()` - 检查包含 OpenSpec 标记的配置文件
- [x] 1.3 实现 `detectLegacySlashCommands()` - 检查旧的 `/openspec:*` 命令目录
- [x] 1.4 实现 `detectLegacyStructureFiles()` - 检查 AGENTS.md（project.md 单独检测以显示提示信息）
- [x] 1.5 实现 `removeMarkerBlock()` - 从文件中精确移除 OpenSpec 标记块
- [x] 1.6 实现 `cleanupLegacyArtifacts()` - 编排移除过程，妥善处理边界情况（保留 project.md）
- [x] 1.7 为 project.md 实现迁移提示输出 - 显示消息引导用户迁移到 config.yaml
- [x] 1.8 为遗留检测和清理功能添加单元测试

## 2. 重写 Init 命令

- [x] 2.1 用 experimental 的方案替换 `src/core/init.ts` 为新实现
- [x] 2.2 从 `src/ui/welcome-screen.ts` 导入并使用动画欢迎界面
- [x] 2.3 从 `src/prompts/searchable-multi-select.ts` 导入并使用可搜索多选
- [x] 2.4 在 init 流程开始时集成遗留检测
- [x] 2.5 添加遗留清理确认的 Y/N 提示
- [x] 2.6 使用现有的 `skill-templates.ts` 生成技能
- [x] 2.7 使用现有的 `command-generation/` 适配器生成斜杠命令
- [x] 2.8 创建带默认模式的 `openspec/config.yaml`
- [x] 2.9 更新成功输出以匹配新工作流（技能、/opsx:* 命令）
- [x] 2.10 添加 `--force` 标志，在非交互模式下跳过遗留清理提示

## 3. 移除遗留代码

- [x] 3.1 删除 `src/core/configurators/` 目录（ToolRegistry、所有配置生成器）
- [x] 3.2 删除 `src/core/templates/slash-command-templates.ts`
- [x] 3.3 删除 `src/core/templates/claude-template.ts`
- [x] 3.4 删除 `src/core/templates/cline-template.ts`
- [x] 3.5 删除 `src/core/templates/costrict-template.ts`
- [x] 3.6 删除 `src/core/templates/agents-template.ts`
- [x] 3.7 删除 `src/core/templates/agents-root-stub.ts`
- [x] 3.8 删除 `src/core/templates/project-template.ts`
- [x] 3.9 删除 `src/commands/experimental/` 目录
- [x] 3.10 更新 `src/core/templates/index.ts` 以移除已删除的导出
- [x] 3.11 删除已移除模块的相关测试文件（wizard.ts）

## 4. 更新 CLI 注册

- [x] 4.1 更新 `src/cli/index.ts` 以移除 `registerArtifactWorkflowCommands()` 调用
- [x] 4.2 保留 experimental 子命令（status、instructions、schemas 等），但直接注册
- [x] 4.3 从保留的子命令中移除"[Experimental]"标签
- [x] 4.4 添加隐藏的 `experimental` 命令作为 `init` 的别名

## 5. 更新相关命令

- [x] 5.1 更新 `openspec update` 命令以刷新技能/命令而非配置文件
- [x] 5.2 从 update 中移除配置文件刷新逻辑
- [x] 5.3 向 update 添加技能刷新逻辑

## 6. 测试与验证

- [x] 6.1 为新 init 流程添加集成测试（全新安装）
- [x] 6.2 为遗留检测和清理添加集成测试
- [x] 6.3 为扩展模式（重新运行 init）添加集成测试
- [x] 6.4 使用 `--tools` 标志测试非交互模式
- [x] 6.5 测试 CI 环境的 `--force` 标志
- [x] 6.6 验证跨平台路径处理（全程使用 path.join）
- [x] 6.7 运行完整测试套件并修复任何损坏的测试

## 7. 文档与清理

- [x] 7.1 使用新的 init 行为更新 README（基于技能的工作流是自文档化的）
- [x] 7.2 为发布说明记录破坏性变更（在任务文件中）
- [x] 7.3 移除对已删除模块的任何孤立导入/引用（已验证不存在）
- [x] 7.4 运行 linter 并修复任何问题（已通过）
