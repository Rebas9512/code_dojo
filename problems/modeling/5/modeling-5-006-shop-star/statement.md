## 题目

每个 line_id 是一次销售明细。创建 shops(id 整数主键,city 文字) 和 sales(line_id 整数主键,shop_id 整数外键,units 整数)，按此列序。门店外键指向 shops.id。载入全部事实和维度，普通属性可空。

## 示例

门店 1 有两条各卖 2 件的明细，需要保留两行；城市只在门店维度保存。

样例库已执行下面的语句。

```sql
CREATE TABLE receipts (line_id int PRIMARY KEY, shop_id int, city text, units int);
INSERT INTO receipts VALUES (10,1,'York',2),(11,1,'York',2),(12,2,'Bath',5);
```

## 约束

沿用题目给定的英文表名和列名。
