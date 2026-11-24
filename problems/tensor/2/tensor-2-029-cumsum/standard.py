import torch


def cumsum(x):
    i = torch.arange(len(x))
    # 每轮合并两个相邻区间，左边越界的位置贡献为零。
    s2 = x + (i >= 1) * x[(i - 1) % len(x)]
    s4 = s2 + (i >= 2) * s2[(i - 2) % len(x)]
    return s4 + (i >= 4) * s4[(i - 4) % len(x)]
