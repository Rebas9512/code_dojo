SELECT day, hall, COUNT(DISTINCT guest) AS guests, COUNT(DISTINCT agent) AS agents
FROM fair_notes GROUP BY day, hall;
