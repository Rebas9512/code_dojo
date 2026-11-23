SELECT m.name
FROM makers m
WHERE NOT EXISTS (
    SELECT 1
    FROM ink_orders i
    WHERE i.maker = m.maker AND i.pigment = 'red'
);
