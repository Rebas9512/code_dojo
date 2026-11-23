WITH ends AS (
    SELECT reader, topic, score,
           FIRST_VALUE(score) OVER (PARTITION BY reader, topic ORDER BY day, trial) AS first_score,
           ROW_NUMBER() OVER (PARTITION BY reader, topic ORDER BY day DESC, trial DESC) AS pos
    FROM proof_trials WHERE day IS NOT NULL
)
SELECT reader, topic, first_score, score AS last_score FROM ends
WHERE pos = 1 AND score > first_score ORDER BY reader, topic;
