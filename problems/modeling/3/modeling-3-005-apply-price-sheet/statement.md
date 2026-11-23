## 题目

用 revisions 的同键新价格更新 prices。调价单中找不到的商品保持旧价，尚未上架的商品暂不新增。

## 示例

A 保持 10，B 改为 22。

样例库已执行下面的语句。

```sql
CREATE TABLE prices (sku text PRIMARY KEY,fee int); INSERT INTO prices VALUES ('A',10),('B',20);
CREATE TABLE revisions (sku text PRIMARY KEY,fee int); INSERT INTO revisions VALUES ('B',22);
```

## 约束

沿用题目给定的英文表名和列名。
