CREATE TABLE team (person_id integer PRIMARY KEY, name text NOT NULL, leader_id integer REFERENCES team, age integer NOT NULL);
INSERT INTO team VALUES (1,'汪宜',NULL,45),(2,'方奇',1,27),(4,'小翎',1,32),(5,'梧桐',2,22);
