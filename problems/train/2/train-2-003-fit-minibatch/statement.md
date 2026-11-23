## 题目

实现 train(model, data, optimizer, steps)。每步对完整训练批前向，计算 data.loss，清梯度、反向并更新一次。

## 示例

本次四个点都满足 y=2x。正确更新后，最后几步的平均误差会比开始小。

## 约束

模型是带偏置的一元线性层；data.train 给出 (x,y)，data.loss 计算本批均方误差。 不需要返回值。
