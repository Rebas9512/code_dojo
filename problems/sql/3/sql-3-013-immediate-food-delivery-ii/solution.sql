WITH first_orders AS (
    SELECT buyer, MIN(placed) AS first_day FROM deliveries GROUP BY buyer
)
SELECT 100.0 * AVG(CASE WHEN d.wanted = d.placed THEN 1 ELSE 0 END) AS immediate_pct
FROM deliveries d JOIN first_orders f ON f.buyer = d.buyer AND f.first_day = d.placed;
