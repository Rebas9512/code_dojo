SELECT s.name, b.amount
FROM staff s
LEFT JOIN bonuses b ON b.staff_id = s.staff_id
WHERE COALESCE(b.amount, 0) < 1000;
