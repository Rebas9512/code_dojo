WITH history AS (
    SELECT maker, day, grade,
           LAG(grade) OVER (PARTITION BY maker ORDER BY day, review) AS previous,
           LAG(grade, 2) OVER (PARTITION BY maker ORDER BY day, review) AS oldest,
           ROW_NUMBER() OVER (PARTITION BY maker ORDER BY day DESC, review DESC) AS pos
    FROM craft_reviews WHERE day IS NOT NULL
)
SELECT maker, grade - oldest AS gain FROM history
WHERE pos = 1 AND grade > previous AND previous > oldest ORDER BY gain DESC, maker;
