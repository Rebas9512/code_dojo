# 题目格式规范 v1.7

> v1.7 支持 SQL 修改类题，使用 `mode: dml` 和 `check_query` 检查修改后的表。
> v1.6 支持将函数参数转换为 DataFrame，并用 `sql_twin` 标记同题的 SQL 版本。
> v1.5 为 `ds` 运行环境提供数值和表格比较、AST 写法约束，以及用于梯度检查和模拟训练的 checker 接口。
> v1.4 支持看数据作答题（inspect）、无语言学习线（none）和课里的可编辑数据示例。
> v1.3 用 `track.yaml` 定义每条学习线、阶段、可选的单元名 `units` 和前置关系，并支持跨线引用技能与课程。
> 题库内容（problems/）和平台代码（server/、judge/、web/）之间的契约：内容按这个格式写，平台按这个格式读。要改格式先改这里。

## 目录

```
problems/
├── <track>/track.yaml                   每条线都有，包括规划中的线
├── data/0/<id>/                         看数据作答的 problem.yaml、statement.md 和数据文件
├── python/                              algo/ 使用相同的 Python 题格式
│   ├── skills.yaml                       技能图
│   └── <stage>/<id>/                     阶段见本线 track.yaml
│       ├── problem.yaml
│       ├── statement.md
│       ├── solution.py                   参考解（predict 模式下是要展示的程序）
│       ├── tests.json                    predict 模式没有
│       ├── starter.py                    可选：编辑器初始代码（complete / fix 题型必填）
│       └── checker.py                    可选：compare: checker 时必填
└── sql/
    ├── skills.yaml
    ├── _db/<name>/schema.sql, seed.sql   共享练习数据库（如 bookstore）
    └── <stage>/<id>/                     阶段见本线 track.yaml
        ├── problem.yaml
        ├── statement.md
        ├── solution.sql
        ├── starter.sql                   可选
        └── datasets/*.sql                可选：题目自带的数据集或补丁
```

## track.yaml

每条学习线各有一个 `problems/<track>/track.yaml`。规划中的线只需此文件。

```yaml
id: python                 # 等于目录名
name: Python 基础
summary: 从输出第一行文字，到用循环、函数和列表解决小问题。
order: 1                   # 学习地图按此字段升序展示
language: python           # python | sql | none，决定编辑器、判题入口和附加题支持
runtime: python            # python（Docker）| pglite（浏览器 SQL）| ds（M6 数据科学镜像）| none（看数据作答）
status: active             # active | planned
requires: [data]           # 直接前置学习线的 id
skill_prefix: py           # 本线技能、题目和课的 id 前缀
stages:
  - id: 0A
    name: 语法基础
    units:                 # 可选，技能 group 的编号与单元名
      0: 值和类型
      1: 变量、运算、输出
  - id: 0B
    name: 算法入门
```

- `requires` 必须构成无环图，且只引用已有的线。地图提示前置进度，所有线都可进入。规划中的线展示已配置的阶段，可以省略技能、题和课。
- `stages` 的顺序就是学习顺序，阶段 id 在线内唯一。数字和带引号的数字统一作字符串，`0a`、`0b` 统一为 `0A`、`0B`。同阶段按题目 `order` 升序，可留间隔（10、20、30…）方便插题。
- 阶段可用 `units` 为技能组命名。只要有技能带 `group`，就按编号升序展示配置或技能中出现的所有组，包括尚无题目的组。未命名的组显示为“第 N 组”，未分组的技能列在第一个单元。阶段内所有技能均无 `group` 时，整个阶段是一个单元，沿用阶段 id 和名称。规划中学习线的阶段返回空 `units`，地图用阶段名显示规划节点。
- 题目归哪个单元默认由技能推算：取 `introduces ∪ requires` 里本阶段技能的最大 `group`，没有就跟随前一道题。推算不对时，在 `problem.yaml` 里写 `unit: N` 直接指定。例如只用到前置线技能的练习题，指定后，后面的题跟着它走。
- 题目归入 `introduces` 和 `requires` 中本线、本阶段技能的最大组号。没有这样的组号时沿用同阶段前一道题的单元；阶段首题归第一个单元。
- 题目 `id` 全局唯一，等于题目目录名，格式为 `<skill_prefix>-<阶段小写>-<三位序号>-<slug>`，slug 用小写 kebab-case。例如 `py-0a-001-hello-print`、`algo-1-001-reverse-list`、`sql-0-101-complete-user-emails`。题目和课的 `track` 都写所在目录的 id，题目的 `stage` 同时对应目录和本线的阶段配置。

