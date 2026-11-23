CREATE VIEW open_jobs AS
SELECT id,fee FROM jobs WHERE state='open';
