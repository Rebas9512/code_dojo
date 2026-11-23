## 题目

按 depot 分组，把 scans 中每个仓的件数之和追加到 daily(depot,units)，保留以前的日报。

## 示例

east 有两笔 3 和 2，应新增一行 east、5。

样例库已执行下面的语句。

```sql
CREATE TABLE scans (depot text, qty int); INSERT INTO scans VALUES ('east',3),('east',2),('west',4);
CREATE TABLE daily (depot text, units int);
```

## 约束

沿用题目给定的英文表名和列名。
