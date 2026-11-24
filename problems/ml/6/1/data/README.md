# 书店 App 用户特征表

`features.csv` 是数据处理线「书店 App 用户特征表」完整参考脚本的输出。每位读者有一行，共 1,720 行，列顺序沿用上游。要重建这份 CSV，在数据处理项目页导出完整的 `features.py` 并解压它的数据包，让 `data/` 与脚本并列，在该目录运行下列命令。将生成的 `features.csv` 复制到机器学习项目的 `data/` 下。[上游项目与原始数据说明](../../../../wrangle/6/1/data/README.md)

```bash
python features.py
```

| 列 | 含义 |
| --- | --- |
| user_id、city | 读者编号和清洗后的城市。编号仅标识读者。 |
| signup_days | 截止时距注册的天数。 |
| sessions_30d、active_days_30d、events_30d | 观察窗口内的会话数、活跃天数和事件数。 |
| orders_30d、spend_30d、avg_basket | 观察窗口内的有效订单数、消费总额和平均每单金额。 |
| days_since_last_order | 距截止前最后一次有效付款的天数；从未下单取 31。 |
| churned | 从 2025-03-01 00:00 UTC 起的 30 天内没有有效付款记 1，有付款记 0。 |

观察窗口为截止时刻前的 30 天。标签取自随后的 30 天。803 人流失，917 人有后续付款。

## 来源与许可

书店 App 来自本仓库的虚构练习库 `readerapp`。上游用固定种子扩充样本后清洗、聚合；本文件是该合成教学数据的派生表。随仓库以 MIT 许可提供。[原始练习库](../../../../analytics/_db/readerapp/seed.sql) · [仓库许可声明](../../../../../README.md#license)
