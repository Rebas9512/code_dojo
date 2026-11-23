WITH boarding AS (
    SELECT turn, rider, SUM(weight) OVER (ORDER BY turn) AS load FROM lineup
)
SELECT rider FROM boarding WHERE load <= 1000 ORDER BY turn DESC LIMIT 1;
