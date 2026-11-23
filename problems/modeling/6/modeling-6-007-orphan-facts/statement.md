## 题目

返回 facts 中 depot_id 非空、却找不到对应 depots.id 的 event_id。一行一个事件。

## 示例

样例中只有事件 12 是孤儿。

```sql
CREATE TABLE depots (id int PRIMARY KEY); INSERT INTO depots VALUES (1);
CREATE TABLE facts (event_id int,depot_id int); INSERT INTO facts VALUES (10,1),(11,NULL),(12,9);
```

## 约束

列依题面顺序，结果行可按任意顺序。
