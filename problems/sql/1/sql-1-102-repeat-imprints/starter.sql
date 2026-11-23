SELECT imprint, COUNT(*) AS slips
FROM proof_slips
GROUP BY imprint
____;
