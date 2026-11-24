## 题目

同一批数字跑两次，想核对每一轮的 loss，就得先让模型从同一起点出发。把脚本共用的超参数放进一个配置对象，由它重置三个随机数源。

实现 `@dataclass class Config`，提供实例方法 `set_seed(self)`。公共骨架已导入 `dataclass`。字段和默认值如下，构造时可用关键字覆盖任意字段。

| 字段 | 类型 | 默认值 |
| --- | --- | ---: |
| seed | int | 42 |
| epochs | int | 40 |
| batch_size | int | 64 |
| hidden_size | int | 96 |
| lr | float | 0.006 |
| weight_decay | float | 0.01 |
| step_size | int | 12 |
| gamma | float | 0.5 |
| max_norm | float | 1.0 |
| patience | int | 10 |

`set_seed()` 把 Python 的 `random`、NumPy 的全局随机数源和 CPU PyTorch 都设到 `self.seed`。

## 示例

`Config().batch_size` 是 `64`。

`cfg = Config(seed=0, batch_size=1)` 后，调用 `cfg.set_seed()`，用 `torch.rand(3)` 抽三个数。再设一次种子并重抽，会得到相同的三个数。

## 约束

种子在 0 到 2³²−1 之间。调用者可以同时持有不同配置。
