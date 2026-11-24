class EarlyStopping:
    def __init__(self, patience, checkpoint):
        """记住等待上限和检查点。"""

    def observe(self, epoch, accuracy, model, optimizer):
        """观察本轮验证结果，返回是否停止。"""

    def restore(self, model, optimizer):
        """恢复最佳现场并返回轮号。"""
