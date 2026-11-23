WITH RECURSIVE paths AS (
    SELECT unit AS ancestor, unit AS child, 0 AS distance FROM archive_units
    UNION ALL
    SELECT p.ancestor, u.unit, p.distance + 1
    FROM paths p JOIN archive_units u ON u.parent = p.child
), levels AS (
    SELECT child, MAX(distance) + 1 AS level FROM paths GROUP BY child
)
SELECT a.label, l.level, COUNT(*) - 1 AS reports, SUM(u.budget) AS funds
FROM paths p JOIN archive_units a ON a.unit = p.ancestor
JOIN archive_units u ON u.unit = p.child JOIN levels l ON l.child = a.unit
GROUP BY a.unit, a.label, l.level ORDER BY l.level, funds DESC, a.label;
