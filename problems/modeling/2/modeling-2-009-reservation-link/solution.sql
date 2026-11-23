CREATE TABLE requests (
    id int PRIMARY KEY,
    depot_id int REFERENCES depots(id)
);
