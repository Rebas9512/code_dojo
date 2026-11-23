SELECT p.product_id,
       COALESCE(ROUND(SUM(p.price * s.units) / SUM(s.units), 2), 0) AS mean_price
FROM prices p
LEFT JOIN unit_sales s ON s.product_id = p.product_id
                      AND s.sold_on BETWEEN p.first_day AND p.last_day
GROUP BY p.product_id;
