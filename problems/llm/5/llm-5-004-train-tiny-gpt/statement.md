## 题目

实现 train_lm(model, data, optimizer, steps)。判题器把 abcabcabcabc 切成错开一格的训练对，并提供一块小 GPT。每步在 data.train 的整批上前向，用 data.loss(logits, targets) 计算交叉熵，清梯度、反向、更新。最后在 data.evaluating()、eval 模式和无梯度环境中对 data.valid 的输入做一次前向。

## 示例

文本 abcab 可提供输入 abca、目标 bcab；若输入有 (3,6) 个位置，模型返回 (3,6,3)，data.loss 会对齐这 18 个词。

## 约束

使用传入的模型、SGD 和步数，无需返回 loss。5 个种子各跑 24 步；最后 5 步损失均值须低于最初 5 步的一半，逐步损失与固定训练脚本对拍。
