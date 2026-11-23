CREATE TABLE topics (id int PRIMARY KEY); INSERT INTO topics VALUES (1),(2);
CREATE TABLE books (id int PRIMARY KEY); INSERT INTO books VALUES (7),(9);
CREATE TABLE raw (book_id int,topic_id int); INSERT INTO raw VALUES (7,1),(7,2),(9,1),(7,1);
CREATE TABLE links (book_id int,topic_id int,PRIMARY KEY(book_id,topic_id)); INSERT INTO links VALUES (7,1);
