CREATE TABLE students (student_id integer PRIMARY KEY, name text NOT NULL);
CREATE TABLE subjects (subject text PRIMARY KEY);
CREATE TABLE attendance (student_id integer NOT NULL REFERENCES students, subject text NOT NULL REFERENCES subjects);
INSERT INTO students VALUES (9,'文'),(2,'林');
INSERT INTO subjects VALUES ('Maps'),('Ink');
INSERT INTO attendance VALUES (2,'Maps'),(2,'Maps'),(9,'Ink');
