CREATE TABLE supply_events (client text, day date, action text);
INSERT INTO supply_events VALUES
    ('A', '2025-01-01', 'buy'),
    ('A', '2025-01-04', 'buy'),
    ('A', '2025-01-31', 'buy'),
    ('B', '2025-01-01', 'buy'),
    ('B', '2025-01-03', 'buy'),
    ('B', '2025-02-02', 'buy'),
    ('B', '2025-02-03', 'refund');
