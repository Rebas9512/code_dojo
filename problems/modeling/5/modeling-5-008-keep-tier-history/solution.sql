UPDATE levels t SET until_day=c.day,current_flag=false FROM changes c
WHERE t.id=c.id AND t.current_flag;
INSERT INTO levels(id,tier,since,until_day,current_flag)
SELECT id,tier,day,NULL,true FROM changes;
