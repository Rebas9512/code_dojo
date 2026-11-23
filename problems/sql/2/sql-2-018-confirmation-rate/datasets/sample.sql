CREATE TABLE accounts (account_id integer PRIMARY KEY);
CREATE TABLE checks (check_id integer PRIMARY KEY, account_id integer NOT NULL REFERENCES accounts, outcome text NOT NULL);
INSERT INTO accounts VALUES (2),(4),(8);
INSERT INTO checks VALUES (1,4,'ok'),(2,4,'timeout'),(3,8,'timeout'),(4,4,'timeout');
