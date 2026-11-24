## 题目

早停决定保留哪一轮，检查点负责把那一轮真正写到磁盘。读取后，新的模型和优化器要能从相同位置再走一步。

实现 `Checkpoint(path)`。方法 `save(model, optimizer, epoch)` 在该路径用 `torch.save` 写一个字典，键为 `"model"`、`"optimizer"` 和 `"epoch"`，分别保存两份 `state_dict()` 和轮号。

方法 `load(model, optimizer) -> int` 读取该文件，把两份状态装入传入的对象，返回保存的轮号。

## 示例

`Checkpoint("one.pt").save(model, optimizer, 1)` 后，另一实例从同一路径读取时返回 `1`。

第 5 轮保存时学习率是 `0.003`。读入初始学习率为 `0.9` 的同型优化器后，学习率恢复为 `0.003`，动量也接着原来的值。

## 约束

模型与优化器均在 CPU 上，读取目标与保存时的结构相同。路径父目录存在，读取前已保存。
