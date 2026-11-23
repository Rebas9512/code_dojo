CREATE TABLE delivery_notes (route text, promised date, actual date);
INSERT INTO delivery_notes VALUES
    ('E', '2025-02-28', '2025-02-26'),
    ('E', '2025-02-28', '2025-03-03'),
    ('W', '2025-03-01', '2025-03-01'),
    ('W', '2025-03-01', NULL);
