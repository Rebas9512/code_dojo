SELECT `rack`, SUM(sheets) AS total FROM sheet_lots GROUP BY rack;
