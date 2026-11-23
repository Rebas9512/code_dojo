SELECT title, publisher
FROM books
WHERE publisher <> 'Harbor Press' OR publisher IS NULL;
