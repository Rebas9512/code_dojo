DELETE FROM queue
USING cancelled
WHERE queue.id = cancelled.id;
