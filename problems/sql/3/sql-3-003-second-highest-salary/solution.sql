SELECT MAX(salary) AS second_salary
FROM payroll WHERE salary < (SELECT MAX(salary) FROM payroll);
