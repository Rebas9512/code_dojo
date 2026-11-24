SELECT order_id, user_id, order_date,
       DATE_TRUNC('month', order_date)::date AS order_month
FROM orders
WHERE status <> 'cancelled'
  AND (coupon_code IS NULL OR coupon_code <> 'TEST')
