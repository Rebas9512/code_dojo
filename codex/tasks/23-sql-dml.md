# 23 · 平台：SQL 修改类题（DELETE / UPDATE / INSERT）的判题模式

## 背景

09 号任务报告：SQL 50 里的 `delete-duplicate-emails` 要求写 DELETE。平台目前只判只读查询，所以 09 把它做成了：
- `sql-3-020`：用查询生成 DELETE 清单；
- `sql-3-021`：查询去重后的通讯录。

这次加一种"修改类"判题：执行学习者的修改语句，然后用一条检查查询看表的最终状态，和参考解执行后的状态比对。

现有 SQL 判题的实现见 07 号任务的交付：`codex/runs/07-sql-judge-*/report.md`。
- 浏览器 Worker 里用事务回滚隔离每个数据集；
- 服务器上用 Node PGlite 预先算出期望结果；
- 前后端共用一个比较模块。

**并行**：18（数据处理线内容）和 14（算法阶段 4）在同时跑，先读 `codex/PLAN.md`。你是唯一的平台任务，但不要动 `problems/wrangle/` 和 `problems/algo/`。

## 要做的事

1. **格式**（`docs/problem-format.md` 升版本）。SQL 题可以写：

   ```yaml
   mode: dml
   check_query: SELECT id, email FROM person ORDER BY id   # 修改后用它读表状态
   ordered: true
   ```

   - 学习者提交的是一条 DELETE、UPDATE 或 INSERT（也允许 WITH … DELETE 这种写法），只能一条语句。
   - 判题流程：建库 → 执行学习者的语句 → 执行 `check_query` → 比对 → 回滚。
   - 参考解同样执行后取 `check_query` 的结果作为期望。
   - 结果面板显示"修改后的表"和"期望的表"，另外显示"影响了 N 行"。
2. **浏览器 Worker**：
   - 只读题照旧只允许 SELECT 或 WITH。
   - `mode: dml` 的题只允许单条 DELETE、UPDATE、INSERT。DROP、TRUNCATE、ALTER、事务控制语句一律拒绝，并给中文提示。
3. **服务器**：期望结果的计算和缓存支持 dml。`verify_sql.py`、`verify_bank.py` 支持 dml：
   - 参考解要真的改到了表，也就是修改前后 `check_query` 的结果不同；
   - `wrong_examples` 在某个隐藏数据集上和参考解的结果不同。
4. **附加题**：SQL 附加题的出题 schema 允许 dml 题，验证规则同上。
5. **内容**：把 `sql-3-020` 改成真正的 DELETE 题（dml 模式），题面、`wrong_examples`、数据集同步改。`sql-3-021`（查询版）保留，作为它前面的阶梯。
   - 这两道题在 `problems/sql/3/`，这次归你改。
   - `docs/curriculum.md` 对应位置同步。
6. **测试**：
   - 后端：dml 的期望计算、拒绝非法语句、错误写法判错。
   - 前端：比较模块的测试，加 dml 用例。

## 验收标准

1. `server/.venv/bin/python -m pytest -q` 全过，前端测试全过，`npm run build` 通过。
2. `python3 scripts/curriculum/verify_sql.py --only sql-3` 全过，SQL 全部题照旧通过。
3. 起 8001 和 5174 测试实例，在浏览器里做 `sql-3-020`，截图放 `{RUN_DIR}/`：
   - 写对的 DELETE：通过，显示修改后的表；
   - 少了条件的 DELETE（删多了）：判错，能看出删多了哪几行；
   - 尝试 DROP TABLE：被拒绝，有中文提示。
4. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
