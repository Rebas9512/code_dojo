INSERT INTO links (book_id, topic_id)
SELECT book_id, topic_id
FROM raw
ON CONFLICT (book_id, topic_id) DO NOTHING;
