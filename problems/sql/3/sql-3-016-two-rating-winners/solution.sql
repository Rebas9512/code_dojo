WITH people AS (
    SELECT u.name FROM users u JOIN ratings r ON r.user_id = u.user_id
    GROUP BY u.user_id, u.name ORDER BY COUNT(*) DESC, u.name, u.user_id LIMIT 1
), titles AS (
    SELECT b.title FROM books b JOIN ratings r ON r.book_id = b.book_id
    GROUP BY b.book_id, b.title ORDER BY AVG(stars) DESC, b.title, b.book_id LIMIT 1
), winners AS (
    SELECT 1 AS pos, name AS winner FROM people
    UNION ALL
    SELECT 2 AS pos, title AS winner FROM titles
)
SELECT winner FROM winners ORDER BY pos;
