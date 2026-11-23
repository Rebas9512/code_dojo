SELECT e.edition, e.label
FROM editions e
WHERE EXISTS (
    SELECT 1
    FROM dispatches d
    WHERE d.edition = e.edition
)
AND NOT EXISTS (
    SELECT 1
    FROM dispatches d
    WHERE d.edition = e.edition
      AND (d.day < DATE '2025-03-01' OR d.day > DATE '2025-05-31')
);
