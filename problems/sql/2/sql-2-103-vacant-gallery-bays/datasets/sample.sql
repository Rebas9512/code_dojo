CREATE TABLE galleries (hall integer, label text);
INSERT INTO galleries VALUES
    (1, 'Cove'),
    (2, 'Arch'),
    (3, 'Bay'),
    (4, 'Glen');

CREATE TABLE exhibits (work integer, hall integer, memo text);
INSERT INTO exhibits VALUES
    (31, 1, NULL),
    (32, 3, 'set'),
    (33, 3, NULL);
