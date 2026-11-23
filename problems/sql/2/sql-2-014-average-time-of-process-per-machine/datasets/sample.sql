CREATE TABLE events (machine_id integer, batch_id integer, kind text, moment numeric NOT NULL, PRIMARY KEY (machine_id, batch_id, kind));
INSERT INTO events VALUES (3,1,'start',1.5),(3,1,'end',4.503),(3,2,'start',2),(3,2,'end',4),(7,1,'start',10),(7,1,'end',16);
