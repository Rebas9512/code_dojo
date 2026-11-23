## 题目

已有 depots。创建 notes，按顺序放 id 整数主键、depot_id 可空整数外键，引用 depots.id。登记 (11,4)、(12,8)，然后删除编号 4 的父行。以后每次删除父行也要保留巡检记录并将引用清空。

## 示例

编号 8 的父行与编号 12 的子行都应保留。删除编号 4 时，要保留巡检记录并将引用清空。

样例库已执行下面的语句。

```sql
CREATE TABLE depots (id int PRIMARY KEY);
INSERT INTO depots VALUES (4),(8);
```

## 约束

沿用题目给定的英文表名和列名。
