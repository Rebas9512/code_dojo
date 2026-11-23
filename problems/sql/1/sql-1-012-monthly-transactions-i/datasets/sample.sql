CREATE TABLE payments (paid_on date NOT NULL, region text, state text NOT NULL, amount integer NOT NULL);
INSERT INTO payments VALUES ('2025-04-01','南','approved',20),('2025-04-17','南','declined',12),('2025-04-30','北','declined',8),('2026-04-30','南','declined',32);
