SELECT binder, cutter
FROM binding_jobs
GROUP BY binder, cutter
HAVING COUNT(*) >= 3;
