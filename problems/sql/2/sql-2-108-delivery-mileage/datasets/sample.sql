CREATE TABLE binders (badge integer, given text, family text);
INSERT INTO binders VALUES
    (11, 'Ivo', 'Lane'),
    (12, 'Ona', 'Hall'),
    (13, 'Teo', 'Moss');

CREATE TABLE route_lengths (badge integer, km integer);
INSERT INTO route_lengths VALUES
    (11, 4),
    (11, 6),
    (13, 10);
