SELECT p.press, COALESCE(SUM(f.fee), 0) AS fees
FROM presses p
LEFT JOIN job_fees f ON f.press = p.press
GROUP BY p.press;
