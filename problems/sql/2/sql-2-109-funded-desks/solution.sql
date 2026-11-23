SELECT b.given, SUM(c.coins) AS balance
FROM binders b JOIN credit_moves c ON c.badge = b.badge
GROUP BY b.badge, b.given HAVING SUM(c.coins) > 100;
