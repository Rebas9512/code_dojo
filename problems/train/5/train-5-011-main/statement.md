## 题目

前十块提供了一套可独立复用的训练工具。现在把它们连进命令行入口，让每一轮的状态有日志可追，最终分数能和磁盘上的最佳权重对应起来。

实现无参数入口 `main()`。用 argparse 支持整数选项 `--epochs`、`--seed`、`--batch-size`、`--patience`，默认取 `Config()` 的同名配置。`--checkpoint` 默认是当前目录的 `best.pt`。

1. 应用配置与种子，在 CPU 上运行（小网络可用 `torch.set_num_threads(1)`）。从 `DATA_DIR / "digits.csv"` 创建数据集，将 `round(0.2 * len(dataset))` 张留作验证。按配置创建加载器、小 MLP、AdamW、StepLR、交叉熵、检查点及早停器。
2. 从第 1 轮开始。记录当前学习率，训练一轮并验证一次。把 `epoch_record` 的结果以一行 JSON 打印，再执行一次轮末调度，让准备保存的优化器持有下一轮的步长。用本轮准确率更新早停器，触发时立即结束训练。
3. 触发早停或跑满指定轮数后，恢复最佳轮的模型和优化器。**用恢复后的模型重新验证**。最后一行打印含 `best_epoch` 与 `val_accuracy` 的 JSON 对象。

## 示例

`python train.py --epochs 1` 输出一行带 `epoch`、`loss`、`val_accuracy`、`lr` 的 JSON 日志，接着一行总结，`best_epoch` 为 `1`。

`python train.py --epochs 3 --seed 7 --batch-size 8 --patience 2 --checkpoint trial.pt` 最多打印三行训练日志。若三轮准确率依次为 0.75、0.875、0.75，最后一行是 `{"best_epoch": 2, "val_accuracy": 0.875}`。

## 约束

轮数、批大小与耐心都是正整数。训练和验证都非空。实际项目有 1,797 张图，按默认参数运行，验证准确率至少为 0.95，限时 60 秒。
