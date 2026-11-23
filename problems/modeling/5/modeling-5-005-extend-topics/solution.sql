INSERT INTO links SELECT DISTINCT book_id,topic_id FROM raw ON CONFLICT(book_id,topic_id) DO NOTHING;
