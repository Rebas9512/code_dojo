# 18 · 进阶线「数据处理」（`wrangle`）：技能图 + 课 + 题，线改成 active

## 背景

用户 2026-11-22 的原话：
- "到后面进阶的内容我也想做一些 比如数据科学类的 数据操作，模型训练，tensor操作，手搓大语言模型之类的"
- "像这种模型训练的内容可以只做训练脚本的检查或者模拟训练 不一定需要真的把模型训练出来"

设计在 `docs/README.md` 2b 节。

**平台**：15 号任务做好了数据科学判题镜像（numpy + pandas + CPU 版 torch），以及这些判法：
- `allclose`、`frame` 两种比较
- 写法约束 `constraints`
- 梯度检查工具
- 模拟训练工具 `dojo_train`

**动手前先读**：
- `codex/runs/15-ds-judge-*/report.md`
- `docs/problem-format.md` 里对应的几节
- `server/tests/fixtures/problems/` 下 15 写的夹具题

字段名和用法以它们为准。

**零基础**：学习者按零基础来设计。每个概念先讲它是什么、为什么要它，再给具体数字的小例子，然后才是代码。

**写法比照已有的线**：
- 数学线（`problems/math/`）：同是进阶线，看它的课和题怎么写。
- Python 基础线：看阶梯、`wrong_examples`、课的三步（read / example / quiz）。

**并行**：先读 `codex/PLAN.md`。你只负责：
- `problems/wrangle/` 全部；
- `docs/curriculum.md` 里新加的这条线一节；
- `docs/teaching-design.md` 里新加的这条线误解目录；
- `check_curve.py` 识别表里新加的行（只加不改）。
- 如果平台还不支持把 DataFrame 当作函数参数传进去，你可以对 harness 和格式文档做最小改动来支持，比如 `convert: dataframe`。这时没有其他平台任务在跑。改了什么写进报告。

## 线的设置

`problems/wrangle/track.yaml` 里已有阶段：1 NumPy 数组、2 广播和向量化、3 pandas 基础、4 分组合并和透视、5 pandas 版 SQL 题。阶段可以微调，写进报告。

收尾时：
- 改成 `status: active`；
- 补上各阶段的 `units`；
- 技能加 `group`。

前置线：python（以及根线 data）。技能可以跨线引用这些线的技能。

## 要做的事

- **阶段 1 NumPy 数组**：
  - 创建数组；dtype、shape、ndim
  - 一维和二维的下标、切片
  - 布尔掩码
  - 花式索引
  - reshape
  - 带 axis 的聚合
- **阶段 2 广播和向量化**：
  - 广播规则（形状对齐，从右往左比）
  - 向量化改写：用 `no_loops` 约束
  - `np.where`、`cumsum`、`argsort` / `argmax`
  - 亲手对比循环和向量化的耗时，可以做成预测题
- **阶段 3 pandas 基础**：
  - Series、DataFrame
  - 从 CSV 读入：数据放在题目目录，或者用字符串
  - `loc` / `iloc`、筛选、排序、新列
  - 缺失值 `isna` / `fillna` / `dropna`：回指根线的 `data.missing`
  - dtype 和类型转换：回指 `data.value-kinds`
- **阶段 4 分组合并和透视**：
  - `groupby` + `agg`
  - `merge`（四种连接，对照 SQL 的 JOIN）
  - `pivot_table`、`melt`
  - 日期列
  - `value_counts`
  - `apply` 和向量化写法的取舍
- **阶段 5 pandas 版 SQL 题**：用书店数据，和 SQL 线同一题两种写法。
  - 书店数据导出成 CSV，放在 `problems/wrangle/_data/bookstore/`。导出脚本放 `scripts/`，从 `problems/sql/_db/bookstore/` 生成，保证两边数据一致。
  - 挑 SQL 线里有代表性的 15–25 道题（选列、筛选、聚合、连接、窗口），用 pandas 再做一遍，`problem.yaml` 里写上对应的 SQL 题 id，比如 `sql_twin: sql-2-011-…`；这个字段格式里没有，就加进格式文档，写进报告。
  - 参考 LeetCode 的 Introduction to Pandas（15 题）和 30 Days of Pandas（33 题），题面自己写，写 `leetcode:` 出处。
- **典型错误**：
  - 广播时形状没对齐
  - 链式赋值（SettingWithCopy）
  - `groupby` 后忘了 `reset_index`
  - `merge` 后行数变多（一对多）
  - `NaN == NaN` 是 False
  - 整数列有缺失值后变成 float

## 通用要求

- **数量**：每个技能按"预测（含形状预测）→ 补全 →（改错）→ 独立写"搭阶梯。题量约 80–100。
- **编号**：题号 `wrangle-<阶段>-NNN-slug`，order 从 10 起、步长 10。
- **课**：每个组一个课文件 `wrangle-<阶段>-lNN-…`。
  - 讲解、可运行示例、小测三步都要有。
  - 示例要在 playground 里（按 runtime 用 ds 镜像）跑出注释写的结果。
- **`wrong_examples`**：每题都要有，并确认它们被判错。这条线最典型的错误，见上面"要做的事"。
- **随机性**：一律固定种子（`torch.manual_seed`、`np.random.default_rng(0)`），或者把随机数作为参数传进来。
- **性能**：单题在 ds 镜像里控制在几秒内，别让参考解跑太久。
- **参考来源**：只参考思路，题面和代码自己写。

## 验收标准

1. `cd server && .venv/bin/python ../scripts/verify_bank.py --only wrangle- --jobs 4` 全过。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track wrangle`：0 错 0 警。
3. 课程示例全部能跑：用 verify 脚本或 playground 接口核对，写进报告。
4. 起测试实例（8001 和 5174，见 brief），首页这条线变成实线，能做题。抽 3 道不同判法的题在浏览器里提交一遍，截图放 `{RUN_DIR}/`。
5. 报告里列出：
   - 技能清单（id、名称、阶段、组、前置）
   - 每组题数和题型统计
   - 每种判法用在了哪些题
