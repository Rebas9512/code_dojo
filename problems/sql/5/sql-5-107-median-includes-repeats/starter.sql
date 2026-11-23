SELECT press, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY minutes) AS median_minutes
FROM (SELECT DISTINCT press, minutes FROM bind_times) AS observations GROUP BY press;
