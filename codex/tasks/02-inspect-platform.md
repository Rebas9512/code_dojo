# 02 · 平台：新题型"看数据作答"（inspect），新增根线"认识数据"，数据处理线改名 wrangle

## 背景

用户 2026-11-22 说："我觉得这个面向零基础的还不够基础 应该从认识不同的数据格式和特点开始做可能更好一些"。

调研报告 `docs/reports/零基础 编程 教学大纲 调研.md` 的建议：
- 加一条两条线共用的根线"认识数据"，7 个技能，全部用"看数据作答"的题练。
- Python 基础和 SQL 的开头跨线引用它。

先读报告的「推荐…根线」「技能清单」「落地要改的六处」三节。这次只做**平台**部分；内容（根线的题和课、Python 第 0 组、SQL 开头）是 06 号任务，等你做完再派。

报告里需要拍板的三点，主控按报告的默认做：
1. 看数据作答题和别的题一样计入通过状态。
2. 跨线前置只算"已学"，现在也没有锁。
3. 根线排在最前。

**并行**：03、04、05 号内容任务，还有平台任务 02m（首页地图）在同时跑，先读 `codex/PLAN.md`。

不要碰 02m 的文件：`web/src/pages/MapPage.tsx`、`web/src/pages/map.css`、新的 `server/app/units.py`、`/api/tracks` 接口函数、`track.yaml` 里的 `units`、`TrackPage.tsx` 和 `SkillsPage.tsx` 里的单元小标题。

`server/app/tracks.py` 两边都要改：你只给 language、runtime 加 `none`，用小补丁改。你独占平台文件，不要动 `problems/python/`、`problems/algo/`、`problems/sql/` 下的题目、技能和课。

## 要做的事

### 1. track 调整

- **数据处理线改名**：01 号任务建的"数据处理"线（`problems/data/`，id `data`）改名为 id `wrangle`，前缀 `wrangle`，目录改成 `problems/wrangle/`。`tensor` 的 requires 跟着改成 `[wrangle, math]`。
- **新建根线** `problems/data/track.yaml`：
  - `id: data`，`name: 认识数据`
  - summary 一句话，比如"表、值的种类、缺失、形状，CSV 和 JSON：先认数据，再写代码。"
  - `order: 0`（地图最前），`status: active`，`requires: []`，`skill_prefix: data`
  - 一个阶段：`id: "0"`，`name: 认识数据`
  - `language: none`、`runtime: none`：这两个是新值，表示这条线没有编程语言，题全是看数据作答。格式文档和代码里都要支持。
  - 先放一个空的 `skills.yaml`（`track: data`、`skills: []`），内容由 06 号任务写。
- **`python` 和 `sql` 的 requires 都加上 `data`**。根线现在没有技能和题，检查脚本不能因此报错。
- 文档里所有提到"数据处理 = data"的地方同步改掉：README 2b 表和地图、PLAN 以外的 docs。

### 2. 新题型 `format: inspect`（看数据作答）

`docs/problem-format.md` 升到 v1.4，写清楚下面的格式，并在开头的版本说明里写一句改了什么。

```yaml
# problems/data/0/data-0-003-count-rows/problem.yaml
id: data-0-003-count-rows
title: 这张表有几行
track: data
stage: "0"
order: 30
format: inspect
mode: inspect
difficulty: 2
skills: { requires: [data.table-intro], introduces: null }
data:                          # 一到多个数据块，按顺序显示在题面下面
  - kind: table                # table | csv | json | schema | values
    title: books（部分）
    file: books.csv            # 题目目录里的文件；也可以用 content: 直接写
  - kind: json
    title: 一笔订单
    file: order.json
answer:
  type: short                  # choice（单选）| short（打一个短答案）
  accept: ["6", "六"]           # short：可接受的答案，规范化后比对
  normalize: [strip, fullwidth, casefold]   # 默认就是这三个：去首尾空白、全角转半角、忽略大小写
  # choice 时：options: ["整数", "小数", "文字", "真假", "空"]，correct: 2（下标）
  misconceptions:              # 错误答案 → 具名误解编号（可选），答错时显示这条误解的一句话解释
    "5": DM05
explain: |                     # 答完之后显示（对错都显示），Markdown
  表头不算一行……
```

