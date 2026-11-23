CREATE TABLE binders (badge integer, given text, family text);
INSERT INTO binders VALUES
    (11, 'Ivo', 'Lane'),
    (12, 'Ona', 'Hall'),
    (13, 'Teo', 'Moss');

CREATE TABLE credit_moves (badge integer, coins integer);
INSERT INTO credit_moves VALUES
    (11, 70),
    (11, 45),
    (12, 140),
    (12, -40),
    (13, 35);
