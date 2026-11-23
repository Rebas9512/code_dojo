## 题目

对输入每行手写 LayerNorm，再按特征乘 gamma、加 beta。结果与固定参数的 nn.LayerNorm 对拍。

## 示例

整行 [3,3] 归一化后为零；若 beta=[2,1]，该行最终就是 [2,1]。

## 约束

eps 在根号内，使用总体方差。gamma、beta 的长度均等于行宽。 禁用 `torch.nn.LayerNorm`、`torch.nn.functional.layer_norm`、`torch.layer_norm`。
