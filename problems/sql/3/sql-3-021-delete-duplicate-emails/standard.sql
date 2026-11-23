SELECT entry.id, entry.email
FROM address_book entry
WHERE NOT EXISTS (
    SELECT 1
    FROM address_book earlier
    WHERE earlier.email = entry.email AND earlier.id < entry.id
);
