完整模型把编号变成向量，连续运行几个 Transformer 块，再把每个位置变成一行词表分数。训练和续写共用这个前向过程。

## 接口

`GPT(vocab_size, context, width, heads, layers)` 继承 `nn.Module`。注册字符嵌入 `token`、可学习的绝对位置嵌入 `position`、由 layers 个独立 Block 构成的 `blocks`、末层 `norm`（LayerNorm）及无偏置的词表线性层 `head`。`forward(ids, targets=None, cache=None)` 返回 `(logits, loss, presents)`。将两种嵌入相加，按顺序运行各块、末层归一化、输出投影。

## 示例

输入 (2,3)、词表 7 时输出 (2,3,7)；有标签时交叉熵对全部 6 个位置取平均。缓存已有 2 格，再输入 1 个字时查位置 2，只输出本次 1 行分数。

## 约束

ids 与可选 targets 都是 (B,T) 的 long 张量；targets 已右移。无标签时 loss 为 None。cache 为 None 或按层排列的 (K,V) 序列；返回每层追加后的缓存。历史加本段的长度不超过 context。独立判题提供 Block。
