SELECT m.design, COUNT(*) AS on_loan
FROM mould_stock m JOIN mould_loans l ON l.design = m.design
WHERE l.back IS NULL
GROUP BY m.design, m.copies HAVING COUNT(*) = m.copies
ORDER BY on_loan DESC, m.design;
