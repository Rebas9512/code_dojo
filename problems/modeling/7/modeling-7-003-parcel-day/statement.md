## 题目

创建普通视图 day_kpi(shipped_on,parcels_n,orders_n)。按发货日统计包裹数和不同订单数，只列有发货的日期。一单跨两日发货时在两日分别计数。

## 示例

5 月 1 日有 2 包、1 单。

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
