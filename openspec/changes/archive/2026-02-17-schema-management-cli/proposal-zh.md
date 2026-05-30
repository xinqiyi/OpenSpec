## 原因

创建和管理项目本地架构目前需要手动创建目录、复制文件，并希望结构正确。用户只有在运行时命令失败时才会发现结构错误。这种摩擦阻碍了架构自定义，并使定制 OpenSpec workflow 以满足特定项目需求变得更加困难。

关键痛点：
- **手动脚手架**：用户必须手动以正确的结构创建 `openspec/schemas/<name>/`
- **无验证反馈**：架构错误直到命令尝试使用该架构时才被发现
- **从零开始很困难**：没有简单的方法基于现有架构创建自定义架构
- **调试解析**：当架构未按预期解析时，无法查看解析路径

## 变更内容

添加一个新的 `openspec schema` 命令组，包含用于创建、派生、验证和检查架构的子命令。

### 命令

1. **`openspec schema init <name>`** - 引导式向导，用于脚手架新的项目架构
 - 提示输入架构描述
 - 提示选择要包含的 artifact（附带说明）
 - 使用 `schema.yaml` 和 template 文件创建有效的目录结构
 - 可选地设置为 `openspec/config.yaml` 中的项目默认值

2. **`openspec schema fork <source> [name]`** - 复制现有架构作为起点
 - 从用户覆盖或包内置复制
 - 允许重命名（默认为 `<source>-custom`）
 - 保留所有 template 和配置

3. **`openspec schema validate [name]`** - 验证架构结构和 template
 - 检查 `schema.yaml` 是否有效
 - 验证所有引用的 template 是否存在
 - 报告缺失或格式错误的文件
 - 不带名称运行时验证所有项目架构

4. **`openspec schema which <name>`** - 显示架构解析路径
 - 显示架构从哪个位置解析（project/user/package）
 - 显示架构目录的完整路径
 - 用于调试遮蔽问题

## 能力

### 新能力
- `schema-init-command`：用于创建新项目架构的引导式向导，带有引导提示
- `schema-fork-command`：将现有架构复制到项目以进行自定义
- `schema-validate-command`：在运行时之前验证架构结构并报告错误
- `schema-which-command`：通过显示使用了哪个位置来调试架构解析

### 修改的能力
<!-- 无 - 这些都是新增命令 -->

## 影响

- **代码**：使用现有解析器基础设施在 `src/commands/` 中实现新命令
- **CLI**：新的 `schema` 命令组，包含 4 个子命令
- **依赖**：可能在 `schema init` 中使用 `enquirer` 或类似的交互式提示
- **文档**：需要更新 CLI 参考和架构自定义指南
