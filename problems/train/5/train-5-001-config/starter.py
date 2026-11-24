@dataclass
class Config:
    """保存训练配置，在 set_seed(self) 中重置三个随机数源。"""

    def set_seed(self):
        """从本配置的种子重新开始抽样。"""
