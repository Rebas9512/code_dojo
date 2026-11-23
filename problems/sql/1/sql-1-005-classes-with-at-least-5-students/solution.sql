SELECT class_name
FROM enrolments
GROUP BY class_name
HAVING COUNT(*) >= 5;
