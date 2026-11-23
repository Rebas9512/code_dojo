SELECT p.quote FROM paper_quotes p
WHERE p.price = (SELECT MAX(q.price) FROM paper_quotes q WHERE ____);
