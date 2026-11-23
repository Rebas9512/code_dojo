SELECT visited_on, COUNT(DISTINCT reader_id) AS active_readers
FROM visits
WHERE visited_on BETWEEN '2025-06-01' AND '2025-06-30'
GROUP BY visited_on;
