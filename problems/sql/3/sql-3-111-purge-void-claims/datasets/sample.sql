CREATE TABLE paper_claims (claim integer, sheets integer);
INSERT INTO paper_claims VALUES
    (1, 8),
    (2, 5),
    (3, 11),
    (4, 3);

CREATE TABLE void_slips (claim integer);
INSERT INTO void_slips VALUES
    (2),
    (4),
    (NULL);
