SELECT c.issued, COUNT(DISTINCT c.card) AS issued_cards, COUNT(DISTINCT t.card) AS returned
FROM card_issues c
LEFT JOIN card_taps t ON t.card = c.card AND t.day = c.issued + 1
GROUP BY c.issued;
