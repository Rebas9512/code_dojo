SELECT name, COALESCE(city, 'unknown') AS city
FROM users;
