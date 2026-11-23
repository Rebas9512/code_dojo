CREATE TABLE views (
    article_id integer NOT NULL,
    author_id integer NOT NULL,
    viewer_id integer NOT NULL,
    view_date date NOT NULL
);

INSERT INTO views VALUES
    (31, 8, 8, '2026-03-06'),
    (12, 3, 8, '2026-03-05'),
    (40, 2, 2, '2026-03-08'),
    (31, 8, 8, '2026-03-06');
