DELETE FROM payments WHERE user_id IN (SELECT user_id FROM assignments WHERE experiment='cover' AND arm='A');
