## 题目

建立普通视图 fee_summary(state,jobs_n,total_fee)，按状态返回笔数和费用之和。

## 示例

open 有 2 笔，总费用 3；done 有 1 笔，总费用 4。

样例库已执行下面的语句。

```sql
CREATE TABLE jobs (id int,state text,fee int); INSERT INTO jobs VALUES (1,'open',3),(2,'done',4),(3,'open',0);
```

## 约束

沿用题目给定的英文表名和列名。
