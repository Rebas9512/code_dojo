-- MySQL 原稿：SELECT `rack`, SUM(sheets) AS total FROM sheet_lots GROUP BY rack
-- 下面是可以运行的 PostgreSQL 译稿，请修正结果。
SELECT 'rack', SUM(sheets) AS total FROM sheet_lots GROUP BY rack;
