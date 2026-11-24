# 60-tutor-scratch：助教看得到草稿，也能参与编辑草稿

## 背景

用户 2026-11-23："我想agent也能看到当前scratchpad和参与共同编辑"。

现状：
- 助教（`server/app/ai/tutor.py`、`main.py` 的聊天接口、前端 `web/src/components/ChatPanel.tsx`）能看到题目、课、答案编辑框和最近一次运行结果。
- 助教回复里的 `edits`（`old` / `new`）由前端写进**答案编辑框**，可以 Ctrl+Z 撤销，并记入"AI 协助 N 行"。
- 草稿标签（`scratch.py` / `scratch.sql`，任务 35、39）在 `web/src/components/ProblemWorkspace.tsx`：每道题都有，存在 localStorage 的 `dojo-scratch:<题号>`，第一次打开时才挂载编辑器。当初设计成助教只改答案，现在要放开。
- 助教走 Claude 和 Codex 两种 agent，结构化输出的 schema 在 `tutor.SCHEMA`，Codex 会把它转成严格 schema（`server/app/ai/codex_schema.py`）。

## 要做的事

1. **请求**：聊天请求带上草稿当前内容，`scratch` 字段，可以为空，长度上限和 `code` 一样。
2. **提示词**：
   - 在 `tutor.py` 的上下文里加一段"草稿（不判题）"，带行号，和答案的格式一致。草稿为空时写"（空）"。
   - 系统提示补一段规则：草稿是学习者随手试代码的地方，不判题、不计入作答。适合在草稿里放演示片段、小实验、打印中间结果；答案编辑框里只做学习者要的修改。教学约束（分级提示、不直接给完整答案）照旧只针对答案。
3. **edits 加目标**：每条 edit 加 `target`，取值 `"answer"` 或 `"scratch"`。
   - 服务端 `tutor.check` / `apply_edits` 按目标核对：`old` 要在对应文本里唯一出现，或者为空表示追加。
   - Codex 的严格 schema 转换要能处理这个枚举字段。
   - 旧聊天记录里没有 `target` 的 edit，一律当成 `answer`。
4. **前端应用**：
   - `ActiveProblem.applyEdits` 按目标分别写：
     - `answer`：和现在一样；
     - `scratch`：写进草稿编辑器，要能 Ctrl+Z 撤销，标出 AI 写入的行。草稿编辑器还没挂载时，先打开草稿标签再应用，或者先改文本再挂载，选简单可靠的做法。
   - 改了草稿就切到草稿标签，让学习者看见变化。
   - 改草稿**不计入**"AI 协助 N 行"，也不影响这题是否算独立完成。
   - ChatPanel 发消息时带上草稿当前内容，取最新文本，不是挂载时的快照。
5. **聊天记录**：助教回复下面显示改了哪里，比如"改了答案 2 处 / 草稿 1 处"，沿用现有的展示方式。
6. **文档**：`docs/README.md` 写助教和共享编辑框的地方补上草稿。只用小补丁改这一节。

## 并行约束（任务 59「访客模式」同时在跑）

- 59 改的是 `bootstrap/`、`desktop/`、`scripts/desktop/`、`deploy/README.md`、同步相关代码，以及前端的 `SyncStatus` 和桌面设置。**这些都不要碰。**
- `server/app/main.py`、`web/src/api.ts`、`docs/README.md` 两边都可能改：只用小补丁改聊天相关的部分，不整文件重写。
- 测试实例端口用 **后端 8031、前端 5201**。

## 不做

- 不改附加题出题，不改判题。
- 不调用真实 AI（标准做法第 4 条），用 FakeProvider 测。真实冒烟由主控做。

## 验收标准

- `cd server && .venv/bin/python -m pytest -q` 全过（7 个会建临时 git 仓库的同步测试可以按标准做法排除）。新增测试覆盖：
  - 提示词里有草稿段；
  - `target=scratch` 的 edit 按草稿文本核对；
  - 没有 `target` 的旧记录当成 `answer`；
  - Codex 严格 schema 包含 `target` 枚举。
- `cd web && npm run build` 通过。
- 起测试实例（8031 / 5201，`CODE_DOJO_AI_PROVIDER` 用测试里的 FakeProvider 注入方式或假 agent 脚本）。用 Playwright 验证并截图：
  1. 草稿里写一段代码后发消息，请求体里带着草稿内容；
  2. 假助教回一条 `target=scratch` 的修改：草稿标签自动打开，内容改了，Ctrl+Z 能撤销，"AI 协助"的行数不变；
  3. 回一条 `target=answer` 的修改：行为和现在一样。
- 报告里给一条主控可以直接跑的真实冒烟命令（Claude 和 Codex 各一次）：让助教"在草稿里写一个打印中间结果的例子"，检查回复里有 `target=scratch` 的 edit。
