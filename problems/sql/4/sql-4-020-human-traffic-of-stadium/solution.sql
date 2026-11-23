WITH qualifying AS (
    SELECT id, day, visitors, id - ROW_NUMBER() OVER (ORDER BY id) AS block
    FROM gate_days WHERE visitors >= 100
), measured AS (
    SELECT id, day, visitors, COUNT(*) OVER (PARTITION BY block) AS length FROM qualifying
)
SELECT id, day, visitors FROM measured WHERE length >= 3 ORDER BY id;
