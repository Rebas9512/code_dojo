## 题目

只保留 top-k 原编号，同分优先小编号。屏蔽其余分数，做 softmax，再抽 count 次。使用 float64 的原词表顺序概率向量。建一个 torch.Generator().manual_seed(seed)，有放回地逐次调用 torch.multinomial(prob, 1, generator=...)，连续使用同一生成器。返回 Python 整数列表。

## 示例

[4,4,0] 且 k=1 时只留下编号 0，不管种子如何，三抽都是 [0,0,0]。

## 约束

1 ≤ k ≤ V，count ≥ 0。用例直接给出分数、k、次数和种子。
