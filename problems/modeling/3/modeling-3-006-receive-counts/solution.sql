UPDATE inventory t SET n=t.n+s.n FROM receipts s WHERE s.id=t.id;
