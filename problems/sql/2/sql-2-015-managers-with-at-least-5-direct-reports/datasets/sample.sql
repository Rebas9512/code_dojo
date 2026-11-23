CREATE TABLE crew (person_id integer PRIMARY KEY, name text NOT NULL, leader_id integer REFERENCES crew);
INSERT INTO crew VALUES (1,'许兰',NULL),(2,'顾真',1),(3,'朴',1),(4,'夏青',1),(5,'关',1),(6,'张本',1),(7,'卢',2);
