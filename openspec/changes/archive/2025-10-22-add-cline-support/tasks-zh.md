## 1. 实现
- [x] 1.1 在 `src/core/configurators/slash/cline.ts` 中创建 ClineSlashCommandConfigurator 类
- [x] 1.2 在 `src/core/configurators/cline.ts` 中创建 ClineConfigurator 类
- [x] 1.3 创建 `cline-template.ts` 用于模板导出
- [x] 1.4 定义 Cline 规则的文件路径（`.clinerules/`）
- [x] 1.5 创建 Cline 特定的前置元数据（Markdown 标题格式）
- [x] 1.6 在 `slash/registry.ts` 中注册 Cline
- [x] 1.7 在 `configurators/registry.ts` 中注册 Cline
- [x] 1.8 在 `config.ts` 中向 `AI_TOOLS` 添加 Cline
- [x] 1.9 在 `templates/index.ts` 中添加 `getClineTemplate()`
- [x] 1.10 更新 README 中的 Cline 文档

## 2. 测试
- [x] 2.1 添加 CLINE.md 创建和更新的初始化测试
- [x] 2.2 添加 `.clinerules/` 文件创建的初始化测试
- [x] 2.3 添加 CLINE.md 更新的更新测试
- [x] 2.4 添加 `.clinerules/` 文件刷新的更新测试
- [x] 2.5 测试与 `openspec init --tools cline` 的集成
- [x] 2.6 验证所有 225 个测试通过
