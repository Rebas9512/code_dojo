CREATE TABLE authors (
    id int PRIMARY KEY,
    name text
);

CREATE TABLE notes (
    id int PRIMARY KEY,
    author_id int REFERENCES authors(id)
);

INSERT INTO authors (id, name)
SELECT DISTINCT author_id, name
FROM raw;

INSERT INTO notes (id, author_id)
SELECT note_id, author_id
FROM raw;
