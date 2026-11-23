# 34 · 新线「建模与写数据」（`modeling`）：多语句脚本判题 + 技能图 + 课 + 题

## 背景

用户 2026-11-23 的原话：
- "话说sql的题库是不是挺少的 这边处理优化的时候可以去帮我看看sql题库有没有什么可以扩充的track之类的"
- 主控给了四条建议，用户回复："好那就做123先吧"。这是第 3 条。

这条线偏数据工程岗。调研里 Meta 数据工程岗的现场面试是：先设计一个数据模型，再在同一个模型上连写几条指标查询（`docs/reports/2026 技术面试 高频题单 调研.md` 和研究笔记 `sql_data_ml_skillsets.md` 的 Data Engineer 部分）。

**现有的 SQL 判题**：
- 只读查询；
- `mode: dml`：单条 DELETE / UPDATE / INSERT，再用一条 `check_query` 看表的最终状态。

建表、约束、多步载入、慢变维度这些要执行一段多条语句的脚本，再从多个角度检查结果，所以这次先扩判题，再写内容。

**并行**：
- 32（`problems/analytics/`）和 33（`problems/sql/1–5`）是内容任务，可能还在跑。
- 平台文件现在归你：`server/app/`、`server/tests/`、`web/`、`docs/problem-format.md`、`docs/README.md`、`scripts/curriculum/verify_sql.py`、`pglite_runner.mjs`、`scripts/verify_bank.py`。
- 不要动 `problems/sql/` 和 `problems/analytics/`。

先读：
- `codex/PLAN.md`；
- 07 和 23 号任务的报告：`codex/runs/07-sql-judge-*/report.md`、`codex/runs/23-sql-dml-*/report.md`；
- 现有 SQL 判题的代码：浏览器 Worker、共用比较模块、`server/app/sql_judge.py`、`verify_sql.py`。

## 一、平台：`mode: script`

1. **格式**（`docs/problem-format.md` 升版本）：

   ```yaml
   mode: script
   checks:
     - label: 表结构            # 结果面板上显示的名字（中文）
       query: SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'members' ORDER BY ordinal_position
       ordered: true
     - label: 重复邮箱会被拒绝
       probe: INSERT INTO members (email) VALUES ('a@x.com')
       expect: error           # error | ok：探针语句应当失败还是成功
     - label: 载入后的会员表
       query: SELECT * FROM members ORDER BY id
       ordered: true
   ```

2. **判题流程**：
   - 建库；
   - 在一个事务里执行学习者的整段脚本，可以有多条语句（DDL、DML、CREATE VIEW / INDEX 等）；
   - 依次执行 `checks`：
     - `query` 取结果，和参考脚本执行后同一条 query 的结果比对；
     - `probe` 在 SAVEPOINT 里执行，看成功还是失败，和 `expect` 比对，然后回滚到 SAVEPOINT；
   - 最后整体回滚。
   - 期望结果照旧由服务器预先算好，`query` 的期望来自参考脚本。
3. **拒绝事务控制语句**：BEGIN、COMMIT、ROLLBACK、SAVEPOINT 一律拒绝，因为判题靠外层事务回滚隔离。给中文提示。其余语句不设限：学习者就是用户自己，数据库在内存里，每次回滚。
4. **结果面板**：
   - 每个检查一行：标签、通过与否；
   - 不通过时展开"你的结果"和"期望结果"；
   - 探针显示"应当被拒绝 / 实际被接受"这类说明，带数据库的报错原文。
5. **课里的 SQL 示例**支持多语句（建表再查询），这条线的课要用。
6. **`verify_sql.py` 支持 script**：
   - 参考脚本能跑，每个检查在参考脚本上的结果都符合 `expect`；
   - 每条 `wrong_examples` 至少在一个数据集上有一个检查不通过。
7. **附加题**：SQL 附加题的出题 schema 加上 script 题，验证规则同上。
8. **测试**：
   - 后端：期望计算、探针、拒绝事务语句、错误脚本判错；
   - 前端：比较模块加 script 用例。

## 二、内容：新线 `modeling`（约 70 题）

