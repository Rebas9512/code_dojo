UPDATE users SET city = NULL WHERE user_id IN (1, 2);
INSERT INTO users (user_id, name, email, phone, city, signup_date, referrer_id) VALUES
    (21, 'Tang Yu', 'tangyu@example.com', NULL, NULL, '2025-07-01', NULL);
