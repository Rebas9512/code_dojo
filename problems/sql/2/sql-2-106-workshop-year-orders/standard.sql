SELECT w.shop, w.opened, COUNT(o.ticket) AS tickets
FROM workshops w
LEFT JOIN print_orders o
  ON w.shop = o.shop
 AND o.placed >= DATE '2025-01-01' AND o.placed < DATE '2026-01-01'
GROUP BY w.shop, w.opened;
