CREATE TABLE parcel_shops (shop integer);
INSERT INTO parcel_shops VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE parcel_log (parcel integer, shop integer, state text);
INSERT INTO parcel_log VALUES
    (18, 1, 'sent'),
    (19, 1, 'signed'),
    (20, 2, 'sent'),
    (21, 4, 'signed');
