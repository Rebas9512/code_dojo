## 题目

实现 gpt_logits(ids, state)。用原生 LongTensor `ids` 和给定的 `state`（state_dict）写一块 GPT 的前向，返回每一格未经 softmax 的 logits。矩阵按 (输出宽, 输入宽) 保存。模型没有 dropout，所有线性层均无偏置。

| 字典键 | 形状与用途 |
|---|---|
| token.weight / pos.weight | (32,48) / (16,48)，分别按编号、从 0 起的位置查表后相加 |
| n1、n2、final 的 .weight 和 .bias | 各 (48,)，LayerNorm 用总体方差，eps=1e-5 |
| qkv.weight | (144,48)，对 n1(x) 一次投影，最后一轴依次为完整 Q、K、V |
| proj.weight | (48,48)，4 头因果注意力合头后的输出投影 |
| up.weight / down.weight | (96,48) / (48,96)，精确 GELU 前后的两层 |
| readout.weight | (32,48)，独立输出表 |

先令 y=x+注意力分支；再令 z=y+down(GELU(up(n2(y))))；最后用 final(z) 给词表打分。

## 示例

若输入是一批 3 个编号，输出形状为 (1,3,32)。改动第三个编号时，前两行 logits 应保持相同。

## 约束

B ≥ 1，1 ≤ T ≤ 16，C=48，H=4，每头宽 12。用例给出种子、批数、句长；判题器据此创建原生参数。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
