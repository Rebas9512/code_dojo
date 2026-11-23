CREATE TABLE tiers (member_id int,since date,tier text,until_day date, is_current boolean, PRIMARY KEY(member_id,since));
INSERT INTO tiers
SELECT member_id,start_on,tier,next_day,next_day IS NULL
FROM (SELECT u.*,LEAD(start_on) OVER (PARTITION BY member_id ORDER BY start_on) AS next_day FROM upgrades u) v;
CREATE TABLE payments (id int PRIMARY KEY,member_id int,day date,amount numeric(9,2));
INSERT INTO payments SELECT id,member_id,day,amount FROM paylog;
CREATE VIEW tier_kpi AS
SELECT t.tier,COUNT(*) AS payments_n,SUM(p.amount) AS gross
FROM payments p JOIN tiers t ON p.member_id=t.member_id
 AND p.day>=t.since AND (t.until_day IS NULL OR p.day<t.until_day) GROUP BY t.tier;
CREATE VIEW daily_kpi AS
SELECT day,COUNT(DISTINCT member_id) AS buyers,SUM(amount) AS gross FROM payments GROUP BY day;
