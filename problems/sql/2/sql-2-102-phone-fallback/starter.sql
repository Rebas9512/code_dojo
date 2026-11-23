-- MySQL 原稿：IFNULL(e.dial, 'unrouted')
-- 下面是可以运行的 PostgreSQL 译稿，请修正结果。
SELECT b.badge, COALESCE('unrouted', e.dial) AS dial
FROM binders b LEFT JOIN extensions e ON e.badge = b.badge;
