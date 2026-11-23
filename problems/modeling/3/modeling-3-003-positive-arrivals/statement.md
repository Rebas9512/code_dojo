## 题目

从 scans 追加所有 qty 严格大于零的行到 arrivals，保留重复扫描的次数和目标已有记录。

## 示例

样例只新增 A 的 3 件。

样例库已执行下面的语句。

```sql
CREATE TABLE scans (sku text, qty int);
INSERT INTO scans VALUES ('A',3),('B',0),('C',-2);
CREATE TABLE arrivals (sku text, qty int);
```

## 约束

沿用题目给定的英文表名和列名。
