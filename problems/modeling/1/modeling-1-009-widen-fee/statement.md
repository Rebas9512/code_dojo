## 题目

将 tariffs.fee 从整数改为 numeric(9,2)，其余结构与原数据照旧。

## 示例

原先的 14 应读作 14.00；此后可以精确保存两位小数。

样例库已执行下面的语句。

```sql
CREATE TABLE tariffs (code text, fee int);
INSERT INTO tariffs VALUES ('city',14);
```

## 约束

沿用题目给定的英文表名和列名。
