模型每读一个字都要猜下一个字。这一部分先留出文章末尾作验证，再从指定的一段抽取连续窗口。

## 接口

`TextWindows(ids)` 将编号转为一维 `torch.long`，在 `9 * len(ids) // 10` 切开为 `train` 与 `valid`。方法 `get_batch(split, batch_size, context, generator)` 返回两个形状为 `(batch_size, context)` 的 long 张量。用传入的生成器和一次 `torch.randint` 等概率、有放回地抽取每行起点。

## 示例

假如某行从编号串 `[3, 7, 2, 1]` 开头取宽度 3，输入是 `[3, 7, 2]`，目标是 `[7, 2, 1]`。把 0 到 19 分段后，在 `valid` 取宽度 1 只能得到 `[18] → [19]`。

## 约束

`split` 为 `"train"` 或 `"valid"`。所选段至少有 `context + 1` 个字符。最后一个合法起点也能抽到。连续调用共用传入的随机状态。
