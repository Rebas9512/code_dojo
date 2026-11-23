-- MySQL 原稿：GROUP_CONCAT(DISTINCT label ORDER BY label SEPARATOR '/')
-- 下面是可以运行的 PostgreSQL 译稿，请修正结果。
SELECT bin, STRING_AGG(label, '/' ORDER BY label) AS labels
FROM bin_labels GROUP BY bin;
