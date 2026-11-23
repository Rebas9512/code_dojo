CREATE TABLE upgrades (member_id int,tier text,start_on date);
INSERT INTO upgrades VALUES (1,'base','2025-01-01'),(1,'gold','2025-04-01'),(2,'base','2025-01-01');
CREATE TABLE paylog (id int PRIMARY KEY,member_id int,day date,amount numeric(9,2));
INSERT INTO paylog VALUES (31,1,'2025-03-31',3.50),(32,1,'2025-04-01',8.00),(33,2,'2025-04-01',2.00);
