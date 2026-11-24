CREATE VIEW tier_kpi AS
SELECT t.tier, COUNT(*) AS payments_n, SUM(p.amount) AS gross
FROM payments p
JOIN tiers t
    ON t.member_id = p.member_id
   AND p.day >= t.since
   AND (t.until_day IS NULL OR p.day < t.until_day)
GROUP BY t.tier;
