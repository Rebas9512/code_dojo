CREATE TABLE purchase_log AS SELECT order_id, user_id, order_date AS day FROM orders;
