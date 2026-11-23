SELECT p.quote
FROM paper_quotes p
WHERE p.price = (
    SELECT MAX(peer.price)
    FROM paper_quotes peer
    WHERE peer.grade = p.grade
);
