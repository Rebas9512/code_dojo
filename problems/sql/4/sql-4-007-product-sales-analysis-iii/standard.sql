WITH ranked AS (
    SELECT product, yr, qty, price, RANK() OVER (PARTITION BY product ORDER BY yr) AS place
    FROM sales
    WHERE yr IS NOT NULL
)
SELECT product, yr, qty, price
FROM ranked
WHERE place = 1;
