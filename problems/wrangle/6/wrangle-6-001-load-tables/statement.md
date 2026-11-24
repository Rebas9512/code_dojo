后面要按人连接表、按时刻切窗口。这一步直接从目录读取登记、操作和付款原表，定好类型，给后面的清洗留下原始行。

```python
def load_tables(data_dir):
```

输入 `data_dir` 是一个 Path。按下面的顺序返回三张 DataFrame 组成的元组，保留全部列、列序、行序、重复行和缺失值。骨架已导入 `pandas as pd`。

| 文件 | 列（按原顺序） |
| --- | --- |
| readers.csv | user_id, joined_on, channel, city, device |
| events.csv | event_id, user_id, action, happened_at |
| payments.csv | payment_id, user_id, paid_at, amount |

所有编号用可空整数 `Int64`，金额用浮点数。其余文本字段以字符串保存，保留原样。空字段表示缺失；骨架提供 CSV_OPTIONS，可用 `pd.read_csv(..., **CSV_OPTIONS)` 保留 NA 这样的字面文本。三个日期或时间列都转成 UTC 日期时间；注册日取当天零点。时间可能有偏移量，也可能没有，无偏移按 UTC。空时间保留为 NaT。每个文件都有表头，可能没有明细。

## 示例 1

事件时间 `2025-02-01T01:00:00+08:00` 读成 `2025-01-31 17:00:00+00:00`，城市字段 ` YORK ` 仍带空格。

## 示例 2

同一条付款出现两次，读完还有两行。空的 user_id 对应可空整数中的缺失值，金额 7.50 可以参与加总。
