## 题目

将 receipts.n 加到 inventory 中同一仓位的现有余额。没有到货的仓位照旧，不新增仓位。

## 示例

2 号仓原有 5 件、到货 3 件，应有 8 件。

样例库已执行下面的语句。

```sql
CREATE TABLE inventory (id int PRIMARY KEY,n int); INSERT INTO inventory VALUES (1,7),(2,5);
CREATE TABLE receipts (id int PRIMARY KEY,n int); INSERT INTO receipts VALUES (2,3);
```

## 约束

沿用题目给定的英文表名和列名。
