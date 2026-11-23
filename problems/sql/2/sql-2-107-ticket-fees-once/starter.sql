SELECT p.press, COALESCE(SUM(f.fee), 0) AS fees
FROM presses p LEFT JOIN job_fees f ON f.press = p.press
LEFT JOIN job_parts j ON j.job = f.job
GROUP BY p.press;
