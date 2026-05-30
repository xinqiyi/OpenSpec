## 1. 清单基础

- [ ] 1.1 在 `src/core/templates/` 下创建 spec 的 workflow 清单注册表
- [ ] 1.2 定义共享清单类型，用于 workflow ID、skill 元数据和可选命令描述符
- [ ] 1.3 迁移现有 workflow 注册（`getSkillTemplates`、`getCommandTemplates`、`getCommandContents`）以从清单派生
- [ ] 1.4 保留 `src/core/templates/skill-templates.ts` 的现有外部导出/API 兼容性

## 2. 工具配置文件层

- [ ] 2.1 添加 `ToolProfile` 类型和 `ToolProfileRegistry`
- [ ] 2.2 将所有当前支持的工具映射到显式的配置文件条目
- [ ] 2.3 将配置文件查找连接到命令适配器解析和 skill 路径解析
- [ ] 2.4 用清单派生的值替换硬编码的检测数组（例如 `SKILL_NAMES`）

## 3. 转换流水线

- [ ] 3.1 引入转换接口（`scope`、`phase`、`priority`、`applies`、`transform`）
- [ ] 3.2 实现具有确定性排序的转换运行器
- [ ] 3.3 将 OpenCode 命令引用重写迁移到转换流水线
- [ ] 3.4 从 `init` 和 `update` 中移除临时的转换调用

## 4. artifact 同步引擎

- [ ] 4.1 创建共享的 artifact 同步引擎，用于生成 planning + 渲染 + 写入
- [ ] 4.2 将引擎集成到 `init` 流程中
- [ ] 4.3 将引擎集成到 `update` 流程中
- [ ] 4.4 将引擎集成到遗留升级的 artifact 生成路径中

## 5. 验证和测试

- [ ] 5.1 添加清单完整性测试（必需元数据字段、命令 ID、目录名称）
- [ ] 5.2 添加工具配置文件一致性测试（skillsDir 支持和适配器/配置文件对齐）
- [ ] 5.3 添加转换适用性/顺序测试
- [ ] 5.4 扩展代表性 workflow/工具矩阵的校验测试
- [ ] 5.5 运行完整测试套件并验证生成的 artifact 保持稳定

## 6. 清理和文档

- [ ] 6.1 迁移后移除被取代的辅助代码和重复的写入循环
- [ ] 6.2 更新内部开发者文档，关于 template 生成架构
- [ ] 6.3 记录未来 workflow/工具添加的迁移指南
