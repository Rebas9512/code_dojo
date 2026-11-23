SELECT v.reader_id, COUNT(*) AS unpaid_visits
FROM visits v
LEFT JOIN bills b ON b.visit_id = v.visit_id
WHERE b.bill_id IS NULL
GROUP BY v.reader_id;
