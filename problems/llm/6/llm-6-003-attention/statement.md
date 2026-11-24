这层让每个位置分别从不同的头读取已有字符。生成时同一层还会接回上一次保存的键和值。

## 接口

`CausalAttention(width, heads)` 继承 `nn.Module`。设 `qkv` 为无偏置线性层 (C → 3C)，输出依次为 Q、K、V；`proj` 为无偏置输出投影 (C → C)。`forward(x, past=None)` 返回 `(output, (k, v))`。x 和输出均为 (B,T,C)，每头宽 D=C/H。每头用 QKᵀ/√D 算分数，屏蔽未来，对键轴做 softmax，再加权 V、合头、做输出投影。

## 示例

长度为 3、无历史时，第 0 个位置只能看键 0。若已有 2 个键，本次一次送入 2 个字符，两行查询可以分别看键 0–2、0–3；返回的缓存长度为 4。

## 约束

CPU 浮点张量。宽度可整除头数。缓存缺省时没有历史，否则是两个 (B,H,P,D) 张量；沿时间轴把本段接在末尾。权重需要保留梯度。 请手写注意力计算，不使用 MultiheadAttention 或 scaled_dot_product_attention。