`problems/modeling/track.yaml`：
- `id: modeling`
- `name: 建模与写数据`
- `order: 11`
- `language: sql`
- `runtime: pglite`
- `requires: [sql]`
- `skill_prefix: modeling`

开发时就用 `status: active`。阶段写 `units`，技能加 `group`。

可以有自己的 `_db/`，比如在书店基础上的仓库和会员系统；也可以每题自带建表脚本。

**阶段**（可以微调，写进报告）：
1. **建表与类型**：
   - CREATE TABLE；
   - 选类型（整数、NUMERIC、TEXT、DATE、TIMESTAMPTZ、BOOLEAN）；
   - NOT NULL、DEFAULT；
   - 主键和自增（`GENERATED ALWAYS AS IDENTITY`）；
   - ALTER TABLE 加列、改列。
2. **约束**：
   - UNIQUE、CHECK；
   - 外键和 `ON DELETE CASCADE / SET NULL`；
   - 复合主键；
   - 用探针检查约束是否真的生效。
3. **写数据**：
   - 多行 INSERT、INSERT … SELECT；
   - UPDATE … FROM；
   - DELETE … USING；
   - RETURNING。
4. **合并与增量载入**：
   - `INSERT … ON CONFLICT DO UPDATE / DO NOTHING`；
   - MERGE；
   - 暂存表 → 目标表的增量去重载入（同一键取最新一条）。
5. **建模**：
   - 范式判断（看数据作答：这张表有什么冗余、更新异常）；
   - 一对多和多对多拆表（中间表）；
   - 星型模型（事实表、维度表）；
   - 慢变维度第 2 型：保留历史版本，有效起止日期 + 当前标记。
6. **视图、索引和数据质量**：
   - 视图；
   - CREATE INDEX；
   - 读简单的执行计划，用看数据作答题，少量；
   - 数据质量检查查询：孤儿行、重复键、空值率、取值越界。
7. **综合**：仿 Meta 数据工程岗的面试形式。
   - 先按需求写建表 + 灌数脚本；
   - 再在同一模型上写 2–3 条指标查询，用一道 script 题的多个 `checks` 或连续几道题都可以。

**通用要求**同其他 SQL 内容任务：
- 题号 `modeling-<阶段>-NNN-slug`，order 步长 10；
- 每题 2–4 条 `wrong_examples`，至少在一个检查上判错；
- 题面中文，标识符英文；
- 每组一个课文件，讲解、示例、小测三步都要有，示例能跑；
- 只参考题型思路，题面自己写。

**典型错误**：
- 金额用 FLOAT；
- 忘了 NOT NULL；
- 外键方向反了；
- UPDATE 漏了 WHERE；
- ON CONFLICT 的冲突目标没有唯一约束；
- 增量载入没去重导致重复；
- 慢变维度更新时没关闭旧版本；
- 多对多直接在一张表里存逗号分隔的列表。

## 不写防御性代码

用户 2026-11-23 说"反正就我自己用 把防御性的代码都撤掉就优化性能就可以"。具体要求：
- 判题代码只写必要的路径，不包多余的 try/except，不重复校验；
- 只在"事务隔离"这一处做限制（拒绝事务控制语句）。

## 验收标准

1. `server/.venv/bin/python -m pytest -q` 全过，前端测试全过，`npm run build` 通过。
2. `python3 scripts/curriculum/verify_sql.py` 全过，含 `--only modeling-`。已有的 SQL 题和 analytics 题照旧通过。
3. `check_curve.py --track modeling`：0 错 0 警。
4. 起 8001 和 5174 测试实例，在浏览器里做 3 道题，截图放 `{RUN_DIR}/`：
   - 一道带探针的建表题：写对时通过；漏了 UNIQUE 时"重复邮箱会被拒绝"这条检查不通过；
   - 一道 upsert 题；
   - 一道综合题；
   - 另外试一下脚本里写 COMMIT，应被拒绝并给中文提示。
5. 报告里列出：
   - 格式改动；
   - 技能清单；
   - 每阶段题数和题型统计；
   - 每种检查（query / probe）各用在了哪些题。
