CREATE TABLE staff (id int PRIMARY KEY, manager_id int, salary int);
INSERT INTO staff VALUES
    (1, NULL, 90000),
    (2, 1, 22000),
    (3, 8, 25000),
    (4, 9, 30000);
