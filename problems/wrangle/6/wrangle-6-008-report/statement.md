这一块是脚本和 notebook 共用的入口。骨架已提供 pandas（pd）、json、数据目录 DATA_DIR、UTC 截止日 CUTOFF、30 天的 WINDOW、列名列表 FEATURE_COLUMNS 和正向付款清洗函数 paid_orders。整跑会调用一次无参数的 main()。

```python
def main():
```

按下面的接口串起来。独立判这一题时，这些函数已由平台提供。先把最终表写到**当前工作目录**的 features.csv，带列名，省略行索引。最后一行用 JSON 对象打印四个数值：rows 为行数，columns_ok 为列名和顺序均与 FEATURE_COLUMNS 相同取 1，否则取 0；churn_rate 为 churned 的平均值，spend_30d 为全表 spend_30d 的总和。输入保证至少有一位合格读者。

```python
readers, events, payments = load_tables(DATA_DIR)
users = clean_readers(readers)
cleaned = clean_events(events, users)
sessions = sessionize(cleaned)
orders = paid_orders(payments)
activity = activity_features(sessions, CUTOFF)
purchases = purchase_features(orders, CUTOFF)
features = label_features(users, activity, purchases, orders, CUTOFF)
```

## 示例 1

若两位读者的标签是 0、1，近窗消费 25、0 元，列序正确，最后一行可以是 `{"rows":2,"columns_ok":1,"churn_rate":0.5,"spend_30d":25}`。

## 示例 2

若唯一读者过去和未来都没下单，CSV 有表头和一行数据，最后一行为 `{"rows":1,"columns_ok":1,"churn_rate":1,"spend_30d":0}`。
