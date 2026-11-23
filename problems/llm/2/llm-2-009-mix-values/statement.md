## 题目

手写单头缩放点积注意力。给定三个矩阵 Q、K、V，返回每个查询对值的加权平均；所有键可见。

## 示例

一个零查询对应的两个值分别是 [2]、[8]，输出 [[5.0]]。

## 约束

Q、K 宽度相同，K、V 行数相同。值的宽度可以和键不同。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
