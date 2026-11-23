CREATE TABLE friendships (sender int, receiver int, PRIMARY KEY(sender, receiver));
INSERT INTO friendships VALUES
    (1, 2),
    (3, 2),
    (2, 4),
    (3, 4);
