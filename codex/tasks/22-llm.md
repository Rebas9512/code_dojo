# 22 · 进阶线「手搓 LLM」（`llm`）：技能图 + 课 + 题，线改成 active

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
- `problems/llm/` 全部；
- `docs/curriculum.md` 里新加的这条线一节；
- `docs/teaching-design.md` 里新加的这条线误解目录；
- `check_curve.py` 识别表里新加的行（只加不改）。

## 线的设置

`problems/llm/track.yaml` 里已有阶段：1 分词、2 嵌入和注意力、3 Transformer 块、4 GPT 前向和采样、5 训练和 KV cache。阶段可以微调，写进报告。

收尾时：
- 改成 `status: active`；
- 补上各阶段的 `units`；
- 技能加 `group`。

前置线：train。技能可以跨线引用这些线的技能。

## 要做的事

从零手写一个很小的 GPT。每一步都和参考实现对拍：固定权重或固定种子，`allclose`。参考 Karpathy 的 nanoGPT、minbpe（MIT），以及 rasbt 的 LLMs-from-scratch（Apache-2.0），只参考思路，代码和题面自己写。

- **阶段 1 分词**：
  - 字符级分词：建表、`encode` / `decode`
  - 字节和 UTF-8：回指根线 `data.text-formats` 和 Python 的 `ord` / `chr`
  - BPE：统计相邻对、合并一次、训练 k 次合并、用学到的合并去编码。小语料上和参考实现结果完全一致
  - 特殊 token
- **阶段 2 嵌入和注意力**：
  - `nn.Embedding` 是查表：回指 tensor 线的索引
  - 位置嵌入
  - 缩放点积注意力：先单头、不带掩码
  - 因果掩码（`masked_fill` 成 `-inf` 再 softmax）
  - 多头：拆头、合头的形状变换，多出形状预测题
  - 用 `forbid_calls` 禁止 `F.scaled_dot_product_attention` 和 `nn.MultiheadAttention`
- **阶段 3 Transformer 块**：
  - LayerNorm：手写，和 `nn.LayerNorm` 对拍
  - 残差连接
  - MLP（GELU）
  - pre-norm 块
  - 参数量计算：预测题
- **阶段 4 GPT 前向和采样**：
  - 组装一个很小的 GPT：几万参数，给定 `state_dict`，logits 和参考实现 `allclose`
  - 贪心解码
  - temperature
  - top-k 和 top-p：用带种子的 generator
  - 停止条件
- **阶段 5 训练和 KV cache**：
  - 在一小段文本上训练几十步，loss 下降：模拟训练
  - 用 KV cache 生成，结果和不用 cache 完全一致
  - 计算省了多少：预测题
- **判法**：数值对拍、写法约束、模拟训练；BPE 和解码结果用精确比较。
- **典型错误**：
  - 注意力忘了除以 √d
  - 掩码方向反了，能看到未来
  - softmax 的维度错
  - 拆头时 `view` 和 `transpose` 顺序错
  - LayerNorm 的方差用了无偏估计
  - 位置编码长度不够
  - temperature 用乘不用除
  - KV cache 拼接维度错

## 通用要求

- **数量**：每个技能按"预测（含形状预测）→ 补全 →（改错）→ 独立写"搭阶梯。题量约 60–80。
- **编号**：题号 `llm-<阶段>-NNN-slug`，order 从 10 起、步长 10。
- **课**：每个组一个课文件 `llm-<阶段>-lNN-…`。
  - 讲解、可运行示例、小测三步都要有。
  - 示例要在 playground 里（按 runtime 用 ds 镜像）跑出注释写的结果。
- **`wrong_examples`**：每题都要有，并确认它们被判错。这条线最典型的错误，见上面"要做的事"。
- **随机性**：一律固定种子（`torch.manual_seed`、`np.random.default_rng(0)`），或者把随机数作为参数传进来。
- **性能**：单题在 ds 镜像里控制在几秒内，别让参考解跑太久。
- **参考来源**：只参考思路，题面和代码自己写。

## 验收标准

1. `cd server && .venv/bin/python ../scripts/verify_bank.py --only llm- --jobs 4` 全过。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track llm`：0 错 0 警。
3. 课程示例全部能跑：用 verify 脚本或 playground 接口核对，写进报告。
4. 起测试实例（8001 和 5174，见 brief），首页这条线变成实线，能做题。抽 3 道不同判法的题在浏览器里提交一遍，截图放 `{RUN_DIR}/`。
5. 报告里列出：
   - 技能清单（id、名称、阶段、组、前置）
   - 每组题数和题型统计
   - 每种判法用在了哪些题
