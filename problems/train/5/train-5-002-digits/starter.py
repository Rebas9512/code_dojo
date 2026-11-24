class DigitsDataset(Dataset):
    def __init__(self, path):
        """从带表头的 CSV 读取像素和标签。"""

    def __len__(self):
        """返回图片张数。"""

    def __getitem__(self, index):
        """取出一张图和它的标签。"""