数据块 `kind` 的显示方式：
- **table**：内容是 CSV，渲染成表格，表头加粗；空格子显示成一个淡色的"空"，和空字符串 `""` 区分开（CSV 里用 `""` 表示空字符串）。
- **csv**：原样等宽显示，带行号。
- **json**：原样等宽显示，可以折叠嵌套。
- **schema**：表结构，用 yaml 写列：名字、类型、能否为空、是不是主键。渲染成一张小表。
- **values**：一串值，每个值一块，等宽显示。

判题（服务端，不用 Docker）：
- **short**：规范化后在 `accept` 里就是 accepted。
- **choice**：下标等于 `correct` 就是 accepted。
- 结果和别的题一样：存进 submissions，走 `verdict`；运行和提交都可以。
- 答错时，结果里带 `misconception: {id, name, line}`（从 `docs/teaching-design.md` 的误解目录取名字和一句话，或者在 problem.yaml 里写死，你选）和 `explain`。答对也带 `explain`。

### 3. 前端

- **题目页**：如果题目是 `inspect`，或者所在线的 `language: none`：
  - 左栏：题面 + 数据块（上面那几种渲染）。
  - 右栏：不用 Monaco，改成作答区。choice 显示选项，可以用数字键选；short 显示一个输入框。下面是"提交"按钮，Ctrl+Enter 提交。
  - 结果区：对 / 错；答错且有误解时显示误解名和一句话解释；然后是 explain。
  - 裸写模式、AI 协助这些对 inspect 没意义的开关要隐藏。
- **课里的数据块**：课的 `example` 步骤除了 `code`，也可以写 `data`（一个数据块，格式同上）。
  - 渲染成可以切换"表格 / CSV / JSON"三种视图的数据块，CSV 可以编辑：改一个格子，表格视图跟着变。
  - JSON 视图由 CSV 转出来（每行一个对象），只读。
  - `kind: schema` 或 `values` 的数据块不切换，只显示。
- **助教**：
  - inspect 题的提示词里带数据块内容、学生当前的答案（choice 显示选了哪项），以及正确答案。正确答案不能直接说出来，规则同参考解。
  - 共享编辑对 inspect 题只作用于 short 的答案框。choice 题让 AI 只用文字讲。改提示词里对应的说明。
- **附加题**：inspect 题也能出附加题。
  - 出题 schema 加 inspect 分支：数据块内容内联、answer、explain。
  - 验证：choice 的 `correct` 在范围内；short 的 `accept` 非空；数据块能解析（CSV 能读、JSON 能 parse）。
  - 不能出附加题的语言（`language: none` 以外的 sql 等）照旧。

### 4. 检查脚本

- `check_curve.py`：
  - 支持 `format: inspect` 的格式校验：answer、data 文件存在、kind 合法。
  - inspect 题没有参考解，不做 AST 扫描。
  - `language: none` 的线不需要 solution 文件。
  - 识别表里 `type()` / None / True 改指哪个技能，**不归你**，06 号任务做。
- `verify_bank.py`：
  - inspect 题检查数据块能解析、答案自洽：choice 下标在范围内；short 的 accept 规范化后不重复且非空。
  - 不跑 Docker。

### 5. 测试和夹具

- 夹具加一条 `data` 根线（`language: none`），里面 2–3 道 inspect 题：choice、short 各至少一道，带 misconceptions。
- 再加一个带 `data` 数据块的课。
- 新测试覆盖：
  - inspect 加载
  - 判对、判错（含全角数字、大小写、首尾空格规范化）
  - 误解返回
  - 课里的数据块
  - `/api/tracks` 里根线排第一
  - 附加题 inspect 分支的验证函数，用 FakeProvider，不调真实 AI

## 验收标准

1. `server/.venv/bin/python -m pytest -q` 全过（含新测试）。
2. 真实题库 `verify_bank.py` 照旧全过，`load_errors` 为 0。注意 03、04 号任务可能在加题，它们的题挂了不算你的；但加载错误如果是你的格式改动造成的，就要修。
3. `check_curve.py` 不因为你的改动报新错。
4. `npm run build` 通过。
5. 起 8001 和 5174 测试实例（用夹具题库 `CODE_DOJO_PROBLEMS=server/tests/fixtures/problems` 也行），这些页面都能打开，没有控制台报错：
   - 地图第一条是"认识数据"
   - 夹具里的 inspect choice 题和 short 题能答、判对判错、显示误解和解释
   - 带数据块的课能切换三种视图、改 CSV 后表格跟着变
6. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
