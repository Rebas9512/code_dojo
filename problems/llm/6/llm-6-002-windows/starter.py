class TextWindows:
    def __init__(self, ids):
        """按原文顺序切出训练段和验证段。"""

    def get_batch(self, split, batch_size, context, generator):
        """随机取一批输入窗口和向右错开一格的目标。"""
