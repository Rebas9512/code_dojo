训练循环把批次、模型、优化器和学习率接在一起。它也在同一组留出窗口上定期测量损失，让各次验证可以直接比较。

## 接口

`train_model(model, data, optimizer, cfg)` 返回按时间排列的 `[(step, mean_val_loss), ...]`。训练生成器用 cfg.seed 初始化一次。每步切到 train，按 learning_rate(step, cfg.steps, cfg.warmup, cfg.peak, cfg.floor) 更新所有参数组。调用 data.get_batch("train", cfg.batch_size, cfg.context, rng)，清梯度，计算 model(x,y) 返回的 loss，反向传播，按 cfg.clip 做全模型梯度范数裁剪，再更新。

## 示例

若 steps=5 且 eval_every=2，则在第 0、2、4、5 步验证，共 5 次参数更新。每次验证都重新用 seed+1 建生成器，取 eval_batches 批 "valid"，记录这些批损失的算术平均。

## 约束

每次验证切到 eval 并关闭梯度，结束时模型处于 eval 状态。需打印各次验证进度（英文，可自定格式）。最后一步即使不是整周期也要测，只测一次。所有批次尺寸合法，步骤和批数均为正。
