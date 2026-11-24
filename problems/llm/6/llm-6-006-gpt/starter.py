class GPT(nn.Module):
    def __init__(self, vocab_size, context, width, heads, layers):
        """建立嵌入、块序列、末层归一化与词表头。"""

    def forward(self, ids, targets=None, cache=None):
        """返回分数、可选损失和逐层缓存。"""
