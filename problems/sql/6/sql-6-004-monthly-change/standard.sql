SELECT cur.order_month, cur.order_count, cur.revenue,
       ROUND(100 * (cur.revenue - prev.revenue) / NULLIF(prev.revenue, 0), 2) AS growth_pct
FROM monthly_sales AS cur
LEFT JOIN monthly_sales AS prev ON prev.order_month = cur.order_month - INTERVAL '1 month'
