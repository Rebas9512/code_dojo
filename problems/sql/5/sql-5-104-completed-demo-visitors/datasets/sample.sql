CREATE TABLE demo_steps (visitor text, tick integer, action text);
INSERT INTO demo_steps VALUES
    ('A', 1, 'sample'),
    ('A', 3, 'reserve'),
    ('A', 5, 'pay'),
    ('B', 1, 'pay'),
    ('B', 2, 'sample'),
    ('B', 2, 'reserve'),
    ('C', 2, 'sample'),
    ('C', 4, 'reserve'),
    ('C', 4, 'pay');
