训练初期需要逐步增大步长，接近结束时再把步长降下来。这一部分只按更新编号计算学习率。

## 接口

`learning_rate(step, steps, warmup, peak, floor)` 返回浮点数。更新编号从 1 开始，第 1 至 warmup 步取 peak × step / warmup。余下的步以 p=(step−warmup)/(steps−warmup) 为进度，取 floor + (peak−floor) × (1+cos(πp))/2。

## 示例

共 10 步，预热 2 步，peak=1、floor=0.2。第 1 步为 0.5，第 2 步为 1.0，第 6 步为 0.6，第 10 步为 0.2。

## 约束

1 ≤ step ≤ steps，1 ≤ warmup < steps，0 ≤ floor ≤ peak。骨架已导入 math。
