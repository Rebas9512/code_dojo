## 题目

补全初始代码中的省略号。给 (B,T,C) 的输入和头数 H，返回 (B,H,T,C/H)。

## 示例

[0,1,2,3] 与 [4,5,6,7] 两个词各切两半。头 0 按时间读到 [0,1] 和 [4,5]。

## 约束

各轴非空，C 是 H 的倍数。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
