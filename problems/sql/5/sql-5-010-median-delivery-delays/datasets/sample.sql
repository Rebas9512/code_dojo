CREATE TABLE shipments (shipment int PRIMARY KEY, route text, delay_days int);
INSERT INTO shipments VALUES
    (1, '北', 1),
    (2, '北', 4),
    (3, '北', 6),
    (4, '北', 12),
    (5, '南', 7),
    (6, '南', NULL),
    (7, '西', NULL);
