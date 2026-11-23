## 题目

建 requests，按顺序放 id 整数主键、depot_id 可空整数。已填写的 depot_id 必须存在于 depots，尚未分配则留空。

## 示例

未分配和指向仓库 8 都可以，指向不存在的 99 不可以。

样例库已执行下面的语句。

```sql
CREATE TABLE depots (id int PRIMARY KEY);
INSERT INTO depots VALUES (4),(8);
```

## 约束

沿用题目给定的英文表名和列名。
