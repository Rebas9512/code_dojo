WITH flags AS (
    SELECT user_id, MIN(logged_at)::date AS first_day,
           COUNT(*) FILTER (WHERE logged_at >= DATE '2025-03-01' - INTERVAL '1 month'
                              AND logged_at < DATE '2025-03-01') AS prev_n,
           COUNT(*) FILTER (WHERE logged_at >= DATE '2025-03-01') AS now_n
    FROM logins WHERE logged_at < DATE '2025-03-01' + INTERVAL '1 month' GROUP BY user_id
), ledger AS (
    SELECT user_id, CASE WHEN now_n=0 THEN 'lost' WHEN prev_n>0 THEN 'retained'
                         WHEN first_day >= DATE '2025-03-01' THEN 'new' ELSE 'reactivated' END AS status
    FROM flags WHERE prev_n>0 OR now_n>0
)
SELECT channel, COUNT(*) FILTER (WHERE status IN ('new','reactivated')) - COUNT(*) FILTER (WHERE status='lost') AS net
FROM ledger JOIN readers USING (user_id) GROUP BY channel ORDER BY channel;