## skills.yaml

技能 id 全局唯一，格式为 `<skill_prefix>.<kebab-case>`。直接前置 `prereqs` 可以引用本线或任一直接、间接前置线的技能。例如算法线的 `algo.hash-seen` 前置 Python 基础的 `py.set-basics`。曲线检查按前置线的拓扑顺序进行，进入一条线时，其所有前置线的技能均视为已学。全题库共用技能卡和技能对应的课，同一技能只能由一个课文件讲解。

```yaml
track: python                 # 所在学习线 id
skills:
  - id: py.for-range          # 前缀取自 track.yaml
    name: for 循环与 range     # 中文
    stage: 0A                 # 这个技能第一次出现的阶段
    group: 3                  # 可选：所在阶段的整数单元编号，可从 0 开始
    prereqs: [py.var-arith]   # 前置技能，必须构成无环图
    card: |                   # 知识卡：Markdown，≤ 20 行，讲清概念 + 一个小例子 + 常见坑
      ...
```

## 看数据作答（inspect）

“认识数据”线的 id 和技能前缀都是 `data`，语言和运行环境都填 `none`。Python 基础和 SQL 共用这条前置线。进阶线“数据处理”使用 `wrangle`。任一学习线都可以放 inspect 题，`language: none` 的线只收 inspect 题。

只有 `track: data` 的 inspect 题计入技能掌握和常规间隔复习，其余线的 inspect 题作为脚手架。代码题的计入题型为 `write`、`variant`、`combine`。每次独立写对给 `skills.requires` 和 `skills.introduces` 中的每个技能累计一道不同题。推荐同套路练习时，焦点取 `introduces`，为空时取 `requires` 中最晚引入的技能。

题目目录放中文题面 `statement.md`、以下元数据以及引用的数据文件。此题型无需 solution、starter、tests 或 SQL 数据集。

```yaml
id: data-0-003-count-rows
title: 这张表有几行
track: data
stage: "0"
order: 30
format: inspect
mode: inspect
difficulty: 2
skills: {requires: [data.table-intro], introduces: null}
data:
  - kind: table
    title: 图书登记
    file: books.csv
  - kind: json
    title: 一笔订单
    content: '{"books": [{"id": "B2"}]}'
answer:
  type: short
  accept: ["6", "六"]
  normalize: [strip, fullwidth, casefold]
  misconceptions:
    "7": {id: CountHeader, name: 把表头也当成记录, line: 表头只写列名，数据从下一行开始。}
explain: |
  从表头的下一行开始数，每行是一本书。
```

`data` 至少一个块，按列表顺序显示。`title` 可省。`content` 是原始文本，也可以用相对于本题目录的 UTF-8 文件 `file`，两者只选一个。

| kind | 文本格式 | 显示 |
| --- | --- | --- |
| table | 第一行是列名的 CSV，每行列数一致，含逗号、换行或引号的格子按 CSV 引号规则转义 | 表头加粗。未加引号的空字段显示淡色“空”，引号包住的空字符串显示 `""` |
| csv | 同上 | 等宽原文和行号 |
| json | JSON 对象、数组或单个值 | 等宽原文，括号可折叠嵌套内容 |
| schema | YAML 对象，`columns` 列表里每列写 `name`、`type` 两个字符串和 `nullable`、`primary_key` 两个布尔值 | 列名、类型、可为空、主键 |
| values | JSON 数组，如 `[7, "7", 7.0, true, null]` | 每一项单独等宽显示，保留原文的类型写法 |

