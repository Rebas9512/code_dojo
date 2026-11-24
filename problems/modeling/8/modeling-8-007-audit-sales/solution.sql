CREATE INDEX fact_customer_day_idx ON fact_sale (customer_key, sold_on);

CREATE VIEW sale_issues AS
SELECT r.batch_no, r.line_id, 'customer_gap' AS issue
FROM raw_sale r
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_customer c
    WHERE c.customer_code = r.customer_code AND c.valid_from <= r.sold_on
      AND (c.valid_to IS NULL OR r.sold_on < c.valid_to)
)
UNION ALL
SELECT r.batch_no, r.line_id, 'unknown_sku' AS issue
FROM raw_sale r
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_product p
    WHERE p.sku = r.sku
);
