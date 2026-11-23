WITH RECURSIVE branch AS (
    SELECT unit, 0 AS depth
    FROM archive_units
    WHERE unit = 11
    UNION ALL
    SELECT u.unit, b.depth + 1
    FROM archive_units u
    JOIN branch b ON u.parent = b.unit
)
SELECT unit, depth
FROM branch;
