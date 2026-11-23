SELECT order_id, coupon_code
FROM orders
WHERE coupon_code ~ '^NEW';
