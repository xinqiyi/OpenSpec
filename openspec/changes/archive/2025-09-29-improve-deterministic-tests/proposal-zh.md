# 变更：改进确定性测试（与 repository 状态隔离）

## 问题

一些单元测试（例如 ChangeCommand.show/validate）通过 `process.cwd()` 和 `openspec/changes` 读取实时 repository 状态。这使得结果依赖于碰巧存在的任何目录以及 `fs.readdir` 返回的顺序，导致不同环境下的成功/失败不稳定。

观察到的症状：
- 测试有时会选择部分或不相关的变更文件夹。
- 当选择到无关的变更目录时，会出现类似缺少 `proposal.md` 的失败。
- 环境/沙箱差异会改变 `readdir` 排序和工作器行为。

## 目标

- 使测试具有确定性和封闭性。
- 消除对真实 repository 内容和目录顺序的依赖。
- 保持运行时行为对最终用户不变。

## 非目标

- 引入重型框架或测试工具复杂度。
- 重新设计 CLI 行为或更改用户的默认路径。

## 方法

1) 测试本地夹具根目录
- 每个涉及文件系统发现的套件创建一个临时目录：
 - `openspec/changes/sample-change/proposal.md`
 - `openspec/changes/sample-change/specs/sample/spec.md`
- `beforeAll`：`process.chdir(tmpRoot)`；`afterAll`：恢复原始 cwd。
- 使用常量 `changeName = 'sample-change'`；消除对 `readdir` 顺序的依赖。

2) 命令的可选薄 DI（最小化，如果需要）
- 允许 `ChangeCommand`（及类似）接受可选的 `root` 路径（默认为 `process.cwd()`），用于路径解析。
- 测试显式传递临时根目录；生产代码保持不变。

3) 强化发现辅助函数（安全增强）
- 更新 `getActiveChangeIds()`/`getActiveChanges()`，仅包含包含 `proposal.md`（以及可选地至少一个 `specs/*/spec.md`）的目录。
- 防止不完整/无关的变更文件夹被视为活跃。

## 理由

- 小而专注的更改消除了不稳定性，而不改变用户 workflow。
- 临时夹具是一种广为人知的测试 schema，保持测试快速。
- 可选的构造函数 root 参数是最小的 DI 表面，避免了全局桩代码并保持代码简单。

## 风险与缓解

- 风险：测试忘记恢复 `process.cwd()`。
 - 缓解：添加恢复 cwd 的 `afterAll` 守卫；在修改 `process.exitCode` 的地方的 `afterEach` 中重置。
- 风险：如果 DI root 被误用，行为出现偏差。
 - 缓解：默认为 `process.cwd()`；仅测试传递自定义根目录。

## 验收标准

- 以前依赖 repository 状态的测试现在：
 - 创建并使用临时夹具根目录。
 - 执行期间不读取真实的 `openspec/changes`。
 - 无论目录顺序或无关文件夹如何，均一致通过。
- CLI 行为对最终用户无变化（路径仍默认为 cwd）。

## 推广

- 阶段 1：将触及 ChangeCommand.show/validate 的套件转换为隔离夹具；在本地和 CI 中验证稳定性。
- 阶段 2：将相同 schema 应用于任何剩下的触及文件发现的套件（`list`、`show`、`validate`、`diff`）。
- 阶段 3（可选）：引入构造函数 `root` 参数和发现强化，如果仅阶段 1 不够充分。
