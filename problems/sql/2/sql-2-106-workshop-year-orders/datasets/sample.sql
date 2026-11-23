CREATE TABLE workshops (shop integer, opened date);
INSERT INTO workshops VALUES
    (1, '2024-03-01'),
    (2, '2025-01-02'),
    (3, '2024-02-02');

CREATE TABLE print_orders (ticket integer, shop integer, placed date);
INSERT INTO print_orders VALUES
    (10, 1, '2025-02-01'),
    (11, 1, '2025-12-31'),
    (12, 2, '2024-12-31');
