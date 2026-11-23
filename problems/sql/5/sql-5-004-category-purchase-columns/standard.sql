SELECT u.user_id,
       SUM(CASE WHEN p.category = 'fiction' THEN p.quantity ELSE 0 END) AS fiction,
       SUM(CASE WHEN p.category = 'scifi' THEN p.quantity ELSE 0 END) AS scifi,
       SUM(CASE WHEN p.category = 'kids' THEN p.quantity ELSE 0 END) AS kids
FROM users u
LEFT JOIN book_purchases p ON p.user_id = u.user_id
GROUP BY u.user_id;
