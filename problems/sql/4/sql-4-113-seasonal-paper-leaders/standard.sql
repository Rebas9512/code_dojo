WITH seasons AS (
    SELECT CASE WHEN month IN (12, 1, 2) THEN 'winter'
                WHEN month <= 5 THEN 'spring'
                WHEN month <= 8 THEN 'summer' ELSE 'fall' END AS season, paper, packs, price
    FROM paper_sales
), totals AS (
    SELECT season, paper, SUM(packs) AS packs, SUM(packs * price) AS revenue
    FROM seasons
    GROUP BY season, paper
), ranked AS (
    SELECT season, paper, packs, revenue,
           ROW_NUMBER() OVER (PARTITION BY season ORDER BY packs DESC, revenue DESC NULLS LAST, paper) AS pos
    FROM totals
)
SELECT season, paper, packs, revenue
FROM ranked
WHERE pos = 1
ORDER BY season;
