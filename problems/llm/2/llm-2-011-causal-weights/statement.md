## 题目

补全初始代码中的省略号。把方阵 scores 的严格上三角填成 −∞，再沿每行做 softmax。

## 示例

两行全零得到 [[1,0],[0.5,0.5]]。

## 约束

方阵边长至少为 1；返回浮点权重。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
