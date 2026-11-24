UPDATE levels
SET until_day = changes.day, current_flag = FALSE
FROM changes
WHERE levels.id = changes.id AND levels.current_flag AND levels.tier <> changes.tier;

INSERT INTO levels (id, tier, since, until_day, current_flag)
SELECT c.id, c.tier, c.day, NULL, TRUE
FROM changes c
LEFT JOIN levels l ON l.id = c.id AND l.current_flag
WHERE l.id IS NULL;
