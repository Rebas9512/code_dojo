SELECT desk FROM desk_tickets
GROUP BY desk ORDER BY COUNT(*) DESC, desk LIMIT 1;
