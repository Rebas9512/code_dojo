SELECT s.student_id, s.name, t.subject, COUNT(a.student_id) AS attended
FROM students s
CROSS JOIN subjects t
LEFT JOIN attendance a ON a.student_id = s.student_id AND a.subject = t.subject
GROUP BY s.student_id, s.name, t.subject
ORDER BY s.student_id, t.subject;
