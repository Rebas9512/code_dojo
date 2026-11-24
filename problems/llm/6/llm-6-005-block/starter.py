class Block(nn.Module):
    def __init__(self, width, heads):
        """建立两个归一化层与两个计算分支。"""

    def forward(self, x, past=None):
        """更新两条残差路径并传回缓存。"""
