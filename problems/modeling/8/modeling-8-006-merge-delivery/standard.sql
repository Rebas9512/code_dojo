INSERT INTO raw_sale (batch_no, line_id, sold_on, customer_code, sku, qty)
SELECT batch_no, line_id, sold_on, customer_code, sku, qty
FROM valid_sales
WHERE batch_no = 2
ON CONFLICT (batch_no, line_id) DO NOTHING;

UPDATE dim_customer c
SET valid_to = incoming.valid_from
FROM warehouse_feed.customers incoming
WHERE incoming.batch_no = 2 AND incoming.customer_code = c.customer_code
  AND c.valid_to IS NULL AND c.tier <> incoming.tier;

INSERT INTO dim_customer (customer_code, tier, valid_from)
SELECT incoming.customer_code, incoming.tier, incoming.valid_from
FROM warehouse_feed.customers incoming
WHERE incoming.batch_no = 2 AND NOT EXISTS (
    SELECT 1
    FROM dim_customer c
    WHERE c.customer_code = incoming.customer_code AND c.valid_to IS NULL
);

INSERT INTO fact_sale (line_id, sold_on, customer_key, product_key, qty)
SELECT line_id, sold_on, customer_key, product_key, qty
FROM keyed_sale
WHERE batch_no = 2
ON CONFLICT (line_id) DO UPDATE
SET sold_on = EXCLUDED.sold_on,
    customer_key = EXCLUDED.customer_key,
    product_key = EXCLUDED.product_key,
    qty = EXCLUDED.qty;
