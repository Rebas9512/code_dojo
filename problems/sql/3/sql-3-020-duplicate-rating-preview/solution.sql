DELETE FROM address_book p
WHERE EXISTS (
    SELECT 1 FROM address_book q
    WHERE q.email = p.email AND q.id < p.id
);
