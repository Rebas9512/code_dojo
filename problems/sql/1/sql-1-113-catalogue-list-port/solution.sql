SELECT bin, STRING_AGG(DISTINCT label, '/' ORDER BY label) AS labels
FROM bin_labels GROUP BY bin;
