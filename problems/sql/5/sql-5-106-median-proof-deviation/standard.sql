SELECT route, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY actual - promised) AS median_days
FROM delivery_notes
GROUP BY route;
