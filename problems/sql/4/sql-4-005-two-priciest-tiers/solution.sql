WITH ranked AS (
    SELECT book_id, category, price,
           DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) AS tier
    FROM shelf WHERE price IS NOT NULL
)
SELECT book_id, category, price FROM ranked WHERE tier <= 2;
