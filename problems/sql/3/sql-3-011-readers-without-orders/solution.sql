SELECT u.user_id, u.name FROM users u
WHERE NOT EXISTS (SELECT 1 FROM checkout_log c WHERE c.user_id = u.user_id);
