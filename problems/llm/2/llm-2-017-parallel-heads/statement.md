## 题目

输入已经投影好的 Q、K、V，形状均为 (B,T,C)。拆成 H 头，各自计算缩放因果注意力，再恢复 (B,T,C)；本题没有输出投影。

## 示例

C=4、H=2 时，每头用 √2 缩放。首个词只能看自己，合头后就是 V 的第一行。

## 约束

C 能整除 H，各轴非空。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
