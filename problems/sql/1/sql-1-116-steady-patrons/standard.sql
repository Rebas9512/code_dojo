SELECT client
FROM supply_events
GROUP BY client
HAVING COUNT(*) FILTER (WHERE action = 'buy') >= 3
   AND MAX(day) - MIN(day) >= 30
   AND COUNT(*) FILTER (WHERE action = 'refund') * 5 < COUNT(*)
ORDER BY client;
