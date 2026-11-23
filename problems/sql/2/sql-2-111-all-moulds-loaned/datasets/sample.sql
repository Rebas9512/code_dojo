CREATE TABLE mould_stock (design text, copies integer);
INSERT INTO mould_stock VALUES
    ('Elm', 2),
    ('Ash', 1),
    ('Oak', 2);

CREATE TABLE mould_loans (design text, slip integer, back date);
INSERT INTO mould_loans VALUES
    ('Elm', 1, NULL),
    ('Elm', 2, NULL),
    ('Elm', 3, '2025-02-01'),
    ('Ash', 4, NULL),
    ('Oak', 5, NULL);
