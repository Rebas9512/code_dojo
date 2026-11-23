## 题目

用 np.random.default_rng(seed).permutation(n) 打乱行号，返回前 count 个整数，保留抽中顺序。补全编辑器中标记的一处。

## 示例

输入 `test_indices(4, 2, 0)`，应返回 `[2, 0]`。

## 约束

1≤count<n，seed 为非负整数。
使用 NumPy 手写计算。
