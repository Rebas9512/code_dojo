SELECT author_id, COUNT(*) AS followers
FROM follows
GROUP BY author_id
ORDER BY author_id;
