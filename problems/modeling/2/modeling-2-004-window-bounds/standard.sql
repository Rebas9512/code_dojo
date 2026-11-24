CREATE TABLE loans (
    start_on date NOT NULL,
    due_on date NOT NULL,
    CHECK (due_on >= start_on)
);
