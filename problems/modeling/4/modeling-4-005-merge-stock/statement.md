## 题目

用 MERGE 将盘点快照 batch 合并到 stock。已在库的更新为盘点数，新的登记，无消息的保持原状。

## 示例

A 从 5 改为 7，C 新入库，B 保留。

样例库已执行下面的语句。

```sql
CREATE TABLE stock (sku text PRIMARY KEY,qty int); INSERT INTO stock VALUES ('A',5),('B',9);
CREATE TABLE batch (sku text,qty int); INSERT INTO batch VALUES ('A',7),('C',2);
```

## 约束

沿用题目给定的英文表名和列名。
