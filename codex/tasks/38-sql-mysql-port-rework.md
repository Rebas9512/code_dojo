# 38-sql-mysql-port-rework：5 道 MySQL 改写题改成真 MySQL 写法

## 背景

任务 33（SQL 主线加厚）写了 5 道"把 MySQL 改成 PostgreSQL"的改错题：
- `problems/sql/1/sql-1-113-catalogue-list-port`
- `problems/sql/1/sql-1-115-runner-up-proof-load`
- `problems/sql/1/sql-1-117-quoted-rack-label`
- `problems/sql/2/sql-2-102-phone-fallback`
- `problems/sql/2/sql-2-112-next-day-color-check`

主控验收时发现，它们的 `starter.sql` 是"注释里保留 MySQL 片段 + 下面一条已经翻译成 PostgreSQL、只是参数顺序错了的译稿"，练不到方言迁移。33 的报告里这样解释："这样既练迁移，也符合可见样例必须跑出错误结果的判题合同"。也就是说，`scripts/curriculum/verify_sql.py` 要求 fix 题的 starter 在样例上能跑、而且结果和参考解不同，starter 报错不被允许，codex 33 只好这样凑。

用户 2026-11-23 同意返工："你说之前还有5道mysql的题是不是要优化一下这个也可以一起做了"。

## 要做的事

1. **5 道题的 starter 改成真正的 MySQL 写法**，在 PostgreSQL（PGlite）上运行会报错。学习者看着报错，把它改成 PostgreSQL 写法。每道题突出题意相关的 1–2 个方言差异，比如：
   - 反引号标识符 → 双引号或不加引号；
   - `IFNULL` → `COALESCE`；
   - `LIMIT 偏移, 条数` → `LIMIT 条数 OFFSET 偏移`；
   - `GROUP_CONCAT(... SEPARATOR ...)` → `STRING_AGG`；
   - `DATE_ADD(d, INTERVAL 1 DAY)` → `d + INTERVAL '1 day'`；
   - 字符串用双引号 → 单引号。
   
   先读每道题现有的 statement、starter、参考解、tests 和 33 报告里的说明，保留题意和参考解。参考解、数据集、期望结果能不改就不改。
2. **题面和提示**（`statement.md`、`problem.yaml` 的 hints）：
   - 题面说明这是一段 MySQL 查询，放到 PostgreSQL 上会报错，要改成 PostgreSQL 写法、结果不变。
   - 提示按"先看报错指向哪个词 → 这个词在 PostgreSQL 里叫什么 → 完整对应写法"递进。
   - 题干中文，学习者要输入的内容用英文（见 `docs/problem-format.md` 的语言约定）。
3. **判题合同**：给 fix 题加一种"starter 预期在 PostgreSQL 上报错"的标记，只给这类方言迁移题用。`verify_sql.py` 对带这个标记的题改为检查：starter 在样例上**必须**报错，参考解照常通过；不带标记的 fix 题保持现有规则。
   - 标记的字段名和取值自己定，写进 `docs/problem-format.md`（升格式版本号并写清楚改了什么）。
   - 后端加载题目的 pydantic 模型（`server/app/problems.py` 的 `ProblemMeta`）要认这个字段。
   - 想想 `scripts/curriculum/check_curve.py` 是否也要认，需要就改。
4. `problems/sql/skills.yaml` 或相关的课里，如果有"方言迁移"技能的讲解，看看是否需要补一张 MySQL → PostgreSQL 对照小表。需要就补，不要大改。

## 不做

- 不改别的题，不改题号（做题记录按 id 存）。
- 不碰平台代码里和这次无关的部分。前端不用改，SQL 报错本来就会显示在"测试结果"和"问题"里。
- 别的任务的文件不要动，比如 `web/src/components/` 下的做题页、`server/app/ai/`。

## 验收标准

- `cd server && .venv/bin/python ../scripts/curriculum/verify_sql.py`（具体跑法看脚本开头说明或 `docs/README.md`）：SQL 全部通过，课示例全部通过，这 5 道题的 starter 被确认会报错。
- `server/.venv/bin/python scripts/curriculum/check_curve.py` 0 错 0 警。
- `cd server && .venv/bin/python -m pytest -q` 全过（7 个会建临时 git 仓库的同步测试可以按标准做法排除，报告里写明）。
- `cd server && .venv/bin/python ../scripts/verify_bank.py --judge local --jobs 4` 全库通过。
- 在报告里逐题列出：原 starter、新 starter、在 PGlite 上的实际报错信息（一行），以及参考解。
