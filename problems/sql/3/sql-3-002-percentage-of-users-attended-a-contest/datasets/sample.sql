CREATE TABLE members (reader_id int PRIMARY KEY);
INSERT INTO members VALUES
    (1),
    (2),
    (3),
    (4);
CREATE TABLE signups (event_id int, reader_id int, PRIMARY KEY(event_id, reader_id));
INSERT INTO signups VALUES
    (8, 1),
    (8, 2),
    (3, 4);
