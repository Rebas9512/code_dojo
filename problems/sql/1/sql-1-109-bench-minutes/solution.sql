SELECT worker, day, SUM(leave_min - enter_min) AS minutes
FROM bench_slots GROUP BY worker, day;
