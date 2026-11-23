WITH RECURSIVE paths AS (
    SELECT unit AS ancestor, unit AS descendant
    FROM archive_units
    UNION ALL
    SELECT p.ancestor, u.unit
    FROM paths p
    JOIN archive_units u ON u.parent = p.descendant
), levels AS (
    SELECT descendant, COUNT(*) AS level
    FROM paths
    GROUP BY descendant
)
SELECT a.label, l.level, COUNT(*) - 1 AS reports, SUM(d.budget) AS funds
FROM paths p
JOIN archive_units a ON a.unit = p.ancestor
JOIN archive_units d ON d.unit = p.descendant
JOIN levels l ON l.descendant = a.unit
GROUP BY a.unit, a.label, l.level
ORDER BY l.level, funds DESC, a.label;
