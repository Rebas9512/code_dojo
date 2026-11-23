SELECT employee_id, dept
FROM assignments
WHERE main_flag = 'Y' OR employee_id IN (
    SELECT employee_id
    FROM assignments
    GROUP BY employee_id
    HAVING COUNT(*) = 1
);
