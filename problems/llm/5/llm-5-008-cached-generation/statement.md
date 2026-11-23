## 题目

实现 generate_cached(model, prompt, steps)。首轮将整段提示作为批大小 1 的原生整型张量送入 project；随后每轮仅计算刚生成的一词，保留历史 K、V 与正确的绝对位置。贪心选择新词，返回含提示的 Python 编号列表。

判题器给同一块 GPT 提供两个方法：

- `model.project(ids, start)` 对这一段按绝对位置嵌入，返回旁路 x 和 Q、K、V。x 为 (B,T,C)，后三者为 (B,H,T,D)。
- `model.finish(x, mixed)` 接收 x 和分头加权后的 (B,H,T,D)，完成输出投影、残差、MLP 与词表读出，返回 (B,T,V) logits。

每个新查询允许看绝对位置小于等于自己的键；缩放用 √D。

## 示例

提示长度 3，生成 3 个词时三次投影的 (起点,长度) 为 (0,3)、(3,1)、(4,1)。最后生成的词无需再投影。

## 约束

仅按 steps 停止；steps=0 时直接返回，不调用模型。总长度 ≤ 16。整串编号须与每轮重算完整前缀的 GPT 精确一致。 禁用 `torch.nn.functional.scaled_dot_product_attention`、`torch.nn.MultiheadAttention`。
