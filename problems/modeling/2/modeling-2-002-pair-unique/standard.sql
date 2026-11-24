CREATE TABLE tags (
    branch text NOT NULL,
    name text NOT NULL,
    UNIQUE(branch,name)
);
INSERT INTO tags VALUES ('east','new');
