SELECT user_id, order_id,
       day - ____ OVER (PARTITION BY user_id ORDER BY day NULLS LAST, order_id) AS days_since
FROM purchase_log;
