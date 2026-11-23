SELECT p.label, SUM(r.units) AS units
FROM products p
JOIN requests r ON r.product_id = p.product_id
WHERE r.ordered_on BETWEEN '2025-04-01' AND '2025-04-30'
GROUP BY p.product_id, p.label
HAVING SUM(r.units) >= 100;