短答案的 `accept` 写成非空字符串列表。平台按 `normalize` 指定的顺序处理学生答案和可接受答案，默认去首尾空白（strip）、全角 ASCII 及全角空格转半角（fullwidth）、忽略大小写（casefold）。可写 `normalize: []` 精确比较。规范化后每个可接受答案都必须非空且唯一。

单选把 `answer` 换成下面的结构。至少两个选项，`correct` 和误解映射的键都从 0 数。页面上的数字键从 1 数。

```yaml
answer:
  type: choice
  options: ["书名", "图书编号"]
  correct: 1
  misconceptions: {"0": DM05}
```

`misconceptions` 可省。短答案用错误答案作键，应用与 `accept` 相同的规范化。值可直接用 DM01–DM08（带引号的数字、真假文字、缺失和零、数字标签、名字当主键、CSV 类型、列内混用、数据形状），也可在题内写 `{id, name, line}`。错误键应与正确答案互斥。

`/run` 和 `/submit` 均接收 `{"answer":"…"}`，单选填选项下标，也接受整数。结果包含 `verdict` 和 Markdown `explain`，错误答案命中映射时另带 `misconception: {id, name, line}`。正式提交计入题目通过状态，运行只记录运行结果。题目详情公开数据块、作答类型和选项。

## Python：problem.yaml

```yaml
id: py-0a-010-sum-of-list
title: 列表求和                 # 中文
track: python
stage: 0A
order: 100
format: write                  # predict | complete | fix | write | variant | combine
mode: function                 # function | class | stdio | predict
difficulty: 8                  # 1–100，比 Easy/Medium/Hard 细；同一阶段内大致递增
skills:
  requires: [py.for-range, py.list-basics]   # 这题要用到、此前已引入的技能
  introduces: py.accumulator                 # 这题新引入的技能，最多 1 个；没有就写 null
source: original               # original | neetcode250 | top-100-liked | grind169 | top-interview-150 | leetcode75 | ...
leetcode: null                 # 对应 leetcode.com 的 slug（如 two-sum），没有写 null
milestones: []                 # 可含 blind75 / nc150 / top100
entry: sum_of_list             # function 模式：函数名；class 模式：类名
signature: "def sum_of_list(nums: list[int]) -> int:"   # function 模式必填
compare: exact                 # exact | unordered | float | checker | allclose | frame
time_limit_ms: 2000            # 可选。省略时 Python 默认 2000，DS 默认 10000，每个用例单独计时
convert:                       # 可选：将 JSON 参数转换为题目约定的数据结构
  args: {"0": listnode}        # 参数下标 → listnode | treenode | dataframe（ds 环境）
  returns: listnode            # 返回值转换支持 listnode | treenode
hints:                         # 可选：作者写的 1–3 级提示（AI 提示之外的离线兜底）
  - 方向提示
```

### tests.json

- **function**：`{"examples": [{"args": [[1, 2, 3]], "expected": 6}], "hidden": [...]}`。`args` 是位置参数数组。examples 在题面和"运行"里可见，hidden 只在"提交"时跑。
- **class**（LeetCode 设计题风格）：每个用例是
  `{"ops": ["LRUCache", "put", "get"], "args": [[2], [1, 1], [1]], "expected": [null, null, 1]}`，
  第一个 op 是构造函数。
- **stdio**：每个用例是 `{"stdin": "3\n1 2 3\n", "expected": "6\n"}`；比较时去掉每行行尾空白和末尾空行。
- **predict**：没有 tests.json。题面展示 `solution.py`，用户写出它的输出；判题时运行 `solution.py` 得到真实输出再比对（规则同 stdio）。

