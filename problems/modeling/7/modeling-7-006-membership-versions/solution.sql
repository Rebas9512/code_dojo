CREATE TABLE tiers (member_id int,since date,tier text,until_day date, is_current boolean, PRIMARY KEY(member_id,since));
INSERT INTO tiers
SELECT member_id,start_on,tier,next_day,next_day IS NULL
FROM (SELECT u.*,LEAD(start_on) OVER (PARTITION BY member_id ORDER BY start_on) AS next_day FROM upgrades u) v;
