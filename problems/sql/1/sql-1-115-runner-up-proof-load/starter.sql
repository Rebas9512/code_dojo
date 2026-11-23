-- MySQL 原稿：ORDER BY total DESC, bench LIMIT 2, 1
-- 下面是可以运行的 PostgreSQL 译稿，请修正结果。
SELECT bench, SUM(sheets) AS total FROM load_slips
GROUP BY bench ORDER BY total DESC, bench LIMIT 2 OFFSET 1;