### compare

- `exact`：JSON 值完全相等（元组按列表比）。
- `unordered`：返回值是列表时忽略顺序（只排外层）。
- `float`：数值容差 1e-6（递归作用于列表）。
- `checker`：调用 `checker.py` 里的 `check(args, expected, actual) -> bool`（多解题用）。

### 数据科学比较和写法约束

在 `ds` 环境的函数题中，`convert: {args: {"0": dataframe, "1": dataframe}}` 将指定位置的 JSON 参数转成独立的 pandas DataFrame。每个表用 `{"columns": ["book_id", "stock"], "data": [[1, 3], [2, null]]}` 表示，可加 `index` 指定行标签。列类型由 pandas 推断，空表仍保留列名。未标记的位置直接传入 JSON 值。

与 SQL 线练习同一查询时，顶层可写 `sql_twin: sql-0-001-book-titles`，值为对应题目目录的完整 id。`leetcode` 另记参考思路的 LeetCode 题目 slug。

学习线配置使用 `language: python`、`runtime: ds`。测试输入仍是 JSON 位置参数，学生函数按照题面约定将列表转换为数组、张量或表。函数返回值和类方法返回值都可使用以下比较方式。类用例中构造函数和没有返回值的方法在 `expected` 中写 `null`。

```yaml
compare: allclose
rtol: 1.0e-5
atol: 1.0e-8
constraints:
  no_loops: true
  forbid_imports: [sklearn]
  forbid_calls: [torch.nn.functional.scaled_dot_product_attention, torch.nn.MultiheadAttention]
```

- `allclose` 接受 Python 数字、布尔值、规则嵌套列表、NumPy 数组和 CPU 张量。在 `tests.json` 中，`[1, 2]` 表示整数，`[1.0, 2.0]` 表示浮点，`[true, false]` 表示布尔。形状和类别必须相同，位宽可以不同。数值条件是 `abs(实际 − 期望) <= atol + rtol * abs(期望)`。容差默认如上。失败时显示第一个超差元素的零起始坐标。
- `frame` 比较 pandas DataFrame 或 Series。DataFrame 的期望格式是 `{"columns":["组","数量"],"data":[["甲",3],["乙",5]],"index":[0,1]}`。Series 的期望格式是 `{"name":"数量","data":[3,5],"index":["甲","乙"]}`。`index` 省略时从 0 编号，未命名 Series 可省略 `name`。用 `null` 表示缺失，两个缺失值相等。数值沿用上述容差。
- `frame` 默认按顺序核对行、索引、列名和数据。`ignore_row_order: true` 将行一一配对，重复行的次数必须一致。`ignore_index: true` 忽略索引标签。`check_column_names: false` 忽略列名或 Series 名称，各列始终按位置对应。三个开关是独立的 `problem.yaml` 顶层字段。
- `constraints` 适用于 Python 和 DS 代码题。三个字段均可省略。`no_loops` 禁止 for、async for、while、列表 / 字典 / 集合推导式及生成器表达式。`forbid_imports` 按模块名及其子模块匹配。禁用调用填完整名字，AST 识别直接调用、常见的 `import ... as ...`、`from ... import ...` 和名字赋值别名。语法检查通过后才检查写法，返回 `constraint_error` 时尚未执行用例。

形状预测使用现有的 `format: predict` 和 `mode: predict`。在 `solution.py` 中逐行 `print(t.shape)`，期望输出来自 DS 镜像内的这段程序。

### 梯度检查和参考实现对拍

函数题的 `compare: checker` 支持另一种入口 `check_function(args, expected, fn) -> bool`。checker 收到当前用例的 JSON 参数、期望值和学生函数，可以创建原生张量、模型或随机输入后调用 `fn`。每个 checker 只需定义一种入口。返回 `False` 或抛出带中文原因的 `AssertionError` 表示答案错误。学生函数、checker 和比较过程共用本用例的时限。

