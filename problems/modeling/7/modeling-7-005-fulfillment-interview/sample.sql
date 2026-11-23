CREATE TABLE dispatch (parcel_id int PRIMARY KEY, order_id int, depot_id int, city text, shipped_on date, units int);
INSERT INTO dispatch VALUES
    (10,80,1,'York','2025-05-01',2),
    (11,80,1,'York','2025-05-01',3),
    (12,81,2,'Bath','2025-05-02',1);
