UPDATE levels t SET until_day=c.day,current_flag=false FROM changes c
WHERE /* 限定待关闭的版本 */ ____;
