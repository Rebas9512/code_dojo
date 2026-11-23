WITH removed AS (
    DELETE FROM queue q USING cancelled c WHERE q.id=c.id RETURNING q.id,q.task
)
INSERT INTO archive SELECT id,task FROM removed;
