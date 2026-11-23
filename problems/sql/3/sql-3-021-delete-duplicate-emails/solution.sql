SELECT p.id, p.email FROM address_book p
WHERE NOT EXISTS (
    SELECT 1 FROM address_book q WHERE q.email = p.email AND q.id < p.id
);
