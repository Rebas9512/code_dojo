WITH history AS (
    SELECT sku, price, ROW_NUMBER() OVER (PARTITION BY sku ORDER BY changed DESC) AS pos
    FROM price_changes
    WHERE changed <= DATE '2019-08-16'
), products AS (
    SELECT DISTINCT sku
    FROM price_changes
)
SELECT p.sku, COALESCE(h.price, 10) AS price
FROM products p
LEFT JOIN history h ON p.sku = h.sku AND h.pos = 1;
