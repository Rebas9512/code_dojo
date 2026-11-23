# 32 · 新线「产品分析 SQL」（`analytics`）：技能图 + 库 + 课 + 题

## 背景

用户 2026-11-23 的原话：
- "话说sql的题库是不是挺少的 这边处理优化的时候可以去帮我看看sql题库有没有什么可以扩充的track之类的"
- 主控给了四条建议，用户回复："好那就做123先吧"。这是第 1 条。

**现状**：SQL 线只有 142 题。留存、漏斗、连续区间、中位数、行列转换这些技能，每个只有 1–3 道题。

**调研结论**见 `docs/reports/2026 技术面试 高频题单 调研.md`：
- 读"数据岗的分水岭在 SQL 窗口函数"一节；
- 读研究笔记 `docs/research_notes/2026 技术面试 高频题单 调研/sql_data_ml_skillsets.md`。

数据分析、产品数据科学、数据工程面试里反复出现的业务题型有：分组 Top N、连续天数、留存与流失、漏斗转化、滚动平均、环比同比、行列转换、中位数、实验指标。Meta 产品数据科学岗的技术筛选是"SQL + 由同一份数据引出的业务问题"。这条线就是专门练这些。

**并行**：
- 33 号任务同时在加厚 SQL 主线 `problems/sql/1–5`。
- 一个 Opus 子代理在清理 `server/app/`、`web/src/`。

你只负责下面这些：
- `problems/analytics/` 全部；
- `docs/curriculum.md` 里新加的「产品分析 SQL（analytics）」一节；
- `docs/teaching-design.md` 里这条线的误解目录；
- `scripts/curriculum/check_curve.py` 识别表里新加的行（只加不改）。

不改平台代码（`server/app/`、`web/`、`judge/`），不改 `problems/sql/`。

先读：
- `codex/PLAN.md`；
- `docs/problem-format.md`：SQL 题、`mode: dml`、看数据作答 `inspect`；
- `docs/curriculum.md` 第 7 节；
- SQL 线阶段 4–5 的几道题和课：`problems/sql/4/`、`problems/sql/5/`、`problems/sql/lessons/sql-4-*`、`sql-5-*`。

格式、数据集密度、`wrong_examples`、课的写法都跟它们一致。

## 线的设置

`problems/analytics/track.yaml`：
- `id: analytics`
- `name: 产品分析 SQL`
- `order: 10`
- `language: sql`
- `runtime: pglite`
- `requires: [sql]`：地图上它会挂在 SQL 标签页里 SQL 主线下面
- `skill_prefix: analytics`

开发时就用 `status: active`，因为 `verify_sql.py` 只查 active 的线。每个阶段写好 `units`，技能加 `group`。

技能可以跨线引用 SQL 线的技能（`sql.window-agg`、`sql.lag-lead`、`sql.gaps-islands`、`sql.retention`、`sql.funnel`、`sql.median`、`sql.pivot`、`sql.generate-series` 等）。这条线自己的技能是业务套路：
- 前缀 `analytics.`；
- 只能人工标注，写进 `introduces`；
- 参考解用到的 SQL 语法照旧由 check_curve 的 SQL 识别表映射到 `sql.*` 技能。

## 库

`problems/analytics/_db/<名字>/schema.sql + seed.sql`，比如 `readerapp`。

**场景**：同一家书店的 App，延续 SQL 线的书店世界。表大致包括：
- App 用户（注册日期、渠道、国家/城市、设备）
- 会话或登录
- 行为事件：浏览图书、加购物车、下单、付款、搜索等，带时间戳
- 订阅会员：开通、续费、取消、套餐价格
- 付费流水
- 实验分组：实验名、用户、组别、分组时间

表名、列名用英文。

**数据量**要够算留存和批次分析，比如几十个用户、跨 8–10 周的事件。同时要让学习者能在题面样例里读懂。写法：
- 共享库给中等规模的真实感数据；
- 需要精确构造边界的题用题内小表。

两种都允许，跟 SQL 线一样。

**数据里要有的情况**：
- 同一天多次登录；
- 跨午夜的会话；
- 跨月；
- 只来过一次的用户；
- 流失后回流；
- 同一用户被分到两个实验组（污染）；
- 退款；
- 时区之类的坑可以不做。

**隐藏数据集**：照 SQL 线的做法用 `datasets/<补丁>.sql` 在样例上追加或修改几行。专门制造：
- 并列；
- 空的一天；
- 单人批次；
- 首日即流失；
- 分母为 0；
- 重复事件。

