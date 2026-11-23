DELETE FROM queue q USING cancelled c WHERE q.id=c.id;
