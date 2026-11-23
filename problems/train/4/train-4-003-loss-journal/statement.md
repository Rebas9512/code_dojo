## 题目

实现 train，在 data.train 上做 steps 次五步更新。返回一个长度为 steps 的列表，每项都是用来做本次 backward 的 loss 的 Python 浮点值。

## 示例

第一步若算出 4.0，更新后重算可能得到 1.0，本步应记 4.0。

## 约束

用 data.loss 算均方误差；不要让日志条目保留计算图。
