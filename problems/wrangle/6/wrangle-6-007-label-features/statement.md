特征表每行代表截数时已经注册的一位读者。它将作为下一项目的训练输入。users 的列为 user_id、city、joined_on；activity、purchases 是前两项汇总；orders 是完整有效正向付款表。cutoff 为 UTC 零点。

```python
def label_features(users, activity, purchases, orders, cutoff):
```

选 joined_on 严格早于 cutoff 的读者，用 user_id 左连接两张汇总。signup_days 是注册日到 cutoff 的天数。缺少活跃或购买汇总的计数、金额、均额填 0；过去从未下单的 days_since_last_order 填 31，已有最近下单天数照录。只查 [cutoff, cutoff + 30 天) 的 orders：期间有单的读者 churned 为 0，否则为 1。窗口后的订单只参与标签。

按 user_id 升序返回骨架常量 `FEATURE_COLUMNS` 的 11 列：user_id, city, signup_days, sessions_30d, active_days_30d, events_30d, orders_30d, spend_30d, avg_basket, days_since_last_order, churned。city 是文本，其余为数值，所有格子都有值。

## 示例 1

读者 7 在 2 月 27 日注册，此前没有事件或订单，3 月 1 日零点恰好下单。以 3 月 1 日为 cutoff，signup_days=2、spend_30d=0、days_since_last_order=31、churned=0。

## 示例 2

若读者 8 仅在 3 月 31 日零点下单，3 月 1 日截数时他的标签为 1。3 月 1 日当天才注册的读者不进入本次人群。
