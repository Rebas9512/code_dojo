CREATE TABLE shelf AS SELECT book_id, category, price FROM books;
ALTER TABLE shelf ADD PRIMARY KEY (book_id);
