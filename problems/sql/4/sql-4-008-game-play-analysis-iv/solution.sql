WITH visits AS (
    SELECT player, day, MIN(day) OVER (PARTITION BY player) AS first_day FROM play_days
)
SELECT 1.0 * COUNT(CASE WHEN day = first_day + 1 THEN 1 END) / COUNT(DISTINCT player) AS fraction
FROM visits;
