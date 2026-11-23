WITH sampled AS (
    SELECT visitor, MIN(tick) AS started FROM demo_steps WHERE action = 'sample' GROUP BY visitor
), reserved AS (
    SELECT s.visitor, MIN(e.tick) AS booked FROM sampled s
    JOIN demo_steps e ON e.visitor = s.visitor AND e.tick > s.started
    WHERE e.action = 'reserve' GROUP BY s.visitor
), paid AS (
    SELECT DISTINCT r.visitor FROM reserved r
    JOIN demo_steps e ON e.visitor = r.visitor AND e.tick > r.booked WHERE e.action = 'pay'
)
SELECT (SELECT COUNT(*) FROM sampled) AS sampled,
       (SELECT COUNT(*) FROM reserved) AS reserved,
       (SELECT COUNT(*) FROM paid) AS paid;
