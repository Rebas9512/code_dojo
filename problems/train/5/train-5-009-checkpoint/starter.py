class Checkpoint:
    def __init__(self, path):
        """记住检查点的路径。"""

    def save(self, model, optimizer, epoch):
        """保存模型、优化器与当前轮号。"""

    def load(self, model, optimizer):
        """读回训练现场并返回保存的轮号。"""
