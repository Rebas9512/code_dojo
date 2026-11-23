# 21 · 进阶线「训练」（`train`）：技能图 + 课 + 题，线改成 active

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
- `problems/train/` 全部；
- `docs/curriculum.md` 里新加的这条线一节；
- `docs/teaching-design.md` 里新加的这条线误解目录；
- `check_curve.py` 识别表里新加的行（只加不改）。

## 线的设置

`problems/train/track.yaml` 里已有阶段：1 数据管道、2 训练循环、3 评估和调参、4 训练脚本改错。阶段可以微调，写进报告。

收尾时：
- 改成 `status: active`；
- 补上各阶段的 `units`；
- 技能加 `group`。

前置线：ml。技能可以跨线引用这些线的技能。

## 要做的事

用户说："模型训练的内容可以只做训练脚本的检查或者模拟训练 不一定需要真的把模型训练出来"。这条线的判法**以模拟训练和插桩检查为主**：小数据、几十步、固定种子，见 15 的 `dojo_train`。

- **阶段 1 数据管道**：
  - `Dataset`（`__len__`、`__getitem__`）
  - `DataLoader`：批大小、`shuffle` 用带种子的 generator、`drop_last`
  - `collate_fn`：变长序列的补齐，回指根线的 `data.missing`、padding
  - 训练集和验证集划分
- **阶段 2 训练循环**：
  - 标准的五步：前向、算 loss、`zero_grad`、`backward`、`step`
  - loss 函数的输入约定：CrossEntropyLoss 吃 logits 和类别下标
  - 优化器：SGD、momentum、Adam
  - 学习率调度
  - 梯度裁剪
- **阶段 3 评估和调参**：
  - `model.eval()` 加 `torch.no_grad()`
  - 验证指标
  - 早停
  - 权重衰减、dropout（`train` / `eval` 下行为不同）
  - 保存和加载 checkpoint（`state_dict`，写进内存里的 BytesIO 就行）
  - **读 loss 曲线判断问题**：用 inspect 题型，数据块给训练和验证 loss 的数值序列，问是过拟合、欠拟合、学习率太大还是有 bug
- **阶段 4 训练脚本改错**：给一段有 bug 的完整训练脚本（fix 格式），修好后通过模拟训练检查。bug 清单：
  - 忘了 `zero_grad`
  - `zero_grad` 放在 `backward` 和 `step` 之间
  - CrossEntropyLoss 前多做了 softmax
  - 标签 dtype 或形状错
  - 评估时没切 `eval`
  - 评估时没 `no_grad`
  - 验证集混进了训练
  - 学习率大了 100 倍
  - `.item()` 忘了写，导致计算图越积越大
  - 打乱数据时特征和标签没对齐

  每道题只放一个 bug。最后加 2–3 道综合题，一题多个 bug。
- **判法**：主要用模拟训练和插桩。
  - 断言 loss 下降、能过拟合一个小批次、和参考实现同种子下的 loss 轨迹一致。
  - 违反时给中文说明，比如"第 2 步开始梯度在累加"。

## 通用要求

- **数量**：每个技能按"预测（含形状预测）→ 补全 →（改错）→ 独立写"搭阶梯。题量约 60–80。
- **编号**：题号 `train-<阶段>-NNN-slug`，order 从 10 起、步长 10。
- **课**：每个组一个课文件 `train-<阶段>-lNN-…`。
  - 讲解、可运行示例、小测三步都要有。
  - 示例要在 playground 里（按 runtime 用 ds 镜像）跑出注释写的结果。
- **`wrong_examples`**：每题都要有，并确认它们被判错。这条线最典型的错误，见上面"要做的事"。
- **随机性**：一律固定种子（`torch.manual_seed`、`np.random.default_rng(0)`），或者把随机数作为参数传进来。
- **性能**：单题在 ds 镜像里控制在几秒内，别让参考解跑太久。
- **参考来源**：只参考思路，题面和代码自己写。

## 验收标准

1. `cd server && .venv/bin/python ../scripts/verify_bank.py --only train- --jobs 4` 全过。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track train`：0 错 0 警。
3. 课程示例全部能跑：用 verify 脚本或 playground 接口核对，写进报告。
4. 起测试实例（8001 和 5174，见 brief），首页这条线变成实线，能做题。抽 3 道不同判法的题在浏览器里提交一遍，截图放 `{RUN_DIR}/`。
5. 报告里列出：
   - 技能清单（id、名称、阶段、组、前置）
   - 每组题数和题型统计
   - 每种判法用在了哪些题
