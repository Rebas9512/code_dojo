SELECT c.issued, ROUND(1.0 * COUNT(DISTINCT t.card) / COUNT(DISTINCT c.card), 2) AS share
FROM card_issues c LEFT JOIN card_taps t ON t.card = c.card AND t.day = c.issued + 1
GROUP BY c.issued;
