# 19 · 进阶线「张量与 PyTorch」（`tensor`）：技能图 + 课 + 题，线改成 active

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
- `problems/tensor/` 全部；
- `docs/curriculum.md` 里新加的这条线一节；
- `docs/teaching-design.md` 里新加的这条线误解目录；
- `check_curve.py` 识别表里新加的行（只加不改）。

## 线的设置

`problems/tensor/track.yaml` 里已有阶段：1 张量和形状、2 索引和掩码、3 einsum、4 自动求导和 nn.Module。阶段可以微调，写进报告。

收尾时：
- 改成 `status: active`；
- 补上各阶段的 `units`；
- 技能加 `group`。

前置线：wrangle、math。技能可以跨线引用这些线的技能。

## 要做的事

- **阶段 1 张量和形状**：
  - 创建张量；dtype；`.shape` / `.ndim`
  - `view` / `reshape` / `permute` / `transpose`（`contiguous` 是什么）
  - `unsqueeze` / `squeeze`
  - 广播（对照 NumPy）
  - 带 `dim` / `keepdim` 的聚合
  - **形状预测题要多**：读一段代码，写出每一步的形状。
- **阶段 2 索引和掩码**：
  - 切片
  - 布尔掩码
  - `gather` / `scatter`
  - `masked_fill`
  - `torch.where`
  - `topk` / `argmax`
  - 用张量操作写 one-hot：回指根线的 `data.quantity-vs-label`
- **阶段 3 einsum**：
  - 从矩阵乘法、批量矩阵乘、转置、对角线，到外积、注意力分数的写法
  - 每道题都和显式写法对拍
- **阶段 4 自动求导和 nn.Module**：
  - `requires_grad`、`backward`、`.grad`
  - 梯度会累加
  - `no_grad`、`detach`
  - `nn.Parameter`、`nn.Linear`
  - 自己写一个 `nn.Module`
  - `parameters()`、`state_dict`
- **Tensor Puzzles 风格的题**（srush/Tensor-Puzzles 是 MIT 许可，只参考思路）：只许用 `arange`、广播和索引，实现 `ones`、`sum`、`outer`、`diag`、`eye`、`triu`、`cumsum`、`diff`、`vstack`、`roll`、`flip` 这类函数。
  - 用 `forbid_calls` 禁止直接调用对应的库函数。
  - 用 `no_loops` 禁止循环。
- **典型错误**：
  - `view` 和 `reshape` 在非连续张量上的区别
  - 维度顺序搞反
  - `keepdim` 忘了加导致广播错位
  - 整数张量不能求导
  - 原地操作破坏计算图
  - 梯度没清零就累加了

## 通用要求

- **数量**：每个技能按"预测（含形状预测）→ 补全 →（改错）→ 独立写"搭阶梯。题量约 70–90。
- **编号**：题号 `tensor-<阶段>-NNN-slug`，order 从 10 起、步长 10。
- **课**：每个组一个课文件 `tensor-<阶段>-lNN-…`。
  - 讲解、可运行示例、小测三步都要有。
  - 示例要在 playground 里（按 runtime 用 ds 镜像）跑出注释写的结果。
- **`wrong_examples`**：每题都要有，并确认它们被判错。这条线最典型的错误，见上面"要做的事"。
- **随机性**：一律固定种子（`torch.manual_seed`、`np.random.default_rng(0)`），或者把随机数作为参数传进来。
- **性能**：单题在 ds 镜像里控制在几秒内，别让参考解跑太久。
- **参考来源**：只参考思路，题面和代码自己写。

## 验收标准

1. `cd server && .venv/bin/python ../scripts/verify_bank.py --only tensor- --jobs 4` 全过。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track tensor`：0 错 0 警。
3. 课程示例全部能跑：用 verify 脚本或 playground 接口核对，写进报告。
4. 起测试实例（8001 和 5174，见 brief），首页这条线变成实线，能做题。抽 3 道不同判法的题在浏览器里提交一遍，截图放 `{RUN_DIR}/`。
5. 报告里列出：
   - 技能清单（id、名称、阶段、组、前置）
   - 每组题数和题型统计
   - 每种判法用在了哪些题