```python
# checker.py：题目要求给出 sum(x ** 2) 对 x 的梯度
import numpy as np
from dojo_grad import check_grad

def check_function(args, expected, fn):
    x = np.asarray(args[0], dtype=float)
    return check_grad(fn, lambda t: (t * t).sum(), [x])
```

- `numeric_grad(f, x, eps=1e-5)` 在独立的双精度副本上做中心差分，返回与输入同形状的梯度。支持 NumPy 和 torch。目标函数 `f` 返回标量，计算向量输出的反向传播时，可先把输出与上游梯度做内积。
- `check_grad(user_backward, f, inputs, *, eps=1e-5, rtol=1e-4, atol=1e-6)` 逐个扰动位置参数。单输入的 backward 直接返回梯度，多输入按顺序返回梯度列表或元组。成功返回 `True`，失败指出第几个输入以及第一处差值。
- 固定种子对拍可以把种子写进用例 `args`。checker 用 `np.random.default_rng(args[0])` 生成同一份输入，分别运行参考函数和学生函数。调用 `dojo_compare.allclose(expected, actual, rtol=..., atol=...)` 或 `dojo_compare.frame(expected, actual, ...)`，成功得到 `None`，失败得到中文差异字符串，checker 可用 `assert reason is None, reason` 回传。

### 小批次模拟训练

训练循环仍用 `function`，需要改错时选 `format: fix` 并提供 `starter.py`。用例的 `args` 可以只保存种子，由 checker 创建微型数据和模型。下面的 checker 要求学生实现 `train(model, data, optimizer, steps)`。

```python
import torch
from dojo_train import simulate_train, assert_loss_decreased, assert_overfit

def batches():
    x = torch.tensor([[-1.0], [1.0]])
    return (x, 2 * x), (x / 2, x)

def check_function(args, expected, train):
    losses = simulate_train(
        train, make_model=lambda: torch.nn.Linear(1, 1), make_data=batches,
        make_optimizer=lambda params: torch.optim.SGD(params, lr=0.25),
        loss_fn=torch.nn.functional.mse_loss, steps=24, seed=args[0], require_eval=True,
    )
    assert_loss_decreased(losses, window=10, ratio=0.5)
    assert_overfit(losses, atol=1e-3)
    return True
```

1. `simulate_train` 先设 Python、NumPy 和 torch 种子，再调用工厂创建新模型、新优化器和一对训练 / 验证小批次。学生从 `data.train` 读取训练批次，对 `data.loss(prediction, target)` 返回的标量反向传播。每次更新前须按 `zero_grad() → backward() → step()` 的顺序操作。
2. 用 `with data.evaluating():` 标明评估阶段，在其中读取 `data.valid`。学生负责 `model.eval()` 和 `with torch.no_grad():`。后面还有训练时需切回 `model.train()`。设置 `require_eval=True` 后，至少要有一次读取验证批次并完成评估前向的记录。训练阶段访问验证批次或使用其张量切片，会得到中文诊断。
3. 返回的 `losses` 按实际参数更新记录反向传播的损失，每步一个值。`assert_loss_decreased` 判最后一个窗口的均值严格低于第一个窗口均值乘以给定比例。`assert_overfit` 判最后一步距零的绝对值。`assert_trajectory(losses, reference, rtol=1e-5, atol=1e-8)` 检查步数和逐步数值，`reference` 可用同样的工厂、种子和参考训练函数再次运行得到。

运行本题的课或附加题时，前端向 `POST /api/playground/run` 提交 `problem_id`、`code` 和可选 `stdin`，后端据此选镜像。旧请求省略 `problem_id` 时使用普通 Python 镜像。完整的七道样例见 [dsfix 测试题库](../server/tests/fixtures/problems/dsfix/)。

### 其他约定

