## 题目

同一套模型参数要跨批次积累 AdamW 的状态。这里给模型配一个优化器，再让学习率调度器在指定轮数过后缩小步长。

实现 `make_optimizer(model, config)`，返回 `(optimizer, scheduler)`。用全部模型参数创建 AdamW，设置 `lr=config.lr`、`weight_decay=config.weight_decay`。用同一个优化器创建 StepLR，使用 `config.step_size` 和 `config.gamma`。本函数只负责构造。

## 示例

初始学习率 0.01，每两轮乘 0.5。若每轮更新结束才调度，前三轮使用 `[0.01, 0.01, 0.005]`。

初始学习率 0.004，每轮乘 0.25，则第二轮使用 `0.001`。

## 约束

学习率、衰减周期均为正，权重衰减可以为 0。其余优化器选项保持 PyTorch 默认值。
