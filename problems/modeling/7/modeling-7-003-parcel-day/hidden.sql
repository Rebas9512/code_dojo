INSERT INTO dispatch VALUES (13,82,3,'York','2025-05-01',4),(14,82,3,'York','2025-05-02',2);
INSERT INTO depots VALUES (3,'York'); INSERT INTO parcels SELECT parcel_id,order_id,depot_id,shipped_on,units FROM dispatch WHERE parcel_id>=13;
