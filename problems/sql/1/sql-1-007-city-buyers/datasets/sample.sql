CREATE VIEW buyer_orders AS
SELECT u.city, o.user_id FROM orders o JOIN users u ON u.user_id = o.user_id;
