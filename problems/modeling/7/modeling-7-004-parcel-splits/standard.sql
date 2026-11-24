CREATE VIEW splits AS
SELECT order_id, COUNT(*) AS parcels_n
FROM parcels
GROUP BY order_id
HAVING COUNT(*) > 1;
