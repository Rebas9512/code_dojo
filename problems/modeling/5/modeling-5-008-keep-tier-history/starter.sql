INSERT INTO levels(id,tier,since,until_day,current_flag)
SELECT id,tier,day,NULL,true FROM changes;
