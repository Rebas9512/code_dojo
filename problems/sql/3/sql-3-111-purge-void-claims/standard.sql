DELETE FROM paper_claims p
WHERE EXISTS (
    SELECT 1
    FROM void_slips v
    WHERE v.claim = p.claim
);
