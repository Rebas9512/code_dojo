SELECT b.badge_id, s.name
FROM staff s
LEFT JOIN badges b ON b.staff_id = s.staff_id;
