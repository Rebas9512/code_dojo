INSERT INTO upgrades VALUES (1,'plus','2025-05-01'),(3,'base','2025-02-01');
INSERT INTO paylog VALUES (34,3,'2025-04-02',4.50),(35,1,'2025-05-01',1.25),(36,1,'2025-05-01',1.25);
TRUNCATE tiers,payments;
INSERT INTO tiers
SELECT member_id,start_on,tier,next_day,next_day IS NULL
FROM (SELECT u.*,LEAD(start_on) OVER (PARTITION BY member_id ORDER BY start_on) AS next_day FROM upgrades u) v;
INSERT INTO payments SELECT id,member_id,day,amount FROM paylog;
