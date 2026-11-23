SELECT n.press, n.day FROM ink_checks n
JOIN ink_checks p ON n.press = p.press AND n.day = DATE_ADD(p.day, INTERVAL 1 DAY)
WHERE n.shade > p.shade;
