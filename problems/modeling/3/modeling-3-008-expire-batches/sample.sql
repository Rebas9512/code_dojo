CREATE TABLE batches (site text,day date); INSERT INTO batches VALUES ('east','2025-01-01'),('east','2025-01-02'),('west','2025-01-01');
CREATE TABLE cutoff (site text PRIMARY KEY,day date); INSERT INTO cutoff VALUES ('east','2025-01-02');
