# 05c · SQL 阶段 0：补上计划里的 10 道 SQL 50 骨架题；检查脚本加"计划题必须真的有题"

## 背景

主控验收 09 号任务时核对了题目文件里的 `leetcode:` 字段：SQL 50 实际只覆盖了 40/50。缺的 10 道都在 `docs/curriculum.md` 第 7 节阶段 0 的计划里：

- `article-views-i`
- `big-countries`
- `find-customer-referee`
- `find-users-with-valid-e-mails`
- `fix-names-in-a-table`
- `invalid-tweets`
- `not-boring-movies`
- `patients-with-a-condition`
- `recyclable-and-low-fat-products`
- `triangle-judgement`

阶段 0 现有的 44 道题都没有 `leetcode:` 字段。可能是最早写的时候把其中几道改编成了书店题，但没有标出处；也可能根本没写。

`check_curve.py` 的"计划覆盖"只检查 curriculum.md 里的计划表，不检查题目文件里是不是真的有这些题，所以这个缺口没有报出来。

**并行**：05b（SQL 阶段 1–2 的 7 道题）、10（Python 0B）、12（算法阶段 3）、11（平台 M4）可能在同时跑，先读 `codex/PLAN.md`。

你名下的东西：
- SQL 阶段 0 的题：新题号 `sql-0-200…249`，以及阶段 0 的 order 调整、`leetcode:` 标注。
- `check_curve.py` 的计划覆盖检查。
- `docs/curriculum.md` 第 5 节和第 7 节阶段 0。

## 要做的事

1. **逐题对照**：10 道题每道查一遍阶段 0 现有的题。
   - 已经有一道是它的改编（同一个考点、同样的输入输出结构，只是换了书店场景），就给那道题补上 `leetcode: <slug>`，`source` 照格式文档填。
   - 没有就新写一道：题面自己写，数据可以用书店库，也可以自带小表。
   - 放在阶段 0 里该放的位置，按 curriculum.md 第 7 节阶段 0 的表；`requires` 和 `introduces` 照规则，order 调好。
   - 格式和测试密度同阶段 1–2 的题：样例 + 至少 2 个隐藏数据集，`wrong_examples` 至少 1 条。
2. **检查脚本**：`check_curve.py` 的计划覆盖加一层"实际覆盖"。
   - 对每条活跃线，如果某个阶段已经有题，计划表里列在这个阶段的骨架题，都必须在这个阶段的题目文件里有对应的 `leetcode:`。缺了报**错误**。
   - 还没有题的阶段不查。
   - 这条对算法线也生效：阶段 1–2 已经写完，要能过；阶段 3 正由 12 号任务在写，它的缺口报出来是正常的，写进报告，不要去修。
   - 规则写进 `docs/curriculum.md` 第 5 节。
3. **SQL 50 实际覆盖**：在报告里给出最终数字，应该是 50/50。

## 验收标准

1. `python3 scripts/curriculum/verify_sql.py --only sql-0` 全过。
2. `check_curve.py --track sql`：0 错 0 警，SQL 50 实际覆盖 50/50。
3. `check_curve.py --track algo`：阶段 1–2 的实际覆盖没有缺口。阶段 3 的情况写进报告。
4. 报告里给出 10 道题的处理方式：补标注的写对应哪道已有题，新写的写题号。
