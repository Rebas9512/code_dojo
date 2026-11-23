## 题目

建 slots，按顺序放 depot_id 整数和 day 日期。两列依次组成主键，depot_id 同时引用已有 depots。

## 示例

仓库 4 一天只能登记一行，仓库 8 可以登记相同日期。

样例库已执行下面的语句。

```sql
CREATE TABLE depots (id int PRIMARY KEY);
INSERT INTO depots VALUES (4),(8);
```

## 约束

沿用题目给定的英文表名和列名。
