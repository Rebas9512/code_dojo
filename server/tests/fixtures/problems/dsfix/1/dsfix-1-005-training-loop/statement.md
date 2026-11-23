## 题目
修复初始代码，让每一步使用当前小批次的梯度，再在验证集上评估一次。
## 示例
用输入 x 拟合目标 2x。第一步运行正常，从第二步开始 loss 偏离参考结果。
## 约束
用 data.train 训练，用 data.loss 计算损失。验证使用 data.evaluating()、model.eval() 和 torch.no_grad()。
