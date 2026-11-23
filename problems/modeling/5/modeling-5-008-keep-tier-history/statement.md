## 题目

处理 changes 中的真实升档，每键一条且生效日晚于原当前版本。先关闭原当前行，再插入新行。新区间从 day 起生效，结束日为空、当前标志为真。新会员直接建首行。

## 示例

会员 1 有 base 和 gold 两行，只有 gold 是当前行。

样例库已执行下面的语句。

```sql
CREATE TABLE levels (id int, tier text, since date, until_day date, current_flag boolean, PRIMARY KEY(id,since));
INSERT INTO levels VALUES (1,'base','2025-01-01',NULL,true),(2,'base','2025-01-01',NULL,true);
CREATE TABLE changes (id int,tier text,day date); INSERT INTO changes VALUES (1,'gold','2025-03-01');
```

## 约束

沿用题目给定的英文表名和列名。
