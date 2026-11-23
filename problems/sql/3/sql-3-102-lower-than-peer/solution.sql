SELECT quote, peer_avg FROM (
    SELECT p.quote, p.price,
           (SELECT AVG(q.price) FROM paper_quotes q
            WHERE q.grade = p.grade AND q.quote <> p.quote) AS peer_avg
    FROM paper_quotes p
) AS compared WHERE price < peer_avg;