- 题面 `statement.md`：中文 Markdown，固定小节 `## 题目` `## 示例` `## 约束`，可选 `## 提示`。**不复制 LeetCode 原题面文字**，用自己的话写；可以在末尾放原题链接。
- `solution.py` 只能用 `requires ∪ {introduces}` 里的技能（平滑性检查会用 AST 核对）。
- complete / fix 题型：`starter.py` 是给用户的半成品或带 bug 的代码；fix 题的 bug 必须能被至少一个测试抓住。
- 每题至少 2 个 examples、至少 3 个 hidden，hidden 要覆盖边界（空输入、单元素、重复、负数等）。

## SQL：problem.yaml

```yaml
id: sql-0-010-select-all-books
title: 查出所有图书
track: sql
stage: "0"
order: 100
format: write
difficulty: 3
skills: {requires: [], introduces: sql.select-basic}
source: original               # original | sql50 | leetcode-db | ...
leetcode: null
milestones: []
datasets:                      # 第一项是题面里展示的样例数据，其余是隐藏数据集
  - db:bookstore               # 共享库：先跑 _db/bookstore/schema.sql 再跑 seed.sql
  - db:bookstore + datasets/ties.sql   # 共享库之后再执行补丁脚本
  - datasets/own.sql           # 题目自带的完整脚本（建表 + 数据）
ordered: false                 # true 时比较行顺序（题目要求 ORDER BY）
hints: []
```

- SQL 使用 PostgreSQL 18（PGlite）。省略 `mode` 时，学生和参考解各写一条只读的 `SELECT` 或 `WITH ... SELECT`。
- 期望结果不手写：校验时在每个数据集上运行 `solution.sql` 得到。所以参考解必须真正正确，隐藏数据集要能区分常见错误写法（NULL、并列、重复、空分组）。
- 结果比对：列数相同；值逐个比较（数字容差 1e-6，NULL 等于 NULL，日期转 ISO 字符串）；`ordered: false` 时忽略行序；不比列名。

### SQL 修改类题

```yaml
mode: dml
check_query: SELECT id, email FROM person ORDER BY id
ordered: true
```

学生、`solution.sql` 和每个 `wrong_examples[].sql` 各写一条 `DELETE`、`UPDATE` 或 `INSERT`，可用 `WITH` 引出这条语句。每次从该数据集的初始状态执行一份答案，再用题目提供的单条只读 `check_query` 读取最终状态，随后回滚。检查查询应包含所有需要保留的行和列，`ordered: true` 时用 `ORDER BY` 确定行序。

参考解必须在每个数据集上改变检查结果，删除后的表可以为空。至少给一段能运行的典型错误写法，每段都要在至少一个隐藏数据集上产生不同的最终状态。SQL 附加题遵循同一规则。结果面板显示两张表，以及 PostgreSQL 对学生主语句报告的影响行数。判分依据是最终状态。

## 谁检查什么

- `scripts/curriculum/check_curve.py`（内容侧）：技能图无环；按学习顺序，每题 `requires` 都已在本线引入或来自前置线；每题最多引入 1 个新技能；参考解实际用到的语法（AST / SQL 解析）不超出标注。
- `scripts/verify_bank.py`（平台侧）：校验 inspect 数据与答案，使用 Docker 跑每道 Python 题的参考解；SQL 题由 Node PGlite 实跑各数据集上的参考解、典型错误写法和改错题的初始代码。

---

## v1.2：题和课合在一起（2026-11-22，取代 v1.1 的独立课）

依据：用户决定"每一题我们可以对应一节课（不用做成两个部分），上来我们可以看到题，如果能做就直接做了，做不了我们切到上课部分 再去了解这节课需要用到的知识点这样 ai助手也能看到一起聊这些点"。

