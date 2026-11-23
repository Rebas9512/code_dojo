SELECT n.press, n.day FROM ink_checks n
JOIN ink_checks p ON n.press = p.press AND n.day = p.day + 1
WHERE n.shade > p.shade;
