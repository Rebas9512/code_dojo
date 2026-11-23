WITH fans AS (
    SELECT r.name FROM readers r JOIN votes v ON v.reader = r.id
    GROUP BY r.id, r.name ORDER BY COUNT(*) DESC, r.name LIMIT 1
), best AS (
    SELECT f.title FROM films f JOIN votes v ON v.film = f.id
    WHERE v.rated >= DATE '2020-02-01' AND v.rated < DATE '2020-03-01'
    GROUP BY f.id, f.title ORDER BY AVG(v.stars) DESC, f.title LIMIT 1
), results AS (
    SELECT 1 AS pos, name AS winner FROM fans UNION ALL SELECT 2, title FROM best
)
SELECT winner FROM results ORDER BY pos;
