UPDATE levels
SET until_day = changes.day, current_flag = FALSE
FROM changes
WHERE levels.id = changes.id AND levels.current_flag;

INSERT INTO levels (id, tier, since, until_day, current_flag)
SELECT id, tier, day, NULL, TRUE
FROM changes;
