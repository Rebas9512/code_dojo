CREATE TABLE customer (
    id integer PRIMARY KEY,
    name text NOT NULL,
    referee_id integer
);

INSERT INTO customer VALUES
    (2, '阿澄', NULL),
    (8, '小池', 2),
    (5, '白帆', NULL),
    (10, '小池', 5);
