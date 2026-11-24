CREATE VIEW daily_kpi AS
SELECT day, COUNT(DISTINCT member_id) AS buyers, SUM(amount) AS gross
FROM payments
GROUP BY day;
