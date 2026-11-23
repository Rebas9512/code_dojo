## 题目

补全初始代码中的省略号。算 QKᵀ/√d，把每一行对键的分数变成概率，返回权重矩阵。

## 示例

一个零查询遇到两个键，权重为 [[0.5,0.5]]。

## 约束

q 和 k 为非空矩阵，最后一轴宽度相同。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
