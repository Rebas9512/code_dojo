INSERT INTO arrivals (sku, qty)
SELECT sku, qty
FROM scans
WHERE qty > 0;
