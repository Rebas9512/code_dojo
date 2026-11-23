CREATE TABLE presses (press integer);
INSERT INTO presses VALUES
    (1),
    (2),
    (7);

CREATE TABLE job_fees (job integer, press integer, fee integer);
INSERT INTO job_fees VALUES
    (11, 1, 20),
    (12, 1, 20),
    (13, 2, 7);

CREATE TABLE job_parts (job integer, part text);
INSERT INTO job_parts VALUES
    (11, 'A'),
    (11, 'B'),
    (12, 'C'),
    (13, 'A');
