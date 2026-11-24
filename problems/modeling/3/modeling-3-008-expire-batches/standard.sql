DELETE FROM batches
USING cutoff
WHERE batches.site = cutoff.site AND batches.day < cutoff.day;
