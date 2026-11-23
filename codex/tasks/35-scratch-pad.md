# 35-scratch-pad：做题页加草稿标签（scratch pad）

## 背景

用户 2026-11-23 原话："我现在想增加一个功能 就是在answer这个写代码的tab旁边加一个scratch pad 这样我可以中途运行一些和答案无关的测试内容或者中间内容什么的看结果这样"

做题页右侧编辑区（`web/src/components/ProblemWorkspace.tsx` 里的 `.wb-code`）现在只有一个文件标签 `solution.py` / `query.sql`。要在它旁边加一个草稿标签，用来随手跑一段和答案无关的代码、看输出，不判对错、不记作答。

能复用的现成接口（课里的"运行示例"就在用，见 `web/src/components/LessonView.tsx` 的 `ExampleStep.run`）：
- Python：`api.playground(code, stdin, problemId)` → `POST /api/playground/run`。按题所在线的 runtime 选普通解释器或数据科学环境，普通 Python 限时 3 秒。
- SQL：`(await import('../sql/client')).runExample(setup, sql)`。在 PGlite Worker 里事务内执行，跑完回滚，返回最后一条语句的结果表。这道题的建库语句从 `api.sqlCases(id, 'sample')` 取第一个数据集的 `setup`。

**这个任务预计只改前端，不改后端。** 确实要动 `server/` 的话，在报告里写清楚原因。

## 要做的事

1. **标签**。`.file-tabs` 里现有的 `active-file` 改成两个可点击的标签：
   - 答案标签：文件名照旧（`solution.py` / `query.sql`）。
   - 草稿标签：`scratch.py` / `scratch.sql`。
   - 样式跟左栏标签一致：激活的那个有上边框高亮。codicon 选一个合适的，比如 `beaker` 或 `note`。
   - 预测题（`mode === 'predict'`）和看数据题（inspect / `language === 'none'`）不显示草稿标签。预测题能跑程序就失去意义了。
2. **两个编辑器各自独立**。答案和草稿各一个 `CodeEditor` 实例，只显示当前标签那个，另一个隐藏但不卸载，这样切换时撤销栈和光标都在。
   - 切换方式：点标签；另外在命令面板加一条"切换答案 / 草稿"。快捷键选一个不和现有冲突的（现有快捷键看 `ProblemWorkspace.tsx` 和 `CodeEditor.tsx`），写进报告。
   - 裸写模式对草稿同样生效。
   - 状态栏的"行 / 列"跟随当前显示的编辑器。
3. **助教只改答案**。`applyEdits`、`editorRef`、`getCode` 必须始终指向答案编辑器。草稿用另一个 ref。底部面板"问题"里点行号跳转，也只跳答案编辑器。
4. **运行**。草稿标签激活时：
   - 顶栏"运行"按钮和 Ctrl+Enter 运行草稿：Python 走 playground，SQL 走 `runExample(setup, sql)`。
   - "提交"按钮和 Ctrl+Shift+Enter 永远提交答案。
   - 草稿运行不调 `api.run` / `api.submit`，不记作答、不影响计时、提示数和 AI 行数。
   - 答案标签激活时，"运行"照旧运行样例。
   - 数据科学线运行时，照旧显示 `runStatus`（`DsPreparation`）。SQL 草稿第一次运行前要 `prepare()`，和现在一样显示"正在准备数据库…"。
5. **输出**。草稿的运行结果进底部面板的"输出"标签：运行时自动打开面板并切到"输出"。
   - Python：显示 stdout 和 error，再加上状态和耗时，比如 `超时`、`运行错误 · 12 ms`。
   - SQL：显示结果表（用现有的 `SqlTableView`），出错显示错误文字。
   - 来源标签：`WorkbenchPanel` 现在写死了"课 · 示例"。改成按来源显示"课 · 示例"或"草稿"。课示例和草稿共用一个 `output` 槽，后跑的覆盖先跑的。做法自己定，比如 `ExampleOutput` 加一个 `source` 字段。
6. **保存**。草稿按题保存到 localStorage，键名 `dojo-scratch:<题目 id>`，用现有的 `readPref` / `writePref`，和答案草稿 `dojo-draft:` 同一套写法。
   - 复习模式（`isReview`）也保留草稿，草稿不算作答。
   - 初始内容为空，空编辑器上显示一行占位提示：`随手试代码，不判题`。
   - "重置代码"只重置答案，不清草稿。
   - 附加题按自己的 id 单独存。删除附加题时，在 `removeExtra` 里把它的 `dojo-scratch:` 一起清掉。
7. **文档**。在 `docs/README.md` 写到做题页功能的地方补一两句，说明草稿标签是什么、怎么运行。写"现在是什么样"，不写变更日志。

## 这次不做

- 不把答案代码拼进草稿，草稿就是独立的一份代码。
- 不给草稿加 stdin 输入框。
- 不做多个草稿文件。
- 不改助教的提示词，也不改助教能看到的内容。
- 不动 `desktop/`、`bootstrap/`、`.github/`、`problems/`。

## 验收标准

- `cd web && npm run build` 通过（tsc + vite）。
- `cd server && .venv/bin/python -m pytest -q` 全过（没改后端也跑一次，报数字）。
- `node web/tests/sql.test.mjs`（或者它原本的跑法）照旧通过。
- 起测试实例（后端 8001，`CODE_DOJO_AI_PROVIDER=off`，`CODE_DOJO_JUDGE=local`；前端 5174），用 Playwright 实际走一遍下面几项，截图放 `{RUN_DIR}/`：
  1. 打开一道 Python 写函数题，比如 `python/` 线早期的 write 题。切到 `scratch.py`，写 `print(sum(range(10)))`，按 Ctrl+Enter。底部"输出"显示 `45`，来源是"草稿"；"测试结果"不变。
  2. 切回 `solution.py`，答案内容和光标都还在。在答案里 Ctrl+Z，不会撤销到草稿的内容。
  3. 刷新页面，草稿内容还在。
  4. 打开一道 SQL 题，比如 `sql/` 阶段 0 的一道 query 题。在 `scratch.sql` 里写 `SELECT 1 AS x;`，运行后输出显示结果表。再写一个查询这道题自己表的 SELECT，能看到真实数据。
  5. 打开一道预测题，没有草稿标签。打开一道看数据题，也没有。
  6. 草稿标签激活时点"提交"，提交的是答案（看请求体或"测试结果"）。
- 报告里写出新的快捷键，并逐项写清以上 1–6 的结果。
