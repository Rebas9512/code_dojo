UPDATE levels
SET until_day = changes.day, current_flag = FALSE
FROM changes
WHERE levels.id = changes.id AND levels.current_flag;
