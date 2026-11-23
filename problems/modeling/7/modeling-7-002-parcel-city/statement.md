## 题目

沿用已载入的履约模型。创建普通视图 city_kpi(city,orders_n,units_n)，统计每座发货城市的不重复订单数及发货件数，只列有发货的城市。

## 示例

York 中订单 80 虽然发了两包，仍是 1 单、5 件。

样例库已执行下面的语句。

```sql
CREATE TABLE dispatch (parcel_id int PRIMARY KEY, order_id int, depot_id int, city text, shipped_on date, units int);
INSERT INTO dispatch VALUES
    (10,80,1,'York','2025-05-01',2),
    (11,80,1,'York','2025-05-01',3),
    (12,81,2,'Bath','2025-05-02',1);
CREATE TABLE depots (id int PRIMARY KEY,city text);
CREATE TABLE parcels (id int PRIMARY KEY,order_id int,depot_id int REFERENCES depots(id),shipped_on date,units int);
INSERT INTO depots SELECT DISTINCT depot_id,city FROM dispatch;
INSERT INTO parcels SELECT parcel_id,order_id,depot_id,shipped_on,units FROM dispatch;
```

## 约束

沿用题目给定的英文表名和列名。
