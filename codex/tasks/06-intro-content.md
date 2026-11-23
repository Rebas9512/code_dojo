# 06 · 内容：根线"认识数据" + Python 基础第 0 组"值和类型" + SQL 阶段 0 开头

## 背景

用户 2026-11-22 说："我觉得这个面向零基础的还不够基础 应该从认识不同的数据格式和特点开始做可能更好一些"。

调研报告 `docs/reports/零基础 编程 教学大纲 调研.md` 给了完整方案。这次按报告的「技能清单」「现有入门段怎么挪」「落地要改的六处」三节落地内容。报告要全文读，尤其是这三节里的表格，技能 id、顺序、题目阶梯都以报告为准。

平台已经由 02 号任务做好：
- 新题型 `format: inspect`（看数据作答），格式见 `docs/problem-format.md` v1.4。
- 根线 `problems/data/`（id `data`，`language: none`），目前有空的 `skills.yaml`。
- `python` 和 `sql` 两条线的 `requires` 已经包含 `data`。

先读格式文档里 inspect 和课的数据块那两节，再读 02 写的夹具题（`server/tests/fixtures/problems/data/`），照着写。

报告里需要拍板的三点，按报告默认做：
1. 看数据作答题计入通过。
2. 跨线前置算"已学"。
3. 根线 7 个技能全部排在写代码之前。

**并行**：03（0A 第 6–10 组）和 05（SQL 阶段 1–2）可能还在跑，先读 `codex/PLAN.md`。

你名下的东西：
- `problems/data/` 全部。
- `problems/python/skills.yaml` 里第 0–2 组的条目，以及给集合类技能加跨线前置这一处，见第 2 节。
- 第 0–5 组题的 order，不超过 1990。
- Python 新题，题号 400–449。
- 课 `py-0a-l00…l02`。
- `problems/sql/skills.yaml` 里阶段 0 的条目。
- SQL 新题，题号 `sql-0-100…149`，以及阶段 0 题的 order。
- 课 `sql-0-l00`。
- `track.yaml` 里 `data` 和 `python` 0A 的 `units`。

## 要做的事

### 1. 根线"认识数据"（`problems/data/`）

- **技能**：`skills.yaml` 写 7 个技能，见报告表格：
  1. `data.table-intro`
  2. `data.value-kinds`
  3. `data.quantity-vs-label`
  4. `data.missing`
  5. `data.column-type-key`
  6. `data.shapes`
  7. `data.text-formats`

  前置照报告。每个技能写完整知识卡，写法比照 Python 0A 的卡，零基础能看懂。每个技能单独一组，`group` 1–7，这样首页地图上根线有 7 个节点。
- **单元名**：在 `problems/data/track.yaml` 的阶段 0 写 `units`：
  - 1 一张表
  - 2 值的种类
  - 3 数量还是标签
  - 4 缺失值
  - 5 类型和主键
  - 6 数据的形状
  - 7 CSV 和 JSON
- **题**：`problems/data/0/` 下约 20 道 inspect 题，每个技能 2–3 道，题号 `data-0-NNN-slug`。
  - 数据全部取自书店练习库 `problems/sql/_db/bookstore/` 的表，导出成 CSV / JSON 放在题目目录里。
  - 前三个技能只给干净的子集，第四个技能起才放缺失值。
  - 题型照报告的"练习"列。答案尽量要求打字（short），少用单选。
  - 每题写 `answer.misconceptions`，把错误答案映射到 DM01–DM08，还有 `explain`。
- **课**：两个课文件，`data-0-l01-values`（技能 1–4）和 `data-0-l02-shapes`（技能 5–7）。
  - 示例用课里的数据块（02 做的 `example` + `data`，可以在表格 / CSV / JSON 三种视图之间切换）。
  - 小测针对 DM01–DM08。
- **要实际验证的一点**：报告说"Python 的 csv 模块把每个字段都读成字符串"，来源弱。写课之前在 Python 里实际跑一下验证，验证代码放在 `{RUN_DIR}/`，结论写进报告。如果这句话要写进课里，就按实际结果写。

### 2. Python 基础第 0 组"值和类型"

照报告「Python 基础第 0 组」表和「现有入门段怎么挪」表：

- **新增 2 个技能**：
  - `py.value-types`：五种值和 `type()`。
  - `py.type-ops`：类型决定运算的意思。PM05 从 `py.type-convert` 移过来。
- **挪进第 0 组的 5 个技能**（group 改成 0）：`py.print`、`py.var-arith`、`py.type-convert`、`py.stdio-input`、`py.compare-bool`。顺序和前置照报告。
  - `py.print` 的前置加上 `data.value-kinds`（跨线）。
  - 它们的知识卡照报告的意思改写，比如 print 改成"显示一个值"。
