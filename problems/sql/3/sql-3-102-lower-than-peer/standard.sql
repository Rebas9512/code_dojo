SELECT quote, peer_avg
FROM (
    SELECT p.quote, p.price, (
        SELECT AVG(peer.price)
        FROM paper_quotes peer
        WHERE peer.grade = p.grade AND peer.quote <> p.quote
    ) AS peer_avg
    FROM paper_quotes p
) AS compared
WHERE price < peer_avg;
