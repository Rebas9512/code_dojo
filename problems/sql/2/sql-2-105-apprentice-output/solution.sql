SELECT a.badge FROM crew_yields a
JOIN crew_yields m ON m.badge = a.mentor
WHERE a.daily > m.daily;
