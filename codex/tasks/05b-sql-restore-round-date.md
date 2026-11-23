# 05b · SQL 阶段 1–2：把绕开日期和舍入的 7 道题改回原题考法

## 背景

05 号任务写 SQL 阶段 1–2 时，阶段 0 还没有题引入 `sql.date-funcs`（日期函数）和 `sql.round-cast`（ROUND 和类型转换）。所以有 7 道 SQL 50 改编题用题内视图或"恰好整除"的数值绕开了它们。

06b 号任务已经在阶段 0 补上了这两个技能的引入题。主控决定：这 7 道题改回原题的考法，让学习者真的练到舍入和取年月。

题目清单和各自"复查哪一点"见 `codex/runs/06b-intro-gaps-*/report.md` 的「05 号任务中绕开日期和舍入的题」表：
- sql-1-012
- sql-1-011
- sql-2-011
- sql-2-014
- sql-2-016
- sql-2-018
- sql-2-021

**并行**：09（SQL 阶段 3–5）、10（Python 0B）、12（算法阶段 3）、11（平台 M4）可能在同时跑，先读 `codex/PLAN.md`。你只改这 7 道题的目录，以及它们在 `docs/curriculum.md` 里的说明。

## 要做的事

- **sql-1-012**：去掉样例脚本里预先算好 `bill_month` 的视图，让学习者从原始日期列自己求年月并分组，比如 `TO_CHAR(paid_on, 'YYYY-MM')` 或 `date_trunc`。
  - 题面写清楚输出格式。
  - `requires` 加 `sql.date-funcs`。
- **另外 6 道**：
  - 题面写明保留几位小数（照原题）。
  - 至少一个隐藏数据集要让不舍入的写法、舍入位数不对的写法都判错：要有循环小数或者多一位的情况。
  - `requires` 加 `sql.round-cast`。
  - 注意 PostgreSQL 的 `ROUND(double precision, int)` 不存在，要先转 numeric。这正是常见误区：课里已经讲过的话，`wrong_examples` 里加一条"整数除法没转类型"或"忘了舍入"。
- **每道题**：
  - `wrong_examples` 加一条"忘了 ROUND"或"没转换日期"的写法，并确认它在隐藏数据集上判错。
  - 样例数据集的期望输出同步改好，题面里如果有示例结果也同步。
- **文档**：`docs/curriculum.md` 第 7 节对应位置，如果写过"绕开"的说明就删掉，改成现在的考法。

## 验收标准

1. `python3 scripts/curriculum/verify_sql.py --only sql-1` 和 `--only sql-2` 全过，新加的错误写法都在隐藏数据集上判错。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track sql`：阶段 1–2 范围内 0 错 0 警。
3. 报告里逐题写改了什么。
