SELECT tutor_id, COUNT(DISTINCT subject_id) AS subjects
FROM teaching
GROUP BY tutor_id;
