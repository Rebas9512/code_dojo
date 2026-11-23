## 题目

修复编辑器中的完整训练函数。脚本中有一处错误。

每步用 data.train 做一次前向、data.loss、清梯度、反向和参数更新。训练目标是 y=2x，损失为均方误差。更新结束后调用 model.eval()，在 data.evaluating() 和 torch.no_grad() 中用 data.valid[0] 做一次前向。

## 示例

脚本已经使用独立验证批，梯度记录也已暂停；插桩发现验证前向时 model.training 仍为 True。

## 约束

判题器按给定步数与固定种子运行小批次，逐步核对更新与损失轨迹。
