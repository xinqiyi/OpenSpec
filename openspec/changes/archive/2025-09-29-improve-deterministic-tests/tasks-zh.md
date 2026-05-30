# 实施任务

## 1. 测试隔离
- [x] 1.1 为每个测试套件创建临时夹具根目录（openspec/changes、openspec/specs）
- [x] 1.2 在测试中使用 process.chdir 切换到临时根目录
- [x] 1.3 每个测试后恢复原始 cwd 并清理临时目录

## 2. 确定性发现
- [x] 2.1 实现 getActiveChangeIds(root?)，仅包含带有 proposal.md 的目录
- [x] 2.2 实现 getSpecIds(root?)，仅包含带有 spec.md 的目录
- [x] 2.3 返回排序结果以避免 fs.readdir 排序差异

## 3. 命令集成
- [x] 3.1 确保 change/show/validate 依赖于 cwd 和发现辅助函数
- [x] 3.2 保持运行时行为对最终用户不变

## 4. 验证
- [x] 4.1 将受影响的命令测试（show、spec、validate、change）转换为隔离夹具
- [x] 4.2 验证测试在不同环境中一致通过
- [x] 4.3 确认测试期间不从真实 repository 状态读取

## 5. 可选（现在不需要）
- [x] 5.1 为发现辅助函数添加可选的 root 参数（默认为 process.cwd()）
