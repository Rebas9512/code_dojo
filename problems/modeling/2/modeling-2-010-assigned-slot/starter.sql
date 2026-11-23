CREATE TABLE slots (
    depot_id int REFERENCES depots(id),
    day date,
    PRIMARY KEY(depot_id)
);