- **第 1 组**剩下 `py.func-return`、`py.floordiv-mod`、`py.fstring`，单元名改成"函数、整除和格式化"（在 `problems/python/track.yaml` 0A 的 `units` 里改）。
- **第 2 组**从 `py.if-else` 开始。
- **集合类技能**：`py.list-basics`、`py.dict-basics`、`py.set-basics`、`py.tuple`、`py.nested-list` 加跨线前置 `data.shapes`。这几个在第 5、7、8 组，03 号任务可能在改第 7、8 组的条目，你只加这一个前置，用小补丁改。
- **题**：
  - 新题约 10 道，题号 `py-0a-400…449`，照报告的"题目阶梯"列。
  - 旧题 001、101、002、102、103、104、110、111、008、009 保留，按报告调整 order 和标注；报告里写了要加的题面内容，比如 `print(7)` 对 `print("7")`，照做。
  - 007、112、010 是 function 模式，挪到第 1 组 `py.func-return` 之后；010 放在 `py.floordiv-mod` 之后。
  - 第 0–5 组的 order 可以整体重排，但不超过 1990。
- **课**：
  - 新建 `py-0a-l00-values`：把 print、type-convert、stdio-input 的讲解从 `py-0a-l01-basics` 搬过来，把 compare-bool 的从 `py-0a-l02-conditions` 搬过来。每个技能只能在一个文件里讲。
  - 补上 `py.value-types`、`py.type-ops` 的讲解、示例和小测。
  - 示例要在 playground 里能跑出注释写的结果。
- **识别表**（`scripts/curriculum/check_curve.py`）：这几行允许你改：
  - `type` 调用：`py.class-basic` → `py.value-types`
  - `none-const`：`py.none` → `py.value-types`
  - `bool-const`：`py.compare-bool` → `py.value-types`
  - `compare-is` 仍归 `py.none`。

### 3. SQL 阶段 0 开头

照报告「SQL 阶段 0 开头」表：

- **新增技能**：`sql.select-star`、`sql.schema-types`，前置照报告，含跨线的 `data.*`。
- **`sql.select-basic`**：前置加上 `sql.select-star`。
- **题**：4 道左右，题号 `sql-0-100…149`。
  - 补全、独立写的 SQL 题照 SQL 格式写。
  - "看表结构作答"这类用 `format: inspect`，数据块 `kind: schema`。
- **order**：阶段 0 题的 order 调整到这两个技能排在最前。
- **课**：新建 `sql-0-l00-tables`。
- **识别表**：`SQL_RULES` 里 `SELECT *` 单独映射到 `sql.select-star`。看清楚现有规则怎么写，不要让已有的题误判。

### 4. 内容校验脚本

`scripts/curriculum/verify_python.py` 和 `verify_sql.py` 是按语言跑参考解和课程示例的。它们要跳过两样东西，交给已经支持这些格式的 `verify_bank.py` 和 `check_curve.py`：
- 放在 python、sql 目录里的 inspect 题；
- 课里的 `data` 数据块示例。

这两个脚本归你改，只加跳过逻辑。

### 5. 文档

- `docs/teaching-design.md`：加上 DM01–DM08（名字和一句话解释照报告），以及 PM51–PM54；PM05 的归属跟着改。
- `docs/curriculum.md`：
  - 加一节"认识数据"根线。
  - 6.1 的表加第 0 组，第 1、2 组跟着改。
  - SQL 阶段 0 小节写上开头的两个技能。

## 验收标准

1. 这几项都要全过：
   - `cd server && .venv/bin/python ../scripts/verify_bank.py --jobs 4`：`data-*` 的 inspect 题自洽，`py-0a-*` 全部通过，`load_errors` 0。
   - `python3 scripts/curriculum/verify_sql.py --only sql-0`
   - `server/.venv/bin/python scripts/curriculum/verify_python.py -q`：课程示例。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py`：data 线、python 线第 0–5 组、sql 阶段 0 都 0 错 0 警。别的任务范围内的报错写进报告。
3. 起测试实例：
   - 首页 Python 和 SQL 两个标签的树根都是"认识数据"，有 7 个节点。
   - Python 基础第一个单元是"值和类型"。
   - 做一道根线 inspect 题，答对、答错都正常显示误解和解释。
   - 根线的课能切换数据块视图。
4. 报告里列出：根线题数、Python 第 0 组新旧题清单（含挪动的 3 道）、SQL 新题；csv 模块那条说法的验证结论。
