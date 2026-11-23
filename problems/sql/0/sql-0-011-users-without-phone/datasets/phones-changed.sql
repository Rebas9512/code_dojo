UPDATE users SET phone = NULL WHERE user_id IN (1, 3);
UPDATE users SET phone = '13500000002' WHERE user_id = 2;
INSERT INTO users (user_id, name, email, phone, city, signup_date, referrer_id) VALUES
    (21, 'Tang Yu', 'tangyu@example.com', NULL, 'Wuhan', '2025-07-01', NULL);
