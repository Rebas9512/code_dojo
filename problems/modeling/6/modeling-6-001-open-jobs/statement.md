## 题目

创建普通视图 open_jobs(id,fee)，读取 jobs 中 state 为 open 的全部工单。保留费用为零的工单。

## 示例

样例结果有 (1,3)、(3,0)。

样例库已执行下面的语句。

```sql
CREATE TABLE jobs (id int,state text,fee int); INSERT INTO jobs VALUES (1,'open',3),(2,'done',4),(3,'open',0);
```

## 约束

沿用题目给定的英文表名和列名。
