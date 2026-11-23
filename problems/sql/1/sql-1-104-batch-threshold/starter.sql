SELECT rack, SUM(sheets) AS sheets FROM sheet_lots
WHERE sheets >= 7 GROUP BY rack;
