## 题目

补全初始代码中的省略号。补出总体方差，让每个词沿最后一轴归一化。暂时省略可学习的缩放、平移。

## 示例

[2,6] 的偏差为 [−2,2]，除以 √(4+eps)。常数行输出全零。

## 约束

每行至少一格，eps > 0。禁止直接调用 LayerNorm。 禁用 `torch.nn.LayerNorm`、`torch.nn.functional.layer_norm`、`torch.layer_norm`。
