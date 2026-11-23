WITH neighbors AS (
    SELECT id, num, LAG(num) OVER (ORDER BY id) AS previous_num,
           LAG(num, 2) OVER (ORDER BY id) AS two_back,
           LAG(id, 2) OVER (ORDER BY id) AS first_id
    FROM journal
)
SELECT DISTINCT num
FROM neighbors
WHERE num = previous_num AND num = two_back AND id = first_id + 2;
