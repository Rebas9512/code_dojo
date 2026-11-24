CREATE VIEW fee_summary AS
SELECT state, COUNT(*) AS jobs_n, SUM(fee) AS total_fee
FROM jobs
GROUP BY state;
