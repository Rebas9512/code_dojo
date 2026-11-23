CREATE TABLE archive_units (unit integer, parent integer, label text, budget integer);
INSERT INTO archive_units VALUES
    (10, NULL, 'Atrium', 20),
    (11, 10, 'Birch', 6),
    (12, 10, 'Cedar', 7),
    (13, 11, 'Dune', 9);
