CREATE TABLE claims (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner text NOT NULL
);
INSERT INTO claims(owner) VALUES ('ivy'),('sam');
