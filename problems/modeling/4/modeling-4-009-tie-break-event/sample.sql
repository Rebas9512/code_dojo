CREATE TABLE catalog (id int PRIMARY KEY,rev int,tag text); INSERT INTO catalog VALUES (3,4,'keep');
CREATE TABLE feed (id int,rev int,tag text); INSERT INTO feed VALUES (1,3,'gold'),(1,1,'base'),(2,1,'plus');
ALTER TABLE feed ADD COLUMN event_id int; UPDATE feed SET event_id=10*rev+id; UPDATE feed SET event_id=30 WHERE id=1 AND rev=3; INSERT INTO feed VALUES (1,3,'blue',90);
