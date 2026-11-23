## 题目

按此列序建库。depots(id 整数主键,city 文字)，parcels(id 整数主键,order_id 整数,depot_id 整数外键引用 depots.id,shipped_on 日期,units 整数)。除主键外列均可空。按仓库编号载入维度，每次发包保留一行事实。 源为 dispatch，parcel_id 是包裹号，一笔订单可多次发包。

## 示例

订单 80 的两次发包形成两条事实，二者引用同一个仓库。

样例库已执行下面的语句。

```sql
CREATE TABLE dispatch (parcel_id int PRIMARY KEY, order_id int, depot_id int, city text, shipped_on date, units int);
INSERT INTO dispatch VALUES
    (10,80,1,'York','2025-05-01',2),
    (11,80,1,'York','2025-05-01',3),
    (12,81,2,'Bath','2025-05-02',1);
```

## 约束

沿用题目给定的英文表名和列名。
