SELECT press, MIN(day) AS first_day
FROM press_checks
GROUP BY press;
