CREATE TABLE stock (
    qty integer NOT NULL CHECK (qty >= 0)
);
