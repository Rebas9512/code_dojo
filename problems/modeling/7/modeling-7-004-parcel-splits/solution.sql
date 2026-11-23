CREATE VIEW splits AS
SELECT p.order_id,COUNT(*) AS parcels_n FROM parcels p GROUP BY p.order_id HAVING COUNT(*)>1;