## 阶段（约 90 题，可以微调，写进报告）

1. **指标基础**：
   - DAU / WAU / MAU，粘性（DAU/MAU）；
   - 用 `generate_series` 给没有数据的日期补零；
   - 7 日滚动平均；
   - 环比、同比、占比。
2. **漏斗与转化**：
   - 各步骤人数；
   - 必须按时间先后发生的严格漏斗；
   - 限定时间窗内的转化（如浏览后 24 小时内下单）；
   - 按渠道、设备拆分；
   - 中位转化时长。
3. **留存与流失**：
   - 次日、7 日、30 日留存；
   - 按注册周的批次留存矩阵（行列转换）；
   - 滚动留存与固定日留存的区别（看数据作答）；
   - 流失定义（N 天未活跃）；
   - 流失率。
4. **会话与连续行为**：
   - 30 分钟无操作切分会话（sessionization）；
   - 会话数和时长；
   - 连续登录天数、最长连续；
   - 首次和末次行为；
   - 两次购买的间隔。
5. **增长核算与用户价值**：
   - 按月把活跃用户分成新增 / 留存 / 回流 / 流失（growth accounting）；
   - ARPU 和 ARPPU；
   - 累计 LTV；
   - 首单到复购；
   - 订阅 MRR 的新增、续费、流失拆解。
6. **实验分析**：
   - 各组人数和分流比例检查（SRM：用卡方统计量，在 SQL 里算）；
   - 各组转化率和相对提升；
   - 两比例 z 值（SQL 里用 SQRT 算）；
   - 剔除同时在两组的用户；
   - 按段拆分时的辛普森悖论（看数据作答）。
7. **综合案例**：仿 Meta 产品数据科学岗的面试形式。
   - 一个场景配 3–4 道连续的题，后一题建立在前一题的结果上；
   - 再配 1–2 道看数据作答题，看结果回答业务问题，比如"转化率下降最可能是哪一步出了问题"。

**题型阶梯**：每个新技能按 "课里的讲解、示例、小测 → 补全 → 独立写 →（改错 / 变式 / 组合）"。改错题集中在这条线最典型的错误上：
- 分母用错（全体用户而不是当期活跃）；
- 留存用了 `>=` 而不是恰好第 N 天；
- 会话切分时 LAG 没按用户分区；
- 漏斗没检查先后顺序；
- 去重时 `COUNT(*)` 和 `COUNT(DISTINCT user_id)` 混用；
- 整数除法；
- 日期截断到周时的周起始日；
- 补零时 LEFT JOIN 的方向。

## 通用要求

- **编号**：题号 `analytics-<阶段>-NNN-slug`，NNN 从 001 起；order 从 10 起，步长 10。
- **题面**：用中文写；表名、列名、学习者要输出的列名用英文（见格式文档"题目语言约定"）。
- **题面要自己写**：只参考 DataLemur、StrataScratch、LeetCode 分析题的题型思路，不抄题面和数据。可以在 `source` 里写题型来源，比如"LeetCode 1097 型"。
- **`wrong_examples`**：每题 2–4 条，`verify_sql.py` 要能确认每条至少在一个隐藏数据集上和参考解不同。
- **课**：每个组一个课文件 `analytics-<阶段>-lNN-…`。
  - 讲解、示例、小测三步都要有；
  - 示例写在这条线自己的库上，并且能跑；
  - 讲业务概念时先讲指标的意思和为什么这么定义，再讲 SQL。
- **结果比较**：涉及小数的统一用 `ROUND(…, 2)` 或 `ROUND(…, 4)`，在题面说清楚，避免浮点误差。
- **不写防御性代码**：参考解写成面试里该写的样子，不为假想情况加多余的 COALESCE 和 CASE。

## 验收标准

1. `python3 scripts/curriculum/verify_sql.py --only analytics-` 全过，SQL 线照旧全过。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track analytics`：0 错 0 警。全库跑一遍，不能新增别的线的错误。
3. 后端测试照旧通过：`cd server && .venv/bin/python -m pytest -q`。
4. 起测试实例（8001 和 5174，见 brief）后：
   - 首页 SQL 标签页里这条线挂在 SQL 主线下面；
   - 双击节点能进题目列表；
   - 在浏览器里提交 3 道题：一道普通查询题、一道看数据作答题、一道综合案例题；
   - 截图放 `{RUN_DIR}/`。
5. 报告里列出：
   - 库的表结构和行数；
   - 技能清单（id、名称、阶段、组、前置）；
   - 每阶段的题数和题型统计；
   - 每个技能的题数。
