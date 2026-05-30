## 1. 核心基础设施

- [x] 1.1 在 `src/core/config-schema.ts` 中创建全局配置的 zod schema
- [x] 1.2 添加点号记法键访问的工具函数（获取/设置嵌套值）
- [x] 1.3 添加类型强制转换逻辑（自动检测布尔值/数字/字符串）

## 2. 配置命令实现

- [x] 2.1 使用 Commander.js 创建 `src/commands/config.ts` 子命令
- [x] 2.2 实现 `config path` 子命令
- [x] 2.3 实现 `config list` 子命令并支持 `--json` 标志
- [x] 2.4 实现 `config get <key>` 子命令（原始输出）
- [x] 2.5 实现 `config set <key> <value>` 并支持 `--string` 标志
- [x] 2.6 实现 `config unset <key>` 子命令
- [x] 2.7 实现 `config reset --all` 并支持 `-y` 确认标志
- [x] 2.8 实现 `config edit` 子命令（启动 $EDITOR）

## 3. 集成

- [x] 3.1 在 CLI 入口点注册 config 命令
- [x] 3.2 更新 shell 补全注册表，包含 config 子命令

## 4. 测试

- [x] 4.1 所有子命令的手动测试
- [x] 4.2 验证 zod 校验拒绝无效的键/值
- [x] 4.3 测试使用点号记法的嵌套键访问
- [x] 4.4 测试类型强制转换的边界情况（true/false、数字、字符串）
