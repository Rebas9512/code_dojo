SELECT id FROM staff
WHERE salary < 30000 AND manager_id IS NOT NULL
  AND manager_id NOT IN (SELECT id FROM staff);
