CREATE TABLE tickets (
    title text NOT NULL,
    status text NOT NULL DEFAULT 'open'
);
INSERT INTO tickets(title) VALUES ('pack');
