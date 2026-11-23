WITH RECURSIVE chain AS (
    SELECT unit, parent, 0 AS distance
    FROM archive_units
    WHERE unit = 13
    UNION ALL
    SELECT u.unit, u.parent, c.distance + 1
    FROM archive_units u
    JOIN chain c ON u.unit = c.parent
)
SELECT unit, distance
FROM chain
WHERE distance > 0;
