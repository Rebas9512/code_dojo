INSERT INTO users (user_id, name, email, phone, city, signup_date, referrer_id) VALUES
    (21, 'Tang Yu', 'tangyu@example.com', NULL, 'Shanghai', '2025-07-01', NULL),
    (22, 'Ye Qing', 'yeqing@example.com', NULL, 'Beijing', '2025-07-02', NULL);
UPDATE users SET city = 'Hangzhou' WHERE user_id = 1;
