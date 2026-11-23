## 题目

本步只关闭 changes 命中的当前版本，把 until_day 设为变更日、current_flag 设为 false。原有历史以及没有变更的会员照旧。

## 示例

1 的旧版本在 3 月 1 日结束，2 仍是当前版本。

样例库已执行下面的语句。

```sql
CREATE TABLE levels (id int, tier text, since date, until_day date, current_flag boolean, PRIMARY KEY(id,since));
INSERT INTO levels VALUES (1,'base','2025-01-01',NULL,true),(2,'base','2025-01-01',NULL,true);
CREATE TABLE changes (id int,tier text,day date); INSERT INTO changes VALUES (1,'gold','2025-03-01');
```

## 约束

沿用题目给定的英文表名和列名。
