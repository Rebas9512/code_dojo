## 题目

手写单头因果自注意力：缩放点积，遮住未来，按键做 softmax，再乘 V。

## 示例

所有点积相同时，值 [2,8,5] 在三个位置的混合结果分别为 2、5、5。

## 约束

Q、K、V 都是二维，各有 T 行，Q、K 的宽度都是 d。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
