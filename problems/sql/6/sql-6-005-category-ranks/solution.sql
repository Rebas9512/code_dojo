SELECT order_month, category, SUM(line_amount) AS category_revenue,
       DENSE_RANK() OVER (
           PARTITION BY order_month
           ORDER BY SUM(line_amount) DESC
       ) AS sales_rank
FROM line_amounts
GROUP BY order_month, category
