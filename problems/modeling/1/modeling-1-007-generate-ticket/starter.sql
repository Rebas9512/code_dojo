CREATE TABLE claims (
    id integer /* 补上自动分配编号的声明 */ ____ PRIMARY KEY,
    owner text NOT NULL
);
INSERT INTO claims(owner) VALUES ('ivy'),('sam');
