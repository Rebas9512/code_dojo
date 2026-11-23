CREATE TABLE card_issues (card integer, issued date);
INSERT INTO card_issues VALUES
    (1, '2025-02-28'),
    (2, '2025-02-28'),
    (3, '2025-03-01');

CREATE TABLE card_taps (card integer, day date);
INSERT INTO card_taps VALUES
    (1, '2025-03-01'),
    (1, '2025-03-01'),
    (2, '2025-03-02'),
    (3, '2025-03-01');
