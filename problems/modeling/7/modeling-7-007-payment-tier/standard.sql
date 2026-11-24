CREATE VIEW assigned AS
SELECT p.id, t.tier, p.amount
FROM payments p
JOIN tiers t
    ON t.member_id = p.member_id
   AND p.day >= t.since
   AND (t.until_day IS NULL OR p.day < t.until_day);
