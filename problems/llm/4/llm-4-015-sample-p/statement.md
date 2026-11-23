## 题目

输入为 logits。先算 float64 概率，按概率降序（同分小编号优先）取累计首次达到 p 的最短前缀。在原词表顺序将其余 logits 遮为 −∞，重新 softmax 后抽样。使用 float64 的原词表顺序概率向量。建一个 torch.Generator().manual_seed(seed)，有放回地逐次调用 torch.multinomial(prob, 1, generator=...)，连续使用同一生成器。返回 Python 整数列表。

## 示例

相同的四个分数、p=0.5，前两个编号已恰好达标；任何抽样只会得到 0 或 1。

## 约束

0 < p ≤ 1，count ≥ 0。求累计质量时顺次相加。
