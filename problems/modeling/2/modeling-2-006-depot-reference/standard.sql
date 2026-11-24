CREATE TABLE handoffs (
    id int PRIMARY KEY,
    depot_id int NOT NULL REFERENCES depots(id)
);
