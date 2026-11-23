CREATE TABLE plate_tests (plate text, day date, verdict text);
INSERT INTO plate_tests VALUES
    ('Arc', '2025-02-25', 'ok'),
    ('Arc', '2025-02-28', 'bad'),
    ('Arc', '2025-03-01', 'bad'),
    ('Arc', '2025-03-02', 'ok'),
    ('Bay', '2025-03-03', 'bad');
