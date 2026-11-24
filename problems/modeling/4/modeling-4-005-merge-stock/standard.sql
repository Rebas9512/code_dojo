MERGE INTO stock
USING batch ON batch.sku = stock.sku
WHEN MATCHED THEN UPDATE SET qty = batch.qty
WHEN NOT MATCHED THEN INSERT (sku, qty) VALUES (batch.sku, batch.qty);
