CREATE VIEW order_counts AS
SELECT user_id, COUNT(*) AS n FROM orders GROUP BY user_id;
