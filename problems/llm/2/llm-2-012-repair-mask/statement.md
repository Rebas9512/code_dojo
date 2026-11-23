## 题目

修正初始代码。修复遮挡方向，让查询只读到当前及之前的位置。初始代码的首行会看到后文。

## 示例

三行零分数时首行应为 [1,0,0]。

## 约束

输入为方形分数矩阵，返回同形的因果权重。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
