# OpenSpec 测试指引

适用于 `test/` 下的测试。

## 运行测试

- 聚焦单个文件：`pnpm exec vitest run test/path/to/file.test.ts`
- 聚焦单个用例：`pnpm exec vitest run test/path/to/file.test.ts -t "用例名称"`
- 完整套件：`pnpm test`
- 在聚焦 CLI 测试前运行 `pnpm run build`，当实现变更可能导致 `dist/` 过时时。

## 路径规范化

路径标识是一个反复出现的 CI 故障模式：Windows 短/长路径、符号链接或交接点别名以及不区分大小写的文件系统可能以不同方式拼写同一现有目录。

当断言现有文件系统路径作为标识时，请先规范化实际路径和期望路径。在项目代码中优先使用 `FileSystemUtils.canonicalizeExistingPath()`，在仅测试的期望中使用 `fs.realpathSync.native()`。

在涉及路径标识逻辑时，添加别名路径回归测试。如果保留用户输入的路径拼写是有意为之，请将其与标识比较分开断言。
