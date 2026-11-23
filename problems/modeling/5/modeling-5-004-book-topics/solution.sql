CREATE TABLE links (book_id int REFERENCES books(id), topic_id int REFERENCES topics(id), PRIMARY KEY(book_id,topic_id));
INSERT INTO links SELECT DISTINCT book_id,topic_id FROM raw;
