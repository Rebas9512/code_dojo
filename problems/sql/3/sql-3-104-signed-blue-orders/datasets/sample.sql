CREATE TABLE makers (maker integer, name text);
INSERT INTO makers VALUES
    (1, 'Ari'),
    (2, 'Bo'),
    (3, 'Cy'),
    (4, 'Dee');

CREATE TABLE ink_orders (ticket integer, maker integer, pigment text);
INSERT INTO ink_orders VALUES
    (11, 1, 'red'),
    (12, 1, 'blue'),
    (13, 2, 'blue'),
    (14, NULL, 'red');
