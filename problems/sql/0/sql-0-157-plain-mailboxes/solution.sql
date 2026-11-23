SELECT user_id, email
FROM users
WHERE email ~ '^[a-z][a-z]*@example[.]com$';
