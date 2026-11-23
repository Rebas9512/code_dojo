SELECT press, ____ WITHIN GROUP (ORDER BY minutes) AS median_minutes
FROM bind_times GROUP BY press;
