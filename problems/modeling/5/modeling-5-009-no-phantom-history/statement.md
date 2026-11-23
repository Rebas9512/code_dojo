## 题目

在每键一行的 changes 中识别真实的等级变化，只对新会员或等级不同的会员执行第二型历史载入。已有会员的生效日保证较新，等级都有值。

## 示例

会员 2 仍是 base 时，应保留原版本的 since，且只有一行。

样例库已执行下面的语句。

```sql
CREATE TABLE levels (id int, tier text, since date, until_day date, current_flag boolean, PRIMARY KEY(id,since));
INSERT INTO levels VALUES (1,'base','2025-01-01',NULL,true),(2,'base','2025-01-01',NULL,true);
CREATE TABLE changes (id int,tier text,day date); INSERT INTO changes VALUES (1,'gold','2025-03-01'); INSERT INTO changes VALUES (2,'base','2025-03-01');
```

## 约束

沿用题目给定的英文表名和列名。
