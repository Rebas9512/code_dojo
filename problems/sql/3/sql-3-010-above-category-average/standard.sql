SELECT b.book_id, b.category, b.price
FROM books b
WHERE b.price > (
    SELECT AVG(peer.price)
    FROM books peer
    WHERE peer.category = b.category
);
