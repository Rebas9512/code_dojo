## 题目

创建普通视图 tier_kpi(tier,payments_n,gross)。按成交当天的等级统计支付笔数和总金额，只列有交易的等级。相同金额的两笔交易分别计入。

## 示例

样例 base 有两笔，金额之和 5.50；gold 有一笔，金额 8.00。

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
