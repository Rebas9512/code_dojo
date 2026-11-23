## 题目

创建普通视图 daily_kpi(day,buyers,gross)，按交易日统计付费会员数和支付总额。同日多次支付只计一名会员。

## 示例

4 月 1 日有两位会员付费，共 10.00。

样例库已执行下面的语句。

```sql
CREATE TABLE upgrades (member_id int,tier text,start_on date);
INSERT INTO upgrades VALUES (1,'base','2025-01-01'),(1,'gold','2025-04-01'),(2,'base','2025-01-01');
CREATE TABLE paylog (id int PRIMARY KEY,member_id int,day date,amount numeric(9,2));
INSERT INTO paylog VALUES (31,1,'2025-03-31',3.50),(32,1,'2025-04-01',8.00),(33,2,'2025-04-01',2.00);
CREATE TABLE tiers (member_id int,since date,tier text,until_day date, is_current boolean, PRIMARY KEY(member_id,since));
INSERT INTO tiers
SELECT member_id,start_on,tier,next_day,next_day IS NULL
FROM (SELECT u.*,LEAD(start_on) OVER (PARTITION BY member_id ORDER BY start_on) AS next_day FROM upgrades u) v;
CREATE TABLE payments (id int PRIMARY KEY,member_id int,day date,amount numeric(9,2));
INSERT INTO payments SELECT id,member_id,day,amount FROM paylog;
```

## 约束

沿用题目给定的英文表名和列名。
