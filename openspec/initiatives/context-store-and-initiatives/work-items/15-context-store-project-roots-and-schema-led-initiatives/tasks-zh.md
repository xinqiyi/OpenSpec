# 上下文存储项目根与 Schema 驱动的倡议的任务

- [x] 创建 Item 15 工作项跟踪说明。
- [ ] 记录产品决策：上下文存储应像 OpenSpec 根一样表现用于配置和 schema 解析，但默认不作为实现仓库。
- [ ] 定义上下文存储根布局，包括 `.openspec-store/`、`openspec/config.yaml`、`openspec/schemas/` 和 `initiatives/`。
- [ ] 决定默认倡议 schema 的配置键，以 `initiative_schema` 作为首选的下一版本安全方向。
- [ ] 决定倡议 schema 是与 `openspec/schemas/` 共享并带有 `usage: initiative` 鉴别器，还是在使用相同产物图格式的同时使用单独的命名空间。
- [ ] 添加或设计内置的 `product-initiative` schema，用于高级需求和设计产物。
- [ ] 定义 `brief.md` 作为精简创建种子，并决定它是位于产物图之外还是表示为已完成产物。
- [ ] 将 `initiative create` 从硬编码的六文件生成改为精简的 `initiative.yaml` 加 `brief.md` 创建。
- [ ] 添加以 `context-store/initiatives/<id>/` 为根的倡议产物状态解析。
- [ ] 添加倡议产物指令输出，返回 schema 指导、模板内容、依赖关系、输出路径和现有路径。
- [ ] 确保可以为倡议产物指令读取存储本地配置上下文和规则，而不与仓库本地变更配置混淆。
- [ ] 保护规划家园解析，使具有 `openspec/config.yaml` 的上下文存储不会静默成为仓库本地的实现家园。
- [ ] 更新 `initiative create --json`、人类输出和下一步命令指导，以支持精简创建和迭代产物。
- [ ] 更新当前断言 MVP 六文件倡议形态的测试。
- [ ] 添加兼容性测试，证明旧的六文件倡议仍然可以列出和显示。
- [ ] 为上下文存储本地 schema 和存储配置默认值添加测试。
- [ ] 更新 beta 文档和代理指导，停止告诉代理在创建后立即编辑每个倡议 Markdown 文件。
- [ ] 记录迁移行为并说明 Item 5 的六文件 MVP 形态已被此 schema 驱动的精简模型取代。
