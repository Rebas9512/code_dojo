CREATE TABLE editions (edition integer, label text);
INSERT INTO editions VALUES
    (10, 'Arc'),
    (12, 'Cove'),
    (15, 'Pier'),
    (17, 'Loft');

CREATE TABLE dispatches (edition integer, day date);
INSERT INTO dispatches VALUES
    (10, '2025-03-01'),
    (10, '2025-05-31'),
    (12, '2025-05-01'),
    (12, '2025-06-01'),
    (15, '2025-01-01');
