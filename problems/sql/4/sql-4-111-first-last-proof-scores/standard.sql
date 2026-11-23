WITH endpoints AS (
    SELECT reader, topic, score AS last_score,
           FIRST_VALUE(score) OVER (PARTITION BY reader, topic ORDER BY day, trial) AS first_score,
           LEAD(day) OVER (PARTITION BY reader, topic ORDER BY day, trial) AS next_day
    FROM proof_trials
    WHERE day IS NOT NULL
)
SELECT reader, topic, first_score, last_score
FROM endpoints
WHERE next_day IS NULL AND last_score > first_score
ORDER BY reader, topic;
