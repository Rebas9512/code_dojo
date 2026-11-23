SELECT press, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY minutes) AS median_minutes
FROM bind_times GROUP BY press;
