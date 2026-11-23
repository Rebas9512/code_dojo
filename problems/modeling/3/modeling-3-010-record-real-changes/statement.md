## 题目

应用同键调价；仅将价格确实变动的商品和新价格追加到 audit。不要为相等价格或未知商品记回执。

## 示例

B 的新价 22 被记录，A 的价格保持原值。

样例库已执行下面的语句。

```sql
CREATE TABLE prices (sku text PRIMARY KEY,fee int); INSERT INTO prices VALUES ('A',10),('B',20);
CREATE TABLE revisions (sku text PRIMARY KEY,fee int); INSERT INTO revisions VALUES ('B',22);
CREATE TABLE audit (sku text, fee int);
```

## 约束

沿用题目给定的英文表名和列名。
