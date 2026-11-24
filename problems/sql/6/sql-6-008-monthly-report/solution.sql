SELECT m.order_month, m.order_count, m.revenue, m.growth_pct,
       (SELECT STRING_AGG(c.category, ', ' ORDER BY c.category)
        FROM category_ranks AS c
        WHERE c.order_month = m.order_month AND c.sales_rank = 1) AS top_categories,
       (SELECT MAX(a.author_revenue)
        FROM author_sales AS a
        WHERE a.order_month = m.order_month) AS top_author_revenue,
       COALESCE(r.repeat_count, 0) AS repeat_count
FROM monthly_change AS m
LEFT JOIN repeat_buyers AS r ON r.order_month = m.order_month
ORDER BY m.order_month;
