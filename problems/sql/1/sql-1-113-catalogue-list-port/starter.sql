SELECT bin, GROUP_CONCAT(DISTINCT label ORDER BY label SEPARATOR '/') AS labels
FROM bin_labels GROUP BY bin;
