CREATE TABLE people (person_id integer PRIMARY KEY, years integer NOT NULL);
CREATE TABLE assignments (project_id integer, person_id integer REFERENCES people, PRIMARY KEY (project_id, person_id));
INSERT INTO people VALUES (2,2),(4,5),(5,4);
INSERT INTO assignments VALUES (30,2),(30,4),(30,5),(17,4);