- 题目列表里只有题。做题页左栏有两个标签：**题目** 和 **课**。默认打开题目；不会做就切到课。
- 课的内容按**技能**写：每个技能一段教学内容（讲解 → 带步骤名的示例 → 小测），写在 lesson 文件里。一道题的"课"标签 = 它 `introduces` 的技能的教学内容（展开、放最前）+ 它 `requires` 的技能（折叠）。
- 原来的判题阶梯（predict → complete → fix → write → variant → combine）不变，就是每个技能的练习。
- AI 助教的上下文里带上这道题的课的内容，可以一起聊这些知识点。

### 目录

```
problems/<track>/lessons/<lesson-id>/lesson.yaml   一个文件讲一组相关技能（比如 0A 的一组），每一步标明讲哪个技能
```

lesson-id 格式为 `<skill_prefix>-<阶段小写>-l<两位序号>-<slug>`，例如 `py-0a-l01-basics`。

### lesson.yaml

```yaml
id: py-0a-l01-print
title: 第一个程序：print              # 中文
track: python
skills: [py.print-basic, py.print-multi]   # 本文件讲的技能；每个技能只能在一个 lesson 文件里讲
steps:                                # 按讲解顺序；每一步必须写 skill，且属于上面的 skills
  - type: read                        # 讲解：Markdown，一个技能一般 150–500 字，配小例子，点名常见误解
    skill: py.print-basic
    md: |
      ...
  - type: example                     # 示例代码：可运行、可以改了再运行（不判对错）
    skill: py.print-basic
    code: |
      # ① 准备数据            ← 用注释给每个步骤起名字（子目标）
      name = "dojo"
      # ② 输出
      print("hello", name)
    md: |                             # 可选：代码下面的说明（"试试把……改成……再运行"）
      ...
    stdin: ""                         # 可选
  - type: quiz                        # 小测：单选，每个技能 0–2 道，针对具名误解
    skill: py.print-basic
    q: 下面哪一行会输出 3？
    options: ["print(1 + 2)", "print('1 + 2')", "print(1, 2)"]
    answer: 0
    explain: |
      ...
```

课的 example 也可将 `code` 换成单个 `data`，同一示例二选一；`file` 相对于 lesson.yaml 所在目录解析。

```yaml
  - type: example
    skill: data.table-intro
    data:
      kind: csv
      title: 图书登记
      content: |
        编号,书名
        B1,夜航
        B2,远山
    md: 改动一个书名，再切回表格看同一行。
```

table、csv、json 示例可切换表格、可编辑 CSV、只读 JSON。表格和 JSON 共用当前 CSV 草稿，原文件保持原样。JSON 视图每行一个对象，以不同的非空列名作键，普通字段保留文字，空字段为 null，`""` 为空字符串。原始 JSON 示例会先按对象的键展开为 CSV，嵌套值作为字段文本，标量放进“值”列。schema 与 values 示例直接显示。

- 每个被某道题 `introduces` 的技能，必须在某个 lesson 文件里至少有一段 read 和一个 example。
- SQL 的 example 写 `db: bookstore`（可加 `patch: <sql>`），平台在书店库上运行并显示结果表，支持修改查询和恢复示例。
- 0 基础：讲解默认读者从没学过；先讲"是什么、为什么"，再讲写法，最后点出常见误解。

### problem.yaml 新字段

```yaml
optional: true                      # 选修（数学与几何、位运算等）
replaces_premium: meeting-rooms     # 替代某道 LeetCode 会员题的原创题：写原题 slug；source 写 original
wrong_examples:                     # 典型错误写法（SQL 已在用；Python 可选），校验时必须至少挂一个测试
  - why: 忘了 NULL 不等于任何值
    sql: SELECT ... WHERE x <> 1     # Python 题用 code:
```

### 平滑性检查对课的要求

`scripts/curriculum/check_curve.py` 增加：lesson 文件格式正确；每一步的 skill 存在且属于该文件的 skills；每个技能最多在一个 lesson 文件里讲；每个被 `introduces` 的技能都有 read + example。
