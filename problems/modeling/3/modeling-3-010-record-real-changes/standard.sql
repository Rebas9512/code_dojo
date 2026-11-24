WITH changed AS (
    UPDATE prices p
    SET fee = r.fee
    FROM revisions r
    WHERE p.sku = r.sku AND p.fee <> r.fee
    RETURNING p.sku, p.fee
)
INSERT INTO audit (sku, fee)
SELECT sku, fee
FROM changed;
