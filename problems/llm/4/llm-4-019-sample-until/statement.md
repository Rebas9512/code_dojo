## 题目

用 table[末词] 作为下一词 logits。依次除以 temperature、保留 top-k、在这 k 项归一化后的概率中保留累计首次达到 p 的前缀。其余项屏蔽后再抽一个，追加到提示。提示或新词以 eos 结束，或新增 limit 个后停。使用 float64 的原词表顺序概率向量。建一个 torch.Generator().manual_seed(seed)，有放回地逐次调用 torch.multinomial(prob, 1, generator=...)，连续使用同一生成器。返回 Python 整数列表。

## 示例

k=1 时等价于贪心；若首步抽到 EOS，只会添加这一个词。

## 约束

同分时较小编号先选。1 ≤ k ≤ V，0 < p ≤ 1，temperature > 0，提示非空。若因浮点舍入到末项仍未达标，保留全部 k 项。
