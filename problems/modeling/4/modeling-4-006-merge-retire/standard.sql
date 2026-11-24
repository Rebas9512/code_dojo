MERGE INTO stock
USING batch ON batch.sku = stock.sku
WHEN MATCHED AND batch.qty = 0 THEN DELETE
WHEN MATCHED THEN UPDATE SET qty = batch.qty
WHEN NOT MATCHED AND batch.qty > 0 THEN INSERT (sku, qty) VALUES (batch.sku, batch.qty);
