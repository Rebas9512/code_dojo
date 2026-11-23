DELETE FROM batches b USING cutoff c
WHERE b.site=c.site AND b.day<c.day;
