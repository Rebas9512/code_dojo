ALTER TABLE codes ADD UNIQUE (code);

INSERT INTO codes (code)
SELECT code
FROM incoming
ON CONFLICT (code) DO NOTHING;
