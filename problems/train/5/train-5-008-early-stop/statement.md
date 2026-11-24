## 题目

验证准确率可能先升后降。早停器在成绩刷新时记住训练现场，并告诉主循环何时结束等待。

实现 `EarlyStopping(patience, checkpoint)`。每个轮末调用 `observe(epoch, accuracy, model, optimizer) -> bool`。首轮或准确率严格超过历史最高值时，调用 `checkpoint.save(model, optimizer, epoch)`，等待数归零。持平或变差则累加等待，达到 `patience` 时返回 `True`，其余返回 `False`。

`restore(model, optimizer) -> int` 调用 `checkpoint.load(model, optimizer)` 恢复首次最佳轮，返回它的轮号。判本题时已有可读写的检查点实现。

## 示例

准确率依次为 `[0.5, 0.8, 0.8, 0.7]`、耐心为 2 时，在第 4 轮停下，恢复第 2 轮。

只跑一轮，即使准确率是 `0.0`，恢复的也是第 1 轮。

## 约束

轮号从 1 起，准确率介于 0 和 1 之间，耐心至少为 1。至少观察过一轮才调用恢复。
