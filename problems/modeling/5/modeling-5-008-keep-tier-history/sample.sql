CREATE TABLE levels (id int, tier text, since date, until_day date, current_flag boolean, PRIMARY KEY(id,since));
INSERT INTO levels VALUES (1,'base','2025-01-01',NULL,true),(2,'base','2025-01-01',NULL,true);
CREATE TABLE changes (id int,tier text,day date); INSERT INTO changes VALUES (1,'gold','2025-03-01');
