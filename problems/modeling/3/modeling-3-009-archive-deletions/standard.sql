WITH removed AS (
    DELETE FROM queue
    USING cancelled
    WHERE queue.id = cancelled.id
    RETURNING queue.id, queue.task
)
INSERT INTO archive (id, task)
SELECT id, task
FROM removed;
