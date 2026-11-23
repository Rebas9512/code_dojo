WITH visits AS (
    SELECT player, day, MIN(day) OVER (PARTITION BY player) AS first_day
    FROM play_days
)
SELECT 1.0 * COUNT(*) FILTER (WHERE day = first_day + 1) / COUNT(DISTINCT player) AS fraction
FROM visits;
