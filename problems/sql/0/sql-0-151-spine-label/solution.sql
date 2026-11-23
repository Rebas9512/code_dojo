SELECT book_id, UPPER(SUBSTRING(title FROM 1 FOR 3)) AS label
FROM books;
