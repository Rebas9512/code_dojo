CREATE TABLE press_readings (slip integer, press text, day date, reading integer);
INSERT INTO press_readings VALUES
    (1, 'A', '2025-01-31', 8),
    (2, 'A', '2025-01-31', NULL),
    (3, 'A', '2025-02-01', 14),
    (4, 'B', '2025-01-31', 7),
    (5, 'A', NULL, 4);
