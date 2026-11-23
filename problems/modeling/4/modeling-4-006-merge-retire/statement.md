## 题目

以 batch 为变更流，qty=0 表示停货，移除已有货号、忽略未知货号。正数表示设定最终库存，可能是新货号。

## 示例

A 停货后应消失，未知的 Z 发来停货消息也不入库。

样例库已执行下面的语句。

```sql
CREATE TABLE stock (sku text PRIMARY KEY,qty int); INSERT INTO stock VALUES ('A',5),('B',9);
CREATE TABLE batch (sku text,qty int); INSERT INTO batch VALUES ('A',0),('C',2); INSERT INTO batch VALUES ('Z',0);
```

## 约束

沿用题目给定的英文表名和列名。
