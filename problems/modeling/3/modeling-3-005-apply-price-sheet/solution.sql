UPDATE prices p SET fee=r.fee
FROM revisions r WHERE p.sku=r.sku;
