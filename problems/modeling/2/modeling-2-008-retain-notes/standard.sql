CREATE TABLE notes (
    id int PRIMARY KEY,
    depot_id int REFERENCES depots(id) ON DELETE SET NULL
);

INSERT INTO notes VALUES (11, 4), (12, 8);

DELETE FROM depots
WHERE id = 4;
