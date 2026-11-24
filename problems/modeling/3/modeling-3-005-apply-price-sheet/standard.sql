UPDATE prices
SET fee = revisions.fee
FROM revisions
WHERE prices.sku = revisions.sku;
