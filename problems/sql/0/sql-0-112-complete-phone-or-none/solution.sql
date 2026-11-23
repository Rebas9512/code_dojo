SELECT name, COALESCE(phone, 'none') AS phone
FROM users;
