CREATE TABLE catalog (id int PRIMARY KEY,rev int,tag text); INSERT INTO catalog VALUES (3,4,'keep');
CREATE TABLE feed (id int,rev int,tag text); INSERT INTO feed VALUES (1,3,'gold'),(1,1,'base'),(2,1,'plus'); INSERT INTO feed VALUES (3,2,'late');
