# 06b · 补缺：有技能没有引入题的地方

## 背景

05 号任务的报告发现：SQL 阶段 0 的日期函数（`sql.date-funcs`）、ROUND 和类型转换（`sql.round-cast`）已经有课，但阶段 0 没有任何一道题 `introduces` 它们。结果是后面阶段用到它们时，只能绕开。

学习曲线检查现在不查这种情况：一个技能在技能图里、有课，却没有题引入它。

**并行**：08（算法阶段 2）、09（SQL 阶段 3–5）、10（Python 0B）、11（平台 M4）可能在同时跑，先读 `codex/PLAN.md`。

你名下的东西：
- SQL 阶段 0 的题，题号 `sql-0-150…199`，以及阶段 0 的 order 调整。
- 下面第 1 步查出来的、Python 0A 和根线 `data` 范围内的缺口题。Python 题号用 `py-0a-450…499`，根线用 `data-0-100…`。
- `check_curve.py` 里新加的那条检查。

## 要做的事

1. **先查全**：写个一次性脚本，脚本放 `{RUN_DIR}/`。在 data、python（0A）、sql（阶段 0–2）三处，列出满足下面全部条件的技能：
   - 所在阶段已经有题，
   - 没有任何一道题 `introduces` 它，
   - 它有知识卡或课，或者被别的技能当作前置。

   结果写进报告。算法线、SQL 阶段 3–5、0B 还在写，不查。
2. **补题**：给每个缺口技能补一套阶梯：
   - 引入题：通常是预测或补全，
   - 至少 1 道独立写，
   - 课里已经有讲解的就复用，没有就补上讲解、示例、小测。

   插进合适的位置，调 order，保证前后的 `requires` 依然成立。

   SQL 的 `sql.date-funcs`、`sql.round-cast` 至少要补上。补完以后，检查 05 号任务说的"绕开"的地方：阶段 1–2 那几道用题内视图或特殊数值绕开舍入、日期的题，在报告里列出来，由主控决定要不要改回直接用。不要改阶段 1–2 的题。
3. **加检查**：`check_curve.py` 加一条**警告**：活跃线里、所在阶段已经有题、但没有任何题引入的技能。规划中的线、还没有题的阶段不报。说明写进 `docs/curriculum.md` 第 5 节。
4. **文档**：`docs/curriculum.md` 对应小节同步题数，`docs/teaching-design.md` 有新误解就补上。

## 验收标准

1. 全部通过：
   - `verify_bank.py --only sql-0`
   - `verify_bank.py --only py-0a`（如果补了 Python 题）
   - `verify_bank.py --only data-`
   - `python3 scripts/curriculum/verify_sql.py --only sql-0`
2. `check_curve.py`：你范围内 0 错 0 警。新警告在 data、python 0A、sql 0–2 上为 0。其他线如果因此冒出警告，在报告里列出来，不要去修。
3. 报告里列出：查出的缺口清单、补的题、"绕开"的题清单。
