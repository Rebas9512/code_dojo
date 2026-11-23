SELECT customer
FROM receipts
GROUP BY customer
HAVING COUNT(DISTINCT sku) = (SELECT COUNT(*) FROM catalog);
