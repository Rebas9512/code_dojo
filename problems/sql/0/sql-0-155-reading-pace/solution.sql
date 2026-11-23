SELECT book_id, ROUND(CAST(pages AS numeric) / 7, 2) AS pages_per_day
FROM books;
