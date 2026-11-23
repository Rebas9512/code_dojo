WITH missing_fees AS (
    SELECT badge FROM press_badges EXCEPT SELECT badge FROM fee_cards
), missing_badges AS (
    SELECT badge FROM press_badges EXCEPT SELECT badge FROM fee_cards
)
SELECT badge FROM missing_fees UNION SELECT badge FROM missing_badges ORDER BY badge;
