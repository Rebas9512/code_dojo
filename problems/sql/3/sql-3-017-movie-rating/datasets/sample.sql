CREATE TABLE readers (id int PRIMARY KEY, name text);
INSERT INTO readers VALUES
    (1, 'An'),
    (2, 'Bo');
CREATE TABLE films (id int PRIMARY KEY, title text);
INSERT INTO films VALUES
    (1, 'Ink'),
    (2, 'Fog');
CREATE TABLE votes (reader int, film int, stars int, rated date, PRIMARY KEY(reader, film));
INSERT INTO votes VALUES
    (1, 1, 5, '2020-02-29'),
    (1, 2, 1, '2020-01-31'),
    (2, 2, 4, '2020-02-01');
