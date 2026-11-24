class CausalAttention(nn.Module):
    def __init__(self, width, heads):
        """建立多头投影。"""

    def forward(self, x, past=None):
        """返回本段输出和包含历史的键值对。"""
