-- 本周刚注册的读者没有活动，也没有已满七天的实验组。
TRUNCATE readers CASCADE;
INSERT INTO readers VALUES (201, '2025-03-15', 'organic', 'Lima', 'ios');
INSERT INTO assignments VALUES (201, 'cover', 201, 'B', '2025-03-15 08:00');
