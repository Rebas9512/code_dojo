## 题目

给 events.team 建一个普通、非唯一的 B-tree 索引，名为 events_team_idx。保留数据，覆盖全部行。

## 示例

很多事件可以来自 team=2，因此索引不能限制 team 唯一。

样例库已执行下面的语句。

```sql
CREATE TABLE events (id integer,team integer,day date);
INSERT INTO events VALUES (1,2,'2025-01-01');
```

## 约束

沿用题目给定的英文表名和列名。
