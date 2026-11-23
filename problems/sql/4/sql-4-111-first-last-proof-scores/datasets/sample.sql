CREATE TABLE proof_trials (trial integer, reader text, topic text, day date, score integer);
INSERT INTO proof_trials VALUES
    (1, 'A', 'ink', '2025-01-01', 4),
    (2, 'A', 'ink', '2025-02-01', 8),
    (3, 'A', 'wax', '2025-01-01', 9),
    (4, 'B', 'ink', '2025-01-01', 5),
    (5, 'B', 'ink', '2025-02-01', 5),
    (6, 'C', 'wax', '2025-01-01', NULL);
