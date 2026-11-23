SELECT p.product_id,
       ROUND(COALESCE(SUM(p.price * s.units) / NULLIF(SUM(s.units), 0), 0), 2) AS mean_price
FROM prices p
LEFT JOIN unit_sales s ON s.product_id = p.product_id
                      AND s.sold_on BETWEEN p.first_day AND p.last_day
GROUP BY p.product_id;
