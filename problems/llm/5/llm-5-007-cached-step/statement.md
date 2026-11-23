## 题目

写 cached_step(model, ids, start, cache)。空历史时 cache 为 None，否则为旧 (K,V)。每次只投影传入的 ids 一次，拼接历史，计算当前段的因果注意力。返回 (新段 logits, (全部 K, 全部 V))。

判题器给同一块 GPT 提供两个方法：

- `model.project(ids, start)` 对这一段按绝对位置嵌入，返回旁路 x 和 Q、K、V。x 为 (B,T,C)，后三者为 (B,H,T,D)。
- `model.finish(x, mixed)` 接收 x 和分头加权后的 (B,H,T,D)，完成输出投影、残差、MLP 与词表读出，返回 (B,T,V) logits。

每个新查询允许看绝对位置小于等于自己的键；缩放用 √D。

## 示例

已有 3 个词，一次补 2 个，新段两行允许看到的键数量依次为 4、5。

## 约束

start 等于旧缓存长度。用例给出种子、批数与每段长度，总长 ≤ 16。逐段与一次整句前向对拍。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
