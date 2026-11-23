DELETE FROM paper_claims p
WHERE NOT EXISTS (SELECT 1 FROM void_slips v WHERE v.claim = p.claim);
