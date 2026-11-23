# 39-scratch-everywhere：每道题都有草稿标签

## 背景

任务 35 给做题页加了草稿标签（`scratch.py` / `scratch.sql`，Alt+S 切换，只看输出不判题），但预测题（`mode === 'predict'`）和看数据题（`format === 'inspect'` 或 `language === 'none'`）上没有。用户在 Windows 上试用时以为草稿没加载出来，然后说：

"哦就是有些题题是没草稿的 不过我想做成每题都有草稿这样 有时候讨论的时候我也想打开草稿写点东西这样"

相关代码：`web/src/components/ProblemWorkspace.tsx` 的 `ActiveProblem`：`hasScratch`、`switchFile`、`runCurrent`、文件标签条 `.file-tabs`、`#answer-editor` / `#scratch-editor`、窗口级快捷键 `onKey`。草稿运行走 `api.playground`（Python）和 `sql/client` 的 `runExample(setup, sql)`（SQL）。

## 要做的事

1. **所有题都显示草稿标签**，`hasScratch` 只要求题目已加载（`!!p`）。
2. **草稿用什么语言**：
   - SQL 线（`p.language === 'sql'`，包括看数据题）用 `scratch.sql`。
   - 其他一律用 `scratch.py`，包括认识数据线（`language === 'none'`）和预测题。
   - Python 草稿走 `api.playground(code, '', id)`，后端按题所在线的 runtime 选解释器，不用改后端。
3. **SQL 草稿的数据库**：
   - 普通 SQL 题照旧取 `api.sqlCases(id, 'sample')` 的第一个数据集。
   - SQL 线的看数据题先查清楚它有没有可用的数据集：`sqlCases` 对看数据题能不能用？题目详情里的 `datasets` 字段是什么？有就用这道题的数据。没有就用 SQL 线的书店练习库（课里的示例怎么建库就照着做，看 `LessonView` 和后端课接口返回的 `setup`）。实在都拿不到就用空库，报告里写清楚选了哪种。
4. **看数据题的右侧**：
   - 原来只有 `.inspect-answer`（选项或短答案）。现在标签条显示答案标签（沿用现在的 `answer` 名称和表格图标）和草稿标签，切到草稿时显示草稿编辑器，隐藏答案区，切回来时答案区状态不变。
   - 草稿激活时显示"运行"按钮；答案标签激活时，看数据题照旧不显示"运行"。
5. **快捷键**：
   - 草稿激活时，Ctrl+Enter 一律运行草稿。
   - 答案标签激活时，看数据题的 Ctrl+Enter 照旧是提交；其他题照旧运行样例。
   - Ctrl+Shift+Enter 永远提交答案。
   - Alt+S 在所有题上可用。
   - 看数据选择题的数字键 1–9 选项：焦点在草稿编辑器里时不能触发，现在的过滤条件应该已经排除了 textarea，确认一下。
6. **预测题**：左边照旧显示程序，草稿可以运行。不加任何限制，用户自己把握。
7. **文档**：`docs/README.md` 里写草稿的那句改成"每道题都有"。只用小补丁改这一处。

## 不做

- 不改助教，助教不读草稿内容。
- 不改后端，除非第 3 条确实需要一个小接口。需要的话在报告里说明。
- 不改别的页面。

## 验收标准

- `cd web && npm run build` 通过。
- `cd server && .venv/bin/python -m pytest -q` 全过（7 个会建临时 git 仓库的同步测试可以按标准做法排除）。
- 起测试实例（后端 8001、前端 5174，`CODE_DOJO_AI_PROVIDER=off`，`CODE_DOJO_JUDGE=local`，独立数据目录），用 Playwright 逐项验证并截图放 `{RUN_DIR}/`：
  1. 预测题（如 `py-0a-002-predict-variables`）：有 `scratch.py`，写 `print(1 + 1)` 按 Ctrl+Enter，输出 2；切回答案，`answer.txt` 内容还在。
  2. 认识数据线的看数据题（如 `data-0-001-count-register`，选择题和短答案题各一道）：有 `scratch.py` 标签；切过去写 Python 能运行；切回答案，已选的选项或已填的短答案还在；答案标签上 Ctrl+Enter 仍然是提交。焦点在草稿编辑器里按数字键 1，不会改选项。
  3. SQL 线的看数据题：有 `scratch.sql`，运行 `SELECT 1 AS x;` 出结果表；如果用了这道题或书店库的数据，再查一张真实的表。
  4. 普通 Python 题和 SQL 题的草稿行为不变（回归任务 35 的验收 1–6）。
- 报告里写明第 3 条的数据库选了哪种、为什么。
