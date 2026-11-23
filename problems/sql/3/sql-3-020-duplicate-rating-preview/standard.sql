DELETE FROM address_book current_entry
WHERE EXISTS (
    SELECT 1
    FROM address_book earlier
    WHERE earlier.email = current_entry.email AND earlier.id < current_entry.id
);
