WITH trials AS (
    SELECT reader, MIN(day) AS start_day
    FROM reading_log
    WHERE action = 'trial'
    GROUP BY reader
), paid AS (
    SELECT t.reader, MIN(e.day) AS paid_day
    FROM trials t
    JOIN reading_log e ON e.reader = t.reader
    WHERE e.action = 'pay' AND e.day BETWEEN t.start_day + 1 AND t.start_day + 7
    GROUP BY t.reader
), renewed AS (
    SELECT DISTINCT p.reader
    FROM paid p
    JOIN reading_log e ON e.reader = p.reader
    WHERE e.action = 'renew' AND e.day > p.paid_day
)
SELECT t.start_day, COUNT(*) AS trials, COUNT(p.reader) AS paid, COUNT(r.reader) AS renewed
FROM trials t
LEFT JOIN paid p ON p.reader = t.reader
LEFT JOIN renewed r ON r.reader = t.reader
GROUP BY t.start_day;
