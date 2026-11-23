-- MySQL 原稿：n.day = DATE_ADD(p.day, INTERVAL 1 DAY)
-- 下面是可以运行的 PostgreSQL 译稿，请修正结果。
SELECT n.press, n.day FROM ink_checks n
JOIN ink_checks p ON n.press = p.press AND n.day = p.day - 1
WHERE n.shade > p.shade;
