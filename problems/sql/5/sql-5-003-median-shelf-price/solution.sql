SELECT category, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price
FROM price_survey GROUP BY category;
