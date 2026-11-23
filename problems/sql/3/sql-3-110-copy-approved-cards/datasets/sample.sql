CREATE TABLE proof_queue (slip integer, verdict text, sheets integer);
INSERT INTO proof_queue VALUES
    (21, 'pass', 8),
    (22, 'hold', 5),
    (23, 'pass', 12);

CREATE TABLE proof_archive (slip integer, sheets integer);
INSERT INTO proof_archive VALUES
    (9, 4);
