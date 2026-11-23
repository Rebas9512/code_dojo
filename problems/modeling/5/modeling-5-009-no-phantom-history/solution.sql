CREATE TEMP TABLE delta AS
SELECT c.* FROM changes c LEFT JOIN levels t ON t.id=c.id AND t.current_flag
WHERE t.id IS NULL OR t.tier<>c.tier;
UPDATE levels t SET until_day=c.day,current_flag=false FROM delta c
WHERE t.id=c.id AND t.current_flag;
INSERT INTO levels(id,tier,since,until_day,current_flag)
SELECT id,tier,day,NULL,true FROM delta;
