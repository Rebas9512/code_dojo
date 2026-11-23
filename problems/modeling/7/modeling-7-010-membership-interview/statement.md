## 题目

按列序建 tiers(member_id 整数,since 日期,tier 文字,until_day 日期,is_current 布尔)，按 (member_id,since) 建主键，其他字段可空。在 upgrades 中每个会员的生效日唯一；载入每个版本，结束日等于该会员下一版本的起始日，最近版本结束日为空且 is_current 为真。

按列序建 payments(id 整数主键,member_id 整数,day 日期,amount numeric(9,2))，非主键列可空。从 paylog 原样载入每笔交易。

建立普通视图 tier_kpi(tier,payments_n,gross)，按交易当日的等级统计支付笔数和总金额。再建 daily_kpi(day,buyers,gross)，按日统计付费会员数（去重）和总金额。两张视图只列有支付记录的分组。

## 示例

会员 1 的两笔交易跨过升档日，应分别计入 base 和 gold。4 月 1 日支付总额 10.00。

样例库已执行下面的语句。

```sql
CREATE TABLE upgrades (member_id int,tier text,start_on date);
INSERT INTO upgrades VALUES (1,'base','2025-01-01'),(1,'gold','2025-04-01'),(2,'base','2025-01-01');
CREATE TABLE paylog (id int PRIMARY KEY,member_id int,day date,amount numeric(9,2));
INSERT INTO paylog VALUES (31,1,'2025-03-31',3.50),(32,1,'2025-04-01',8.00),(33,2,'2025-04-01',2.00);
```

## 约束

沿用题目给定的英文表名和列名。
