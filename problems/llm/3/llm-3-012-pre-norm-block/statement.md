## 题目

函数接收 x、norm1、attention、norm2、mlp，后四项都是可调用层。按 pre-norm 顺序接好两条分支，返回块的输出。第一分支已经包含因果注意力与输出投影的接口。

## 示例

若两条分支都返回零，出口必须与原输入逐格相同。

## 约束

输入是 (B,T,C) 原生浮点张量；每个层均保留此形状。测试输入是固定种子。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
