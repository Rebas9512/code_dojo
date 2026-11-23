CREATE TABLE staff (staff_id integer PRIMARY KEY, name text NOT NULL);
CREATE TABLE bonuses (staff_id integer PRIMARY KEY REFERENCES staff, amount integer NOT NULL);
INSERT INTO staff VALUES (1,'小杭'),(3,'阿禾'),(5,'叶朗'),(7,'沈竹');
INSERT INTO bonuses VALUES (3,600),(5,1000),(7,1300);
