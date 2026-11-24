GPT 要堆叠多个相同结构的块。这一块先借助注意力读上下文，再用前馈层加工特征，两次更新都要接上残差。

## 接口

`Block(width, heads)` 继承 `nn.Module`。注册独立的 `norm1`、`norm2`（默认 nn.LayerNorm(width)）、`attention = CausalAttention(width, heads)`、`mlp = build_mlp(width)`。`forward(x, past=None)` 返回 `(output, present)`。向注意力传入第一层归一化的结果与 past，把其输出加回 x。对更新后的值做第二次归一化、前馈，再加回这一次的输入。

## 示例

若两个分支分别给残差加 2 和 3，输入 10 会依次变为 12、15。带 3 格历史处理 1 个新字符时，输出仍只有 1 个位置，返回的键和值各有 4 格。

## 约束

输入形状 (B,T,C)，缓存格式沿用注意力部分。两条残差路径都要传递梯度。独立判题会提供注意力和前馈层。
