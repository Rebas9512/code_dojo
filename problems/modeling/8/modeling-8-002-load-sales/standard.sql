CREATE VIEW valid_sales AS
SELECT batch_no, line_id, sold_on, customer_code, sku, qty
FROM warehouse_feed.sales
WHERE qty > 0;

INSERT INTO raw_sale (batch_no, line_id, sold_on, customer_code, sku, qty)
SELECT batch_no, line_id, sold_on, customer_code, sku, qty
FROM valid_sales
WHERE batch_no = 1;

SELECT line_id
FROM warehouse_feed.sales
WHERE batch_no = 1 AND (qty <= 0 OR qty IS NULL);
