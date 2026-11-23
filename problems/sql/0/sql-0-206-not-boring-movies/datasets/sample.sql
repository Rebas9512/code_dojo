CREATE TABLE cinema (
    id integer PRIMARY KEY,
    movie text NOT NULL,
    description text NOT NULL,
    rating numeric(4,2) NOT NULL
);

INSERT INTO cinema VALUES
    (7, '灯塔', 'gentle', 7.6),
    (2, '长街', 'vivid', 9.8),
    (11, '泊岸', 'boring', 9.3),
    (5, '纸船', 'fun', 8.4);
