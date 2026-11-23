SELECT day, amount, SUM(amount) ____ AS total
FROM daily_sales ORDER BY day;
