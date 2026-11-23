SELECT apprentice.badge
FROM crew_yields apprentice
JOIN crew_yields mentor ON mentor.badge = apprentice.mentor
WHERE apprentice.daily > mentor.daily;
