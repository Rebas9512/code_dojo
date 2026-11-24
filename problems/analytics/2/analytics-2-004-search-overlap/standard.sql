SELECT COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'search') AS search_users,
       COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'view') AS view_users
FROM events e;
