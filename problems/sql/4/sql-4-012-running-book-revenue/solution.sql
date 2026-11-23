SELECT day, amount, SUM(amount) OVER (ORDER BY day) AS total
FROM daily_sales ORDER BY day;
