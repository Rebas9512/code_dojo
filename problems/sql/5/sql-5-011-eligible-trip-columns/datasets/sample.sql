CREATE TABLE accounts (id int PRIMARY KEY, blocked boolean);
INSERT INTO accounts VALUES
    (1, false),
    (2, true),
    (3, false),
    (4, false);
CREATE TABLE trips (trip int PRIMARY KEY, day date, rider int, driver int, status text);
INSERT INTO trips VALUES
    (11, '2025-04-01', 1, 3, 'done'),
    (12, '2025-04-01', 1, 4, 'rider_cancel'),
    (13, '2025-04-01', 2, 4, 'driver_cancel'),
    (14, '2025-04-02', 3, 1, 'driver_cancel');
