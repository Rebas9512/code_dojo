CREATE TABLE assignments (employee_id int, dept int, main_flag text, PRIMARY KEY(employee_id, dept));
INSERT INTO assignments VALUES
    (1, 9, 'N'),
    (2, 9, 'N'),
    (2, 3, 'Y'),
    (3, 4, 'N');
