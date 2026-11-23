SELECT CASE WHEN seat % 2 = 0 THEN seat - 1
            WHEN seat < (SELECT MAX(seat) FROM seats) THEN seat + 1
            ELSE seat END AS new_seat, reader
FROM seats ORDER BY new_seat;
