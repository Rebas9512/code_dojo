## 题目

写出完整 train，先对 data.train 完成 steps 次五步更新，再在 data.evaluating() 中取 data.valid 的输入做一次验证前向。

## 示例

训练数据为 y=2x；验证批采用不同的输入。验证只读取模型，此时不更新权重。

## 约束

用 data.loss 作为训练目标；验证时要切 eval 并关闭梯度。
