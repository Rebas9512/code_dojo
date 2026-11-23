SELECT g.hall FROM galleries g
LEFT JOIN exhibits e ON e.hall = g.hall
WHERE e.work IS NULL;
