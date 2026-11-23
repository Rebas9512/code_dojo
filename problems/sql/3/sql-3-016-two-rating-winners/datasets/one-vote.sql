DELETE FROM ratings WHERE (user_id, book_id) <> (SELECT user_id, book_id FROM ratings ORDER BY user_id, book_id LIMIT 1);
