UPDATE inventory
SET n = inventory.n + receipts.n
FROM receipts
WHERE receipts.id = inventory.id;
