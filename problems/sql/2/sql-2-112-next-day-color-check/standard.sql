SELECT today.press, today.day
FROM ink_checks today
JOIN ink_checks prev ON prev.press = today.press AND prev.day + 1 = today.day
WHERE today.shade > prev.shade;
