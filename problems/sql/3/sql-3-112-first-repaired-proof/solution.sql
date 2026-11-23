WITH failed AS (
    SELECT plate, MIN(day) AS first_bad FROM plate_tests WHERE verdict = 'bad' GROUP BY plate
), repaired AS (
    SELECT f.plate, f.first_bad,
           (SELECT MIN(t.day) FROM plate_tests t
            WHERE t.plate = f.plate AND t.verdict = 'ok' AND t.day > f.first_bad) AS first_ok
    FROM failed f
)
SELECT plate, first_ok - first_bad AS days FROM repaired
WHERE first_ok IS NOT NULL ORDER BY days, plate;
