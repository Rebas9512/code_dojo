WITH history AS (
    SELECT maker, grade,
           LAG(grade) OVER (PARTITION BY maker ORDER BY day, review) AS previous,
           LAG(grade, 2) OVER (PARTITION BY maker ORDER BY day, review) AS two_back,
           LEAD(day) OVER (PARTITION BY maker ORDER BY day, review) AS next_day
    FROM craft_reviews
    WHERE day IS NOT NULL
)
SELECT maker, grade - two_back AS gain
FROM history
WHERE next_day IS NULL AND grade > previous AND previous > two_back
ORDER BY gain DESC, maker;
