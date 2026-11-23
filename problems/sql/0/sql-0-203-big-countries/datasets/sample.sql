CREATE TABLE world (
    name text PRIMARY KEY,
    continent text NOT NULL,
    area integer NOT NULL,
    population integer NOT NULL,
    gdp bigint NOT NULL
);

INSERT INTO world VALUES
    ('松湾', '南洲', 3010000, 9200000, 81000000000),
    ('石原', '东洲', 410000, 27000000, 39000000000),
    ('星屿', '东洲', 82000, 4500000, 6200000000);
