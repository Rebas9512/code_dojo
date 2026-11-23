SELECT COALESCE(SUM(p.new_value), 0) AS total_value
FROM policies p
WHERE (
    SELECT COUNT(*)
    FROM policies q
    WHERE q.old_value = p.old_value
) > 1
AND (
    SELECT COUNT(*)
    FROM policies q
    WHERE q.lat = p.lat AND q.lon = p.lon
) = 1;
