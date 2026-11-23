## 题目

每个 id 取 rev 最大的行，同版本时取 event_id 最大的行。把胜者的 id、rev、tag 合入 catalog，其他目标行照旧。event_id 全局唯一。

## 示例

1 的 rev=3 有两条，事件 90 的标签胜过事件 30。

样例库已执行下面的语句。

```sql
CREATE TABLE catalog (id int PRIMARY KEY,rev int,tag text); INSERT INTO catalog VALUES (3,4,'keep');
CREATE TABLE feed (id int,rev int,tag text); INSERT INTO feed VALUES (1,3,'gold'),(1,1,'base'),(2,1,'plus');
ALTER TABLE feed ADD COLUMN event_id int; UPDATE feed SET event_id=10*rev+id; UPDATE feed SET event_id=30 WHERE id=1 AND rev=3; INSERT INTO feed VALUES (1,3,'blue',90);
```

## 约束

沿用题目给定的英文表名和列名。
