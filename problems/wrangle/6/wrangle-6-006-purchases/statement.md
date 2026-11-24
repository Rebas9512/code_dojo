购买特征描述截止日到来前的消费水平。`orders` 是骨架的 `paid_orders(payments)` 返回的有效正向付款表，已剔除缺字段、重复付款编号和退款；每行是一单。列为 payment_id、user_id、paid_at、amount。cutoff 是 UTC 零点。

```python
def purchase_features(orders, cutoff):
```

每个在 cutoff 前买过书的人一行，按 user_id 升序。返回 user_id、days_since_last_order、orders_30d、spend_30d、avg_basket。距上次下单按 **UTC 日期之差** 计算，查全部截止前历史。后三项只取 [cutoff − 30 天, cutoff) 的单数、金额之和、每单平均金额。只有旧单时后三项均为 0；从未买过或只有未来订单的人留到合表时处理。金额保留计算精度。

## 示例 1

3 月 1 日截数，一位读者 2 月 28 日 23:59 付了 9 元，2 月 10 日付了 15 元。返回的四个值是 1、2、24、12。

## 示例 2

若最后一单在 1 月 1 日，3 月 1 日截数时仍保留该人，四个值是 59、0、0、0。
