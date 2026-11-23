DELETE FROM payments WHERE user_id IN (SELECT user_id FROM readers WHERE device='ios');
