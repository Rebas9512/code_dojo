CREATE TABLE policies (id int PRIMARY KEY, old_value numeric(8, 2), new_value numeric(8, 2), lat int, lon int);
INSERT INTO policies VALUES
    (1, 20, 12.25, 1, 2),
    (2, 20, 30.30, 1, 3),
    (3, 40, 19, 2, 3),
    (4, 20, 18, 2, 3);
