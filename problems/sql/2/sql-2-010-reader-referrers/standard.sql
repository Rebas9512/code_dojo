SELECT u.user_id, u.name, ref.name AS referrer_name
FROM users u
LEFT JOIN users ref ON ref.user_id = u.referrer_id;
