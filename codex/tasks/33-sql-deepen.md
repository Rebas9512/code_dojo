# 33 · SQL 主线加厚：阶段 1–5 补阶梯、补免费题、补改错题（约 +70 题）

## 背景

用户 2026-11-23 的原话：
- "话说sql的题库是不是挺少的 这边处理优化的时候可以去帮我看看sql题库有没有什么可以扩充的track之类的"
- 主控给了四条建议，用户回复："好那就做123先吧"。这是第 2 条。

**现状**（主控 2026-11-23 统计）：

| 阶段 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 题数 | 54 | 15 | 21 | 21 | 20 | 11 |

题型分布：write 56、complete 44、combine 27、variant 7、fix 5、inspect 3。

几个技能的题明显不够：

| 技能 | 题数 |
|---|---|
| `sql.window-frame` | 2 |
| `sql.lag-lead` | 2 |
| `sql.gaps-islands` | 3 |
| `sql.median` | 2 |
| `sql.pivot` | 2 |
| `sql.generate-series` | 1 |
| `sql.recursive-cte` | 1 |
| `sql.correlated-subquery` | 2 |
| `sql.exists` | 3 |
| `sql.set-ops` | 4 |
| `sql.dml` | 1 |

阶段 1–5 大多只有"一道引入 + 一道独立写"，没走完阶梯。

**并行**：
- 32 号任务同时在做新线 `problems/analytics/`（产品分析 SQL：留存、漏斗、会话、增长核算、实验）。留存、漏斗、会话切分的深入练习归 32。这里阶段 5 的这些技能只补到"补全 + 独立写 + 改错"各一道，不要做成一大串。
- 一个 Opus 子代理在清理 `server/app/`、`web/src/`。

你只负责下面这些：
- `problems/sql/1/` 到 `problems/sql/5/` 的题；
- `problems/sql/lessons/sql-1-*` 到 `sql-5-*`；
- `problems/sql/skills.yaml` 里阶段 1–5 的条目；
- `problems/sql/_db/bookstore/`：只追加行或新表，不改已有的行；
- `docs/curriculum.md` 第 7 节阶段 1–5；
- `docs/teaching-design.md` 的 SQL 误解目录；
- `check_curve.py` 识别表加行（只加不改）。

阶段 0 不动，平台代码不动。

先读：
- `codex/PLAN.md`；
- `docs/problem-format.md` 的 SQL 部分，包括 `mode: dml`；
- `docs/curriculum.md` 第 7 节；
- 05、09 号任务的报告 `codex/runs/05-sql-s1-2-*/report.md`、`codex/runs/09-sql-s3-5-*/report.md`；
- 阶段 1–5 已有的题和课。

## 要做的事

### 1. 补阶梯

上表里题少的技能，以及 `sql.conditional-agg`、`sql.string-agg`、`sql.having`、`sql.left-join`、`sql.anti-join`、`sql.self-join`、`sql.top-n-per-group`、`sql.rank`，都补齐"补全 → 独立写 → 改错 / 变式 / 组合"。

`sql.dml` 加 UPDATE、INSERT … SELECT、带子查询的 DELETE 各至少一道，用现有的 `mode: dml`。

### 2. 补 LeetCode 免费数据库题

范围是 SQL 50 以外、**免费**（非会员）的经典数据库题，约 30–40 道。要求：
- 用 `leetcode: <slug>` 标出处；
- 题面、表名、数据都自己写，做成原创同构题；
- 按"用到的最高概念"放进阶段 1–5。

**免费状态要核实**：可以用公开的 `https://leetcode.com/graphql` 查 `paidOnly`（研究笔记就是这么查的），查询方式和结果写进报告。

**已经做过的不要重复**：比如 176、177、178、180、184、185、196、197、601、1757。`grep -h '^leetcode:' problems/sql/*/*/problem.yaml` 可以列出已有的。

### 3. 补改错题

至少 15 道 `format: fix`，分到各阶段。starter 里的错误要在可见样例上就能看出来，规则见格式文档。错误集中在面试常见的坑上：
- `NOT IN` 碰到 NULL；
- `COUNT(col)` 和 `COUNT(*)`；
- 本该用 HAVING 却写在 WHERE；
- LEFT JOIN 后在 WHERE 里过滤右表，变成了内连接；
- 一对多连接后 SUM 被放大；
- 并列时 ROW_NUMBER 和 RANK 用错；
- 整数除法；
- 日期区间的右端点；
- 窗口漏了 PARTITION BY；
- LAG 的默认值。

另做一组"MySQL 写法改成 PostgreSQL"的改错题：`IFNULL`、`DATE_ADD`、`LIMIT x, y`、`GROUP_CONCAT`、反引号。网上参考解大量用 MySQL，这组题专门练这个。

### 4. 课

新技能或新错误需要讲解的，在对应阶段的课文件里加步骤（read / example / quiz）。每个技能只在一个文件里讲。

## 编号

- **已有题的 id 一律不改**：用户的做题记录按 id 存。
- **新题的题号**：每个阶段 NNN 从 101 起，比如 `sql-4-101-…`。
- **order**：可以在阶段 1–5 内重新排，让阶梯连贯。只改 order 字段，不改目录名。

## 通用要求

- 每题一个可见样例 + 至少 2 个隐藏数据集。数据集要求同 09：
  - 窗口题覆盖并列、单行分区、NULL 排序；
  - 连续区间覆盖断档、单天、跨月。
- 每题 2–4 条 `wrong_examples`。
- 题面中文；表名、列名、输出列名用英文。
- **不写防御性代码**：参考解写成面试里该写的样子。

## 验收标准

1. `python3 scripts/curriculum/verify_sql.py` 全过（SQL 全线）。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track sql`：0 错 0 警，SQL 50 计划覆盖照旧 50/50。
3. 后端测试照旧通过。
4. 报告里列出：
   - 每阶段新增题数和题型统计；
   - 上表那些技能补完后的题数；
   - 新增的 LeetCode 免费题清单（slug + 对应题号）和免费状态核实方式；
   - 对书店库的改动。
