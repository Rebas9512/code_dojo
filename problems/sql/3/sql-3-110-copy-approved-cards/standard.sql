INSERT INTO proof_archive (slip, sheets)
SELECT slip, sheets
FROM proof_queue
WHERE verdict = 'pass';
