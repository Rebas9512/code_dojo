from pathlib import Path

import numpy as np
import torch


def check_function(args, expected, cls):
    start, count = args[0]
    pixels = (np.arange(count * 64).reshape(count, 64) + start) % 17
    labels = (np.arange(count) * 3 + start) % 10
    path = Path("samples.csv")
    header = ",".join([f"p{i}" for i in range(64)] + ["label"])
    np.savetxt(path, np.column_stack((pixels, labels)), delimiter=",", fmt="%d", header=header, comments="")
    dataset = cls(path)
    assert isinstance(dataset, Dataset) and len(dataset) == count, "数据集长度应等于样本行数"
    for i in range(count):
        x, y = dataset[i]
        assert x.shape == (64,) and x.dtype == torch.float32, "每张图应是 64 个 float32 像素"
        assert torch.equal(x, torch.tensor(pixels[i], dtype=torch.float32) / 16), "请按原顺序取像素，每个像素除以 16"
        assert y.shape == () and y.dtype == torch.long and y.item() == labels[i], "标签应是同一行的标量 long"
    return True
