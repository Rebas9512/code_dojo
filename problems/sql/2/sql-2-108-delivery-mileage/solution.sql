SELECT b.given, COALESCE(SUM(r.km), 0) AS distance
FROM binders b LEFT JOIN route_lengths r ON r.badge = b.badge
GROUP BY b.badge, b.given ORDER BY distance DESC, b.given;
