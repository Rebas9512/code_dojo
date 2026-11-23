CREATE TABLE reading_log (reader int, action text, day date);
INSERT INTO reading_log VALUES
    (1, 'trial', '2025-01-29'),
    (1, 'pay', '2025-02-05'),
    (1, 'renew', '2025-02-10'),
    (2, 'trial', '2025-01-29'),
    (2, 'pay', '2025-02-06'),
    (3, 'pay', '2025-03-01'),
    (3, 'trial', '2025-03-02'),
    (3, 'renew', '2025-03-04');
