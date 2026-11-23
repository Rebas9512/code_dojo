CREATE TABLE staff (staff_id integer PRIMARY KEY, name text NOT NULL);
CREATE TABLE badges (staff_id integer PRIMARY KEY REFERENCES staff, badge_id integer UNIQUE NOT NULL);
INSERT INTO staff VALUES (2,'杨青'),(3,'阿索'),(5,'杨青');
INSERT INTO badges VALUES (5,702),(3,910);
