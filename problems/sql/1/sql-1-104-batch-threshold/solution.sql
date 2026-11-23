SELECT rack, SUM(sheets) AS sheets FROM sheet_lots
GROUP BY rack HAVING SUM(sheets) >= 7;
